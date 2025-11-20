"""
Serviço de gestão de prazos processuais com integração ao Kermartin
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from typing import List, Optional, Dict
from datetime import datetime, timedelta
from shared.utils.logger import bot_telegram_logger as logger
from services.database_service import db_service


class PrazosService:
    """Serviço de gestão de prazos"""
    
    def formatar_prazos(self, prazos: List) -> str:
        """
        Formata lista de prazos para mensagem do Telegram
        
        Args:
            prazos: Lista de objetos Prazo
        
        Returns:
            Texto formatado para envio
        """
        if not prazos:
            return """📅 **Seus Prazos Processuais**

✅ Você não possui prazos pendentes no momento.

Use /alerta para configurar notificações automáticas!"""

        texto = "📅 **Seus Prazos Processuais**\n\n"
        
        hoje = datetime.now().date()
        
        for prazo in prazos[:10]:  # Limitar a 10
            data_venc = prazo.data_vencimento if isinstance(prazo.data_vencimento, datetime) else prazo.data_vencimento
            dias_restantes = (data_venc - hoje).days
            
            # Emoji de urgência
            if dias_restantes <= 1:
                emoji = "🔴 URGENTE"
            elif dias_restantes <= 3:
                emoji = "🟡 ALERTA"
            else:
                emoji = "🟢 OK"
            
            texto += f"{emoji} **{prazo.tipo}**\n"
            
            if hasattr(prazo, 'processo') and prazo.processo:
                texto += f"📄 Processo: {prazo.processo}\n"
            
            if hasattr(prazo, 'tribunal') and prazo.tribunal:
                texto += f"🏛️ Tribunal: {prazo.tribunal}\n"
            
            texto += f"📅 Vence em: {data_venc.strftime('%d/%m/%Y')}\n"
            texto += f"⏰ {dias_restantes} dias restantes\n\n"
        
        if len(prazos) > 10:
            texto += f"... e mais {len(prazos) - 10} prazos.\n\n"
        
        texto += "💡 Use /alerta para configurar notificações automáticas!"
        
        return texto
    
    def sincronizar_prazos_kermartin(self, user_id: int, telegram_id: int) -> List[Dict]:
        """
        Sincroniza prazos com processos do Kermartin
        
        Args:
            user_id: ID do usuário no banco
            telegram_id: ID do Telegram do usuário
            
        Returns:
            Lista de prazos sincronizados
        """
        try:
            from services.kermartin_service import kermartin_service
            from services.auth_service import auth_service
            
            # Verificar autenticação
            if not auth_service.is_authenticated(telegram_id):
                return []
            
            # Buscar processos do usuário no Kermartin
            # Por enquanto, buscar processos recentes (pode ser melhorado com busca por usuário)
            processos = kermartin_service.buscar_processos_rag({})
            
            prazos_sincronizados = []
            
            for processo in processos[:20]:  # Limitar a 20 processos
                try:
                    metadata = processo.get('metadata_json', {})
                    if isinstance(metadata, str):
                        import json
                        try:
                            metadata = json.loads(metadata)
                        except:
                            metadata = {}
                    
                    numero = processo.get('processo_numero') or processo.get('numero')
                    ultima_mov = metadata.get('ultima_movimentacao') or metadata.get('data_ultima_mov')
                    
                    if numero and ultima_mov:
                        # Calcular prazo baseado na última movimentação
                        # Prazo padrão: 15 dias para contestação, 8 dias para recurso
                        try:
                            data_mov = datetime.strptime(ultima_mov[:10], '%Y-%m-%d')
                            prazo_dias = 15  # Prazo padrão para contestação
                            data_vencimento = data_mov + timedelta(days=prazo_dias)
                            
                            if data_vencimento > datetime.now():
                                prazos_sincronizados.append({
                                    'processo': numero,
                                    'tipo': 'Contestação',
                                    'data_vencimento': data_vencimento,
                                    'tribunal': metadata.get('tribunal', 'N/A'),
                                    'comarca': metadata.get('comarca', 'N/A'),
                                    'fonte': 'Kermartin'
                                })
                        except:
                            continue
                            
                except Exception as e:
                    logger.warning(f"Erro ao processar processo para prazos: {e}")
                    continue
            
            logger.info(f"Sincronizados {len(prazos_sincronizados)} prazos do Kermartin para usuário {user_id}")
            return prazos_sincronizados
            
        except Exception as e:
            logger.error(f"Erro ao sincronizar prazos com Kermartin: {e}")
            return []
    
    def criar_prazo_exemplo(self, user_id: int) -> str:
        """
        Cria um prazo de exemplo para demonstração
        
        Isso é útil para testes quando não há banco de dados configurado
        """
        logger.info(f"Gerando prazo de exemplo para usuário {user_id}")
        
        return """📅 **Prazos de Exemplo**

🔴 URGENTE **Contestação**
📄 Processo: 0001234-56.2024.8.26.0100
🏛️ Tribunal: TJMG - 26ª Vara Cível de Belo Horizonte
📅 Vence em: 02/11/2024
⏰ 0 dias restantes

---

🟡 ALERTA **Recurso de Apelação**
📄 Processo: 0005678-90.2024.5.08.0024
🏛️ Tribunal: TRT-08 (Manaus)
📅 Vence em: 05/11/2024
⏰ 3 dias restantes

---

🟢 OK **Impugnação ao Termo de Inicial**
📄 Processo: 0009012-34.2024.8.22.0001
🏛️ Tribunal: TJSP - Foro Central - 10ª Vara Cível
📅 Vence em: 15/11/2024
⏰ 13 dias restantes

💡 Use /alerta para configurar notificações!"""


# Instância global
prazos_service = PrazosService()

