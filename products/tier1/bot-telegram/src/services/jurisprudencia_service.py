"""
Serviço de busca de jurisprudência com IA
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from typing import Dict, List, Optional
from shared.config.settings import settings
from shared.utils.logger import bot_telegram_logger as logger
from services.ia_service import ai_service


class JurisprudenciaService:
    """Serviço de busca de jurisprudência"""
    
    def __init__(self):
        self.ia_service = ai_service
    
    def _parse_filtros(self, query: str) -> tuple[str, Dict]:
        """
        Parse filtros da query (--tribunal, --data, --assunto, --magistrado, --limite)
        Suporta valores com múltiplas palavras usando aspas
        
        Returns:
            (query_limpa, filtros_dict)
        """
        filtros = {
            'tribunal': None,
            'data': None,
            'assunto': None,
            'magistrado': None,
            'limite': 10
        }
        
        # Parse melhorado que suporta valores com espaços usando aspas
        import re
        
        # Padrão para encontrar --chave "valor com espaços" ou --chave valor
        pattern = r'--(\w+)\s+(?:"([^"]+)"|(\S+))'
        matches = re.findall(pattern, query)
        
        query_limpa = query
        for match in matches:
            chave = match[0].lower()
            valor = match[1] if match[1] else match[2]
            
            # Remover o filtro da query original
            query_limpa = re.sub(rf'--{chave}\s+(?:"[^"]+"|\S+)', '', query_limpa, count=1)
            
            if chave == 'limite':
                try:
                    filtros['limite'] = int(valor)
                except:
                    filtros['limite'] = 10
            elif chave in filtros:
                filtros[chave] = valor
        
        # Limpar espaços extras
        query_limpa = ' '.join(query_limpa.split()).strip()
        
        return query_limpa, filtros
    
    async def buscar_jurisprudencia(self, query: str, filtros: Optional[Dict] = None) -> str:
        """
        Busca jurisprudência usando IA com filtros opcionais
        
        Args:
            query: Consulta jurídica do usuário
            filtros: Dict com filtros (tribunal, data, assunto, magistrado, limite)
        
        Returns:
            Resposta formatada com jurisprudência
        """
        try:
            filtros = filtros or {}
            
            # Buscar processos no Kermartin se filtros especificados
            processos_relevantes = []
            if filtros.get('tribunal') or filtros.get('assunto') or filtros.get('magistrado'):
                try:
                    from services.kermartin_service import kermartin_service
                    filtro_kermartin = {}
                    if filtros.get('tribunal'):
                        filtro_kermartin['tribunal'] = filtros['tribunal']
                    if filtros.get('assunto'):
                        filtro_kermartin['assunto'] = filtros['assunto']
                    
                    processos_rag = kermartin_service.buscar_processos_rag(filtro_kermartin)
                    processos_relevantes = processos_rag[:filtros.get('limite', 10)]
                except Exception as e:
                    logger.warning(f"Erro ao buscar processos no Kermartin: {e}")
            
            # Construir prompt com contexto dos processos encontrados
            contexto_processos = ""
            if processos_relevantes:
                contexto_processos = "\n\nProcessos relevantes encontrados na base:\n"
                for i, proc in enumerate(processos_relevantes[:5], 1):
                    numero = proc.get('processo_numero') or proc.get('numero', 'N/A')
                    assunto = proc.get('assunto', 'N/A')
                    contexto_processos += f"{i}. Processo {numero}: {assunto}\n"
            
            # Prompt específico para jurisprudência
            filtros_texto = ""
            if filtros.get('tribunal'):
                filtros_texto += f"\nTribunal: {filtros['tribunal']}"
            if filtros.get('data'):
                filtros_texto += f"\nAno: {filtros['data']}"
            if filtros.get('assunto'):
                filtros_texto += f"\nAssunto: {filtros['assunto']}"
            if filtros.get('magistrado'):
                filtros_texto += f"\nMagistrado: {filtros['magistrado']}"
            
            prompt = f"""Você é um assistente jurídico especializado em jurisprudência brasileira.

Busque informações sobre: {query}{filtros_texto}

Forneça:
1. A definição/contexto jurídico
2. Principais precedentes relevantes
3. Jurisprudência dominante dos tribunais
4. Fundamento legal{contexto_processos}

Seja objetivo e cite fontes quando possível."""

            # Usar IA para gerar resposta
            response = await self.ia_service.process_message(prompt)
            
            # Formatar resposta com design profissional
            from utils.message_formatter import message_formatter
            
            resposta_formatada = message_formatter.header("BUSCA DE JURISPRUDÊNCIA", message_formatter.EMOJIS['busca'])
            
            resposta_formatada += message_formatter.section("Consulta",
                f"   🔍 {query}",
                message_formatter.EMOJIS['busca'])
            
            if filtros_texto:
                resposta_formatada += f"\n{message_formatter.SEPARADOR}\n\n"
                resposta_formatada += message_formatter.section("Filtros Aplicados",
                    filtros_texto.replace('\n', '\n   '),
                    "🔍")
            
            resposta_formatada += f"\n{message_formatter.SEPARADOR}\n\n"
            resposta_formatada += response
            
            if processos_relevantes:
                resposta_formatada += f"\n\n{message_formatter.SEPARADOR}\n\n"
                resposta_formatada += message_formatter.section("Processos Encontrados na Base",
                    "\n".join([
                        f"   {i}. Processo `{proc.get('processo_numero') or proc.get('numero', 'N/A')}`"
                        for i, proc in enumerate(processos_relevantes[:5], 1)
                    ]),
                    "📚")
            
            resposta_formatada += message_formatter.footer("💡 Esta resposta é baseada em jurisprudência consolidada. Sempre consulte um advogado para orientação específica.")

            logger.info(f"Busca de jurisprudência realizada: {query} (filtros: {filtros})")
            return resposta_formatada
            
        except Exception as e:
            logger.error(f"Erro ao buscar jurisprudência: {e}")
            return f"""🔍 **Busca de Jurisprudência**

**Consulta:** {query}

⚠️ No momento não consigo acessar a base de jurisprudência.

Por favor, tente mais tarde ou consulte diretamente:
• STF: https://jurisprudência.stf.jus.br
• STJ: https://sitar.stj.justica.gov.br
• Tribunais Regionais"""


# Instância global
jurisprudencia_service = JurisprudenciaService()

