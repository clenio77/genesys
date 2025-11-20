"""
Serviço para consultar processos via API Pública do CNJ (DataJud)
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List
import re

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import requests
from shared.utils.logger import bot_telegram_logger as logger


class CNJService:
    """Serviço para consultar processos via API CNJ"""
    
    # Base URL da API Pública do CNJ DataJud
    # Documentação: https://datajud-wiki.cnj.jus.br/api-publica/
    BASE_URL = "https://api-publica.datajud.cnj.jus.br"
    
    # Formatos válidos de número de processo
    # Exemplo: 0001234-56.2024.8.26.0100
    PROCESSO_PATTERN = re.compile(r'^(\d{7})-(\d{2})\.(\d{4})\.(\d)\.(\d{2})\.(\d{4})$')
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'GenesysBot/1.0'
        })
        # Cache será inicializado quando necessário (lazy loading)
        self._cache = None
    
    def _get_cache(self):
        """Lazy loading do cache"""
        if self._cache is None:
            try:
                from services.cache_service import cache_service
                self._cache = cache_service
            except ImportError:
                logger.warning("CacheService não disponível - cache desabilitado")
                self._cache = None
        return self._cache
    
    def validar_numero_processo(self, numero: str) -> bool:
        """
        Valida se o número do processo está no formato CNJ
        
        Formato esperado: NNNNNNN-DD.AAAA.J.TR.OOOO
        Exemplo: 0001234-56.2024.8.26.0100
        """
        numero_limpo = numero.replace(' ', '').replace('-', '-').replace('.', '.')
        return bool(self.PROCESSO_PATTERN.match(numero_limpo))
    
    def formatar_numero_processo(self, numero: str) -> Optional[str]:
        """
        Tenta formatar número de processo para padrão CNJ
        
        Retorna None se não conseguir formatar
        """
        # Remove espaços e caracteres extras
        numero_limpo = re.sub(r'[^\d.-]', '', numero)
        
        # Verifica se já está no formato correto
        if self.validar_numero_processo(numero_limpo):
            return numero_limpo
        
        # Tenta diferentes formatos comuns
        # Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
        # Pode vir como: NNNNNNNDDAAAJJTROOOO ou NNNNNNN-DD.AAAA.J.TR.OOOO
        
        # Remove todos os pontos e traços e tenta reconstruir
        apenas_numeros = re.sub(r'[^\d]', '', numero_limpo)
        
        if len(apenas_numeros) >= 20:
            # Tenta formatar: 7-2.4.1.2.4
            parte1 = apenas_numeros[:7]  # 7 dígitos
            parte2 = apenas_numeros[7:9]  # 2 dígitos
            parte3 = apenas_numeros[9:13]  # 4 dígitos (ano)
            parte4 = apenas_numeros[13:14]  # 1 dígito (segmento)
            parte5 = apenas_numeros[14:16]  # 2 dígitos (tribunal)
            parte6 = apenas_numeros[16:20]  # 4 dígitos (vara)
            
            formatado = f"{parte1}-{parte2}.{parte3}.{parte4}.{parte5}.{parte6}"
            if self.validar_numero_processo(formatado):
                return formatado
        
        return None
    
    def consultar_processo(self, numero_processo: str, telegram_id: Optional[int] = None) -> Optional[Dict]:
        """
        Consulta processo verificando PRIMEIRO no Kermartin, depois na API CNJ como fallback
        
        Princípio: Kermartin coleta → Genesys consulta
        - Prioridade 1: Kermartin (dados já coletados)
        - Prioridade 2: API CNJ (consulta pública, não extração)
        
        Args:
            numero_processo: Número do processo no formato CNJ
            telegram_id: ID do usuário Telegram (opcional, para verificar autenticação)
            
        Returns:
            Dict com dados do processo ou Dict com 'erro' se não encontrado
        """
        try:
            # Validar e formatar número
            numero_formatado = self.formatar_numero_processo(numero_processo)
            if not numero_formatado:
                logger.warning(f"Número de processo inválido: {numero_processo}")
                return {"erro": "Número de processo inválido"}
            
            # Verificar cache PRIMEIRO
            cache = self._get_cache()
            if cache:
                cache_key = f"processo:{numero_formatado}"
                cached_result = cache.get(cache_key, cache_type='processo')
                if cached_result is not None:
                    logger.info(f"✅ Processo encontrado no cache: {numero_formatado}")
                    return cached_result
            
            # PRIORIDADE 1: Verificar Kermartin PRIMEIRO (dados já coletados)
            try:
                from services.kermartin_service import kermartin_service
                from services.auth_service import auth_service
                
                # Verificar autenticação se necessário
                if telegram_id:
                    is_auth = auth_service.is_authenticated(telegram_id)
                    if not is_auth:
                        logger.info("Usuário não autenticado - Kermartin requer autenticação")
                    else:
                        logger.info(f"🔍 Verificando Kermartin primeiro: {numero_formatado}")
                        processo_kermartin = kermartin_service.buscar_processo_por_numero(numero_formatado)
                        if processo_kermartin:
                            logger.info("✅ Processo encontrado no Kermartin (dados coletados)!")
                            processo_kermartin['fonte'] = 'Kermartin (Base Local)'
                            # Armazenar no cache
                            if cache:
                                cache.set(f"processo:{numero_formatado}", processo_kermartin, cache_type='processo')
                            return processo_kermartin
                        else:
                            logger.info("Processo não encontrado no Kermartin")
                else:
                    # Sem telegram_id, tentar buscar mesmo assim (pode funcionar sem auth)
                    logger.info(f"🔍 Verificando Kermartin (sem auth): {numero_formatado}")
                    processo_kermartin = kermartin_service.buscar_processo_por_numero(numero_formatado)
                    if processo_kermartin:
                        logger.info("✅ Processo encontrado no Kermartin!")
                        processo_kermartin['fonte'] = 'Kermartin (Base Local)'
                        # Armazenar no cache
                        if cache:
                            cache.set(f"processo:{numero_formatado}", processo_kermartin, cache_type='processo')
                        return processo_kermartin
            except Exception as e:
                logger.warning(f"Erro ao buscar no Kermartin (continuando): {e}")
            
            # PRIORIDADE 2: Se não encontrou no Kermartin, consultar API CNJ (consulta pública)
            logger.info(f"🔍 Consultando API CNJ: {numero_formatado}")
            
            # Extrair tribunal do número do processo
            # Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
            # TR = código do tribunal (ex: 13 = TJMG, 02 = TJSP)
            partes = numero_formatado.split('.')
            if len(partes) >= 4:
                codigo_tribunal = partes[3]  # TR está na posição 3
                alias_tribunal = f"tj{codigo_tribunal}"
            else:
                alias_tribunal = "tj26"  # Default: TJMG
            
            # Montar URL da API
            # Formato: https://api-publica.datajud.cnj.jus.br/{alias}/processes/{numero}
            url = f"{self.BASE_URL}/{alias_tribunal}/processes/{numero_formatado}"
            
            # Fazer requisição
            response = self.session.get(url, timeout=10)
            
            # Verificar status
            if response.status_code == 200:
                dados = response.json()
                logger.info(f"✅ Processo encontrado via API CNJ: {numero_formatado}")
                dados['fonte'] = 'API CNJ (Consulta Pública)'
                # Armazenar no cache (TTL menor para dados da API)
                if cache:
                    cache.set(f"processo:{numero_formatado}", dados, cache_type='processo', ttl_seconds=1800)  # 30 min
                return dados
            elif response.status_code == 404:
                logger.info(f"Processo não encontrado na API CNJ: {numero_formatado}")
                return {"erro": "Processo não encontrado na base local (Kermartin) nem na API CNJ"}
            else:
                logger.error(f"Erro ao consultar API CNJ. Status: {response.status_code}")
                return {"erro": f"Erro na API CNJ (status {response.status_code})"}
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao consultar processo: {numero_processo}")
            # Tentar Kermartin mesmo com timeout
            try:
                from services.kermartin_service import kermartin_service
                logger.info("🔍 Timeout na API CNJ, tentando Kermartin...")
                processo_kermartin = kermartin_service.buscar_processo_por_numero(numero_processo)
                if processo_kermartin:
                    logger.info("✅ Processo encontrado no Kermartin!")
                    processo_kermartin['fonte'] = 'Kermartin (Base Local)'
                    return processo_kermartin
            except Exception as e2:
                logger.error(f"Erro ao buscar no Kermartin após timeout: {e2}")
            return {"erro": "Timeout na consulta. Tente novamente."}
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão ao consultar processo: {e}")
            # Tentar Kermartin mesmo com erro de conexão
            try:
                from services.kermartin_service import kermartin_service
                logger.info("🔍 Erro de conexão com API CNJ, tentando Kermartin...")
                processo_kermartin = kermartin_service.buscar_processo_por_numero(numero_processo)
                if processo_kermartin:
                    logger.info("✅ Processo encontrado no Kermartin!")
                    processo_kermartin['fonte'] = 'Kermartin (Base Local)'
                    return processo_kermartin
            except Exception as e2:
                logger.error(f"Erro ao buscar no Kermartin após erro de conexão: {e2}")
            return {"erro": "Erro de conexão com a API"}
        except Exception as e:
            logger.error(f"Erro inesperado ao consultar processo: {e}")
            # Tentar Kermartin mesmo com erro inesperado
            try:
                from services.kermartin_service import kermartin_service
                logger.info("🔍 Erro inesperado na API CNJ, tentando Kermartin...")
                processo_kermartin = kermartin_service.buscar_processo_por_numero(numero_processo)
                if processo_kermartin:
                    logger.info("✅ Processo encontrado no Kermartin!")
                    processo_kermartin['fonte'] = 'Kermartin (Base Local)'
                    return processo_kermartin
            except Exception as e2:
                logger.error(f"Erro ao buscar no Kermartin após erro inesperado: {e2}")
            return {"erro": "Erro inesperado"}
    
    def buscar_movimentacoes(self, numero_processo: str) -> Optional[List[Dict]]:
        """
        Busca movimentações de um processo
        
        Args:
            numero_processo: Número do processo
            
        Returns:
            Lista de movimentações ou None se erro
        """
        try:
            dados = self.consultar_processo(numero_processo)
            
            if not dados or "erro" in dados:
                return None
            
            # A estrutura exata depende da API
            # Geralmente vem em dados["movimentacoes"] ou similar
            movimentacoes = dados.get("movimentacoes", [])
            
            if isinstance(movimentacoes, list):
                return movimentacoes
            else:
                return []
                
        except Exception as e:
            logger.error(f"Erro ao buscar movimentações: {e}")
            return None
    
    def formatar_resposta_processo(self, dados: Dict) -> str:
        """
        Formata dados do processo para exibição no Telegram
        
        Args:
            dados: Dados retornados pela API ou Kermartin
            
        Returns:
            String formatada em Markdown
        """
        if "erro" in dados:
            return f"⚠️ **{dados['erro']}**\n\nTente verificar o número do processo."
        
        # Extrair informações (estrutura pode variar conforme fonte)
        numero = dados.get("numero", "N/A")
        fonte = dados.get("fonte", "API Pública do CNJ (DataJud)")
        
        # Processos do Kermartin podem ter estrutura diferente
        if "magistrado" in dados or fonte.startswith("Kermartin"):
            # Formato do Kermartin (julgado)
            classe = dados.get("classe", "Processo Judicial")
            assunto_texto = dados.get("assunto", dados.get("ementa", "N/A"))
            
            # Se a ementa for apenas o número do processo, tentar melhorar
            if assunto_texto == numero or assunto_texto == "N/A" or (isinstance(assunto_texto, str) and len(assunto_texto) < 10):
                assunto_texto = "Processo criminal (dados do julgado)" if "Criminal" in str(dados.get("vara", "")) else "Processo judicial (dados do julgado)"
            
            tribunal = dados.get("tribunal", "N/A")
            vara = dados.get("vara", "N/A")
            status = dados.get("status", "Julgado" if "julgado" in fonte.lower() else "Processo com julgado registrado")
            data_autuacao = dados.get("data_autuacao", dados.get("data", "N/A"))
            magistrado = dados.get("magistrado", "")
            promotor = dados.get("promotor", "")
            decisao = dados.get("decisao", "")
            confiabilidade = dados.get("confiabilidade", "")
            
            resposta = f"""⚖️ **Consulta de Processo**

