"""
Serviço para enviar notificações via Telegram
"""

import sys
from pathlib import Path
from typing import Optional

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from datetime import datetime, date
from shared.config.settings import settings
from shared.utils.logger import bot_telegram_logger as logger
from services.alertas_service import alertas_service

try:
    from telegram import Bot
    from telegram.constants import ParseMode
except ImportError:
    logger.warning("python-telegram-bot não disponível para notificações")
    Bot = None


class TelegramNotifier:
    """Serviço para enviar alertas via Telegram"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.bot = Bot(token=self.bot_token) if self.bot_token and Bot else None
    
    async def enviar_alerta_prazo(self, user_telegram_id: int, prazo: dict, dias_restantes: int) -> bool:
        """
        Envia alerta de prazo via Telegram
        
        Args:
            user_telegram_id: ID do Telegram do usuário
            prazo: Dict com dados do prazo
            dias_restantes: Dias até o vencimento
            
        Returns:
            bool: True se enviado com sucesso
        """
        if not self.bot:
            logger.error("Bot do Telegram não configurado")
            return False
        
        try:
            # Determinar emoji e prioridade
            if dias_restantes == 0:
                emoji = "🔴"
                urgência = "URGENTE - VENCE HOJE!"
            elif dias_restantes == 1:
                emoji = "🟠"
                urgência = "MUITO URGENTE - Vence amanhã!"
            elif dias_restantes <= 3:
                emoji = "🟡"
                urgência = f"ATENÇÃO - Vence em {dias_restantes} dias"
            else:
                emoji = "🟢"
                urgência = f"Vence em {dias_restantes} dias"
            
            # Formatar mensagem
            mensagem = f"""🔔 *ALERTA DE PRAZO PROCESSUAL*

{emoji} *{urgência}*

📋 *Tipo:* {prazo.get('tipo', 'N/A')}
📄 *Processo:* {prazo.get('processo', 'N/A')}
🏛️ *Tribunal:* {prazo.get('tribunal', 'N/A')}
📅 *Data de Vencimento:* {prazo.get('data_vencimento', 'N/A')}

💡 *Lembrete:* Não esqueça de cumprir o prazo!
📊 Use /prazos para ver todos os prazos pendentes."""
            
            # Enviar mensagem
            await self.bot.send_message(
                chat_id=user_telegram_id,
                text=mensagem,
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Registrar no histórico
            user = alertas_service.get_user_by_telegram_id(user_telegram_id)
            if user:
                alertas_service.registrar_notificacao(
                    user_id=user.id,
                    prazo_id=prazo.get('id'),
                    canal="telegram",
                    mensagem=mensagem,
                    status="enviada"
                )
            
            logger.info(f"Alerta enviado para Telegram ID {user_telegram_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar alerta via Telegram: {e}")
            
            # Tentar registrar falha
            try:
                user = alertas_service.get_user_by_telegram_id(user_telegram_id)
                if user:
                    alertas_service.registrar_notificacao(
                        user_id=user.id,
                        prazo_id=prazo.get('id'),
                        canal="telegram",
                        mensagem=f"Erro ao enviar: {str(e)}",
                        status="falhou"
                    )
            except:
                pass
            
            return False
    
    async def verificar_e_enviar_alertas(self):
        """
        Verifica prazos próximos e envia alertas conforme preferências
        Função a ser chamada pelo scheduler
        """
        from shared.config.database import get_db
        from shared.database.models import Prazo, User
        from datetime import timedelta
        
        if not self.bot:
            return
        
        db = next(get_db())
        
        try:
            hoje = date.today()
            
            # Buscar todos os usuários com alertas ativos
            usuarios_ativos = db.query(User).filter(
                User.telegram_id.isnot(None),
                User.alerta_ativo == True
            ).all()
            
            logger.info(f"Verificando alertas para {len(usuarios_ativos)} usuários...")
            
            for user in usuarios_ativos:
                if not user.telegram_id:
                    continue
                
                intervalo_dias = user.alerta_intervalo_dias or 3
                data_limite = hoje + timedelta(days=intervalo_dias)
                
                # Buscar prazos do usuário que vencem no intervalo
                prazos = db.query(Prazo).filter(
                    Prazo.user_id == user.id,
                    Prazo.status == "pendente",
                    Prazo.data_vencimento <= data_limite,
                    Prazo.data_vencimento >= hoje
                ).all()
                
                for prazo in prazos:
                    dias_restantes = (prazo.data_vencimento - hoje).days
                    
                    # Verificar se já foi notificado hoje
                    hoje_inicio = datetime.combine(hoje, datetime.min.time())
                    if prazo.ultima_notificacao and prazo.ultima_notificacao >= hoje_inicio:
                        continue  # Já notificado hoje
                    
                    # Verificar canal preferido
                    canal = user.alerta_canal or "telegram"
                    
                    if canal == "telegram" or canal == "ambos":
                        prazo_dict = {
                            "id": prazo.id,
                            "tipo": prazo.tipo,
                            "processo": prazo.processo,
                            "tribunal": prazo.tribunal,
                            "data_vencimento": prazo.data_vencimento.strftime("%d/%m/%Y")
                        }
                        
                        await self.enviar_alerta_prazo(
                            user.telegram_id,
                            prazo_dict,
                            dias_restantes
                        )
                        
                        # Atualizar prazo
                        prazo.ultima_notificacao = datetime.now()
                        if dias_restantes <= 1:
                            prazo.alertas_enviados += 1
                
                db.commit()
            
        except Exception as e:
            logger.error(f"Erro ao verificar e enviar alertas: {e}")
            db.rollback()
        finally:
            db.close()


# Instância global
telegram_notifier = TelegramNotifier()