📄 **Número:** `{numero}`
📋 **Classe:** {classe}
📝 **Assunto:** {assunto_texto}
🏛️ **Tribunal:** {tribunal}
⚖️ **Vara:** {vara}
📊 **Status:** {status}
📅 **Data do Julgado:** {data_autuacao}"""
            
            if magistrado and magistrado != "N/A":
                resposta += f"\n👨‍⚖️ **Magistrado Relator:** {magistrado}"
            
            if promotor and promotor != "N/A":
                resposta += f"\n👤 **Promotor:** {promotor}"
            
            if decisao and decisao != "N/A" and decisao != "Processo real" and len(decisao) > 5:
                resposta += f"\n\n📋 **Decisão:**\n{decisao}"
            elif decisao == "Processo real":
                resposta += "\n\n✅ Processo real documentado na base de conhecimento"
            
            if confiabilidade:
                conf_emoji = "🟢" if confiabilidade.lower() == "alta" else "🟡" if confiabilidade.lower() == "media" else "🔴"
                resposta += f"\n{conf_emoji} **Confiabilidade:** {confiabilidade.capitalize()}"
            
            resposta += f"\n\n💡 Dados fornecidos por: {fonte}"
        else:
            # Formato padrão da API CNJ
            classe = dados.get("classe", {}).get("nome", "N/A") if isinstance(dados.get("classe"), dict) else dados.get("classe", "N/A")
            assunto = dados.get("assunto", [])
            if isinstance(assunto, list) and assunto:
                assunto_texto = assunto[0].get("nome", "N/A") if isinstance(assunto[0], dict) else assunto[0]
            else:
                assunto_texto = dados.get("assunto", "N/A")
            
            tribunal = dados.get("tribunal", {}).get("nome", "N/A") if isinstance(dados.get("tribunal"), dict) else dados.get("tribunal", "N/A")
            vara = dados.get("vara", "N/A")
            status = dados.get("status", "N/A")
            data_autuacao = dados.get("data_autuacao", "N/A")
            
            # Buscar última movimentação
            movimentacoes = dados.get("movimentacoes", [])
            ultima_mov = "N/A"
            data_ultima = "N/A"
            
            if movimentacoes and isinstance(movimentacoes, list):
                try:
                    ultima = movimentacoes[-1]
                    if isinstance(ultima, dict):
                        ultima_mov = ultima.get("descricao", "N/A")
                        data_ultima = ultima.get("data", "N/A")
                except Exception:
                    pass
            
            resposta = f"""⚖️ **Consulta de Processo**

📄 **Número:** `{numero}`
📋 **Classe:** {classe}
📝 **Assunto:** {assunto_texto}
🏛️ **Tribunal:** {tribunal}
⚖️ **Vara:** {vara or 'N/A'}
📊 **Status:** {status}
📅 **Data de Autuação:** {data_autuacao}

📋 **Última Movimentação:**
📅 {data_ultima}
📝 {ultima_mov}

💡 Dados fornecidos por: {fonte}"""
        
        return resposta


# Instância global
cnj_service = CNJService()

