"""
Serviço de Guardrails para respostas da IA
Garante que o bot só responda o que foi perguntado e traga referências
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import unicodedata

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.utils.logger import bot_telegram_logger as logger


class GuardrailsService:
    """Serviço de guardrails para controlar respostas da IA"""
    
    def __init__(self) -> None:
        self.TEMAS_JURIDICOS_NORMALIZADOS = [
            self._normalize_text(tema) for tema in self.TEMAS_JURIDICOS
        ]
        self.TOPICOS_PROIBIDOS_NORMALIZADOS = [
            self._normalize_text(topico) for topico in self.TOPICOS_PROIBIDOS
        ]

    @staticmethod
    def _normalize_text(texto: str) -> str:
        if not texto:
            return ""
        texto = unicodedata.normalize("NFKD", texto)
        texto = texto.encode("ASCII", "ignore").decode("ASCII")
        return texto.lower()

    # Temas jurídicos válidos
    TEMAS_JURIDICOS = [
        'direito', 'jurídico', 'legal', 'processo', 'jurisprudência', 'decisão',
        'sentença', 'acórdão', 'tribunal', 'magistrado', 'promotor', 'advogado',
        'lei', 'código', 'constituição', 'penal', 'civil', 'trabalhista',
        'tributário', 'administrativo', 'constitucional', 'homicídio', 'roubo',
        'furto', 'danos morais', 'indenização', 'prazos', 'prazo processual',
        'comarca', 'vara', 'justiça', 'legislação', 'norma', 'decreto',
        'portaria', 'resolução', 'clt', 'cpc', 'cp', 'ctb', 'ctn',
        'adquirido', 'prescrição', 'decadência', 'direito adquirido'
    ]
    
    # Tópicos que NÃO devem ser respondidos
    TOPICOS_PROIBIDOS = [
        'receita médica', 'diagnóstico', 'medicamento', 'tratamento médico',
        'como fazer bomba', 'hackear', 'como roubar', 'drogas ilegais',
        'conteúdo adulto', 'apostas ilegais', 'jogos de azar'
    ]
    
    # Padrões de SQL Injection
    SQL_INJECTION_PATTERNS = [
        r"('|(\\')|(;)|(;)|(\\;)|(,)|(\))|(\())*(\s)*(union|select|insert|update|delete|drop|create|alter|exec|execute|script|declare|cast|convert)",
        r"(\s|^)(union|select|insert|update|delete|drop|create|alter|exec|execute|declare|cast|convert)(\s|$)",
        r"(\bor\b|\band\b)\s+\d+\s*=\s*\d+",
        r"(\bor\b|\band\b)\s+['\"]\s*=\s*['\"]",
        r"';?\s*(drop|delete|truncate|alter)",
        r"(\||\||&|&&)\s*(rm|cat|ls|pwd|whoami|id|uname)",
        r"(\/\*|\*\/|--|\#)",
    ]
    
    # Padrões de Code Injection (Python, JavaScript, etc)
    CODE_INJECTION_PATTERNS = [
        r"(__import__|eval|exec|compile|__builtins__|__globals__|__locals__)",
        r"(eval\(|exec\(|compile\(|__import__\()",
        r"(import\s+os|import\s+subprocess|import\s+sys)",
        r"(os\.system|os\.popen|subprocess\.call|subprocess\.Popen)",
        r"(<script|javascript:|onerror=|onload=|onclick=)",
        r"(\.py[^\w]|\.js[^\w]|\.sh[^\w]|\.bat[^\w]|\.exe[^\w])",
        r"(process\.env|require\(|global\[|window\[)",
    ]
    
    # Padrões de Command Injection (mais restritivos para evitar falsos positivos)
    COMMAND_INJECTION_PATTERNS = [
        # Caracteres de shell seguidos de comandos específicos (não apenas qualquer palavra)
        r"(\||\||&|&&|;|`|\$\(|\$\{)[\s]*(rm|del|format|mkfs|dd|cat|ls|pwd|whoami|id|uname|nc|netcat|wget|curl|ping|bash|sh|cmd|powershell)",
        # Comandos destrutivos específicos
        r"(rm\s+-rf|del\s+/|format\s+[a-z]:|mkfs|dd\s+if=)",
        # Comandos de sistema específicos (apenas se seguidos de paths suspeitos)
        r"(cat\s+[\w\/]+|ls\s+-la|pwd|whoami|id|uname)(\s|$|;|&|\||`)",
        # Comandos de rede seguidos de IPs ou URLs suspeitas
        r"(nc\s+|netcat|wget\s+|curl\s+|ping\s+)(\d+\.\d+\.\d+\.\d+|http|https|ftp)",
        # Shells explícitos
        r"(bash\s+|sh\s+|cmd\s+|powershell\s+)(-c|--command|/c)",
        # Variáveis de ambiente usadas para injection
        r"(\$\{IFS\}|\$\{PATH\})",
    ]
    
    # Padrões de Path Traversal
    PATH_TRAVERSAL_PATTERNS = [
        r"(\.\.\/|\.\.\\|\.\.\/\.\.\/|\.\.\\\.\.\\)",
        r"(\/etc\/|\/proc\/|\/sys\/|\/dev\/|\/usr\/|\/var\/)",
        r"(c:\\windows|c:\\system32|c:\\users)",
        r"(\.\.\/\.\.\/\.\.\/|\.\.\\\.\.\\\.\.\\)",
        r"(\/\.\.\/|\/\.\.\\|\\\.\.\/|\\\.\.\\)",
    ]
    
    # Padrões de NoSQL Injection
    NOSQL_INJECTION_PATTERNS = [
        r"(\$ne|\$gt|\$lt|\$gte|\$lte|\$in|\$nin|\$or|\$and|\$regex|\$where)",
        r"(\$ne|\$gt|\$lt|\$gte|\$lte|\$in|\$nin|\$or|\$and)(\s*:\s*|\s*\{)",
    ]
    
    # Padrões de LDAP Injection
    LDAP_INJECTION_PATTERNS = [
        r"(\*\)|\(\*|&\(|\|\(|!\()",
        r"(\%00|\x00|\\x00)",
    ]
    
    # Padrões suspeitos gerais
    SUSPICIOUS_PATTERNS = [
        r"(base64|hex|unicode|url.*encode)",
        # Detecta sequências hexadecimais suspeitas no formato literal \xHH
        r"(\\x[0-9a-fA-F]{2})",
        r"(<\?php|<\?=|\<%|<\?xml)",
        r"(perl\s+-e|ruby\s+-e|python\s+-c)",
    ]
    
    def detectar_ataques_seguranca(self, texto: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Detecta tentativas de ataques de segurança no texto
        
        Args:
            texto: Texto a ser analisado
            
        Returns:
            (tem_ataque, tipo_ataque, mensagem_erro)
        """
        texto_lower = texto.lower()
        texto_original = texto  # Manter original para análise de padrões case-sensitive
        
        # Verificar SQL Injection
        for pattern in self.SQL_INJECTION_PATTERNS:
            if re.search(pattern, texto_lower, re.IGNORECASE):
                logger.warning(f"Tentativa de SQL Injection detectada: {texto[:100]}")
                return True, "SQL_INJECTION", (
                    "⚠️ **Segurança:** Conteúdo suspeito detectado.\n\n"
                    "Não é possível processar essa solicitação por questões de segurança."
                )
        
        # Verificar Code Injection
        for pattern in self.CODE_INJECTION_PATTERNS:
            if re.search(pattern, texto_lower, re.IGNORECASE):
                logger.warning(f"Tentativa de Code Injection detectada: {texto[:100]}")
                return True, "CODE_INJECTION", (
                    "⚠️ **Segurança:** Tentativa de injeção de código detectada.\n\n"
                    "Não é possível processar essa solicitação por questões de segurança."
                )
        
        # Verificar Command Injection (com verificação de contexto jurídico)
        for pattern in self.COMMAND_INJECTION_PATTERNS:
            if re.search(pattern, texto_lower, re.IGNORECASE):
                # Verificar se é uma pergunta jurídica legítima que pode ter termos similares
                # Ex: "direito adquirido" não deve ser bloqueado
                temas_juridicos_no_texto = any(tema in texto_lower for tema in self.TEMAS_JURIDICOS)
                
                # Se contém tema jurídico e não tem caracteres suspeitos múltiplos, pode ser falso positivo
                caracteres_suspeitos = sum(1 for c in texto if c in ['|', '&', ';', '`', '$', '(', '{'])
                
                # Se tem tema jurídico e poucos caracteres suspeitos, provavelmente é pergunta legítima
                if temas_juridicos_no_texto and caracteres_suspeitos < 2:
                    logger.debug(f"Padrão de command injection detectado, mas pergunta parece jurídica legítima: {texto[:100]}")
                    continue  # Pular este padrão, pode ser falso positivo
                
                logger.warning(f"Tentativa de Command Injection detectada: {texto[:100]}")
                return True, "COMMAND_INJECTION", (
                    "⚠️ **Segurança:** Tentativa de injeção de comandos detectada.\n\n"
                    "Não é possível processar essa solicitação por questões de segurança."
                )
        
        # Verificar Path Traversal
        for pattern in self.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, texto_original, re.IGNORECASE):
                logger.warning(f"Tentativa de Path Traversal detectada: {texto[:100]}")
                return True, "PATH_TRAVERSAL", (
                    "⚠️ **Segurança:** Tentativa de acesso não autorizado detectada.\n\n"
                    "Não é possível processar essa solicitação por questões de segurança."
                )
        
        # Verificar NoSQL Injection
        for pattern in self.NOSQL_INJECTION_PATTERNS:
            if re.search(pattern, texto_lower, re.IGNORECASE):
                logger.warning(f"Tentativa de NoSQL Injection detectada: {texto[:100]}")
                return True, "NOSQL_INJECTION", (
                    "⚠️ **Segurança:** Tentativa de injeção NoSQL detectada.\n\n"
                    "Não é possível processar essa solicitação por questões de segurança."
                )
        
        # Verificar LDAP Injection
        for pattern in self.LDAP_INJECTION_PATTERNS:
            if re.search(pattern, texto_original, re.IGNORECASE):
                logger.warning(f"Tentativa de LDAP Injection detectada: {texto[:100]}")
                return True, "LDAP_INJECTION", (
                    "⚠️ **Segurança:** Tentativa de injeção LDAP detectada.\n\n"
                    "Não é possível processar essa solicitação por questões de segurança."
                )
        
        # Verificar padrões suspeitos gerais
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, texto_lower, re.IGNORECASE):
                logger.warning(f"Padrão suspeito detectado: {texto[:100]}")
                # Mais leniente com padrões suspeitos, apenas logar
                # Retornar True apenas se for muito suspeito
                if any(sus in texto_lower for sus in ['<?php', '<?xml', 'perl -e', 'ruby -e', 'python -c']):
                    return True, "SUSPICIOUS", (
                        "⚠️ **Segurança:** Conteúdo suspeito detectado.\n\n"
                        "Por favor, faça uma pergunta jurídica válida."
                    )
        
        return False, None, None
    
    def sanitizar_texto(self, texto: str) -> str:
        """
        Sanitiza texto removendo caracteres perigosos
        
        Args:
            texto: Texto a ser sanitizado
            
        Returns:
            Texto sanitizado
        """
        # Usar a função sanitize_text compartilhada primeiro (evita erros de escape)
        from shared.utils.text_sanitizer import sanitize_text
        try:
            texto = sanitize_text(texto)
        except Exception as e:
            logger.warning(f"Erro na sanitização compartilhada: {e}. Usando sanitização básica...")
            # Fallback: sanitização básica sem regex problemático
            try:
                # Converter para bytes e depois de volta para string (remove caracteres inválidos)
                texto_bytes = str(texto).encode('utf-8', errors='ignore')
                texto = texto_bytes.decode('utf-8', errors='ignore')
                # Remover caracteres de controle manualmente (sem regex)
                texto = ''.join(c for c in texto if ord(c) >= 32 or c in ['\n', '\r', '\t'])
            except Exception:
                texto = str(texto) if texto else ""
        
        # Limitar tamanho para evitar DoS
        if len(texto) > 10000:
            texto = texto[:10000] + "..."
            logger.warning("Texto truncado por exceder limite de tamanho")
        
        return texto
    
    def validar_pergunta(self, pergunta: str) -> Tuple[bool, Optional[str]]:
        """
        Valida se a pergunta é jurídica e apropriada
        
        Returns:
            (é_válida, mensagem_erro)
        """
        # PRIMEIRO: Verificar ataques de segurança
        tem_ataque, tipo_ataque, msg_erro = self.detectar_ataques_seguranca(pergunta)
        if tem_ataque:
            return False, msg_erro
        
        # Sanitizar texto antes de processar
        pergunta = self.sanitizar_texto(pergunta)
        
        pergunta_lower = pergunta.lower()
        pergunta_normalizada = self._normalize_text(pergunta_lower)
        
        # Verificar se contém tópicos proibidos
        for topico, topico_normalizado in zip(self.TOPICOS_PROIBIDOS, self.TOPICOS_PROIBIDOS_NORMALIZADOS):
            if topico in pergunta_lower or topico_normalizado in pergunta_normalizada:
                return False, "⚠️ Não posso ajudar com esse tipo de conteúdo. Por favor, faça uma pergunta jurídica."
        
        # Verificar se é uma pergunta jurídica
        contem_tema_juridico = any(
            tema in pergunta_lower or tema_normalizado in pergunta_normalizada
            for tema, tema_normalizado in zip(self.TEMAS_JURIDICOS, self.TEMAS_JURIDICOS_NORMALIZADOS)
        )
        
        # Se não tem tema jurídico claro, mas é uma pergunta simples sobre o bot, permitir
        perguntas_gerais_ok = [
            'ajuda', 'help', 'comandos', 'o que você faz', 'funcionalidades',
            'como usar', 'menu', 'iniciar', 'começar'
        ]
        
        pergunta_geral = any(
            p in pergunta_lower or self._normalize_text(p) in pergunta_normalizada
            for p in perguntas_gerais_ok
        )
        
        if not contem_tema_juridico and not pergunta_geral:
            return False, (
                "⚠️ Sou um assistente jurídico especializado.\n\n"
                "Por favor, faça uma pergunta sobre:\n"
                "• Direito brasileiro\n"
                "• Processos judiciais\n"
                "• Jurisprudência\n"
                "• Legislação\n"
                "• Prazos processuais\n\n"
                "💡 Use /help para ver comandos disponíveis."
            )
        
        return True, None
    
    def extrair_topicos_da_pergunta(self, pergunta: str) -> List[str]:
        """
        Extrai tópicos/chaves de busca da pergunta para buscar no Kermartin
        
        Returns:
            Lista de termos-chave para busca
        """
        topicos = []
        pergunta_lower = pergunta.lower()
        
        # Extrair termos jurídicos importantes
        termos_juridicos = [
            'homicídio', 'roubo', 'furto', 'tráfico', 'estelionato',
            'danos morais', 'indenização', 'desapropriação', 'despejo',
            'contrato', 'obrigação', 'responsabilidade', 'pena', 'prisão',
            'habeas corpus', 'mandado de segurança', 'ação', 'recurso',
            'apelação', 'agravo', 'embargos'
        ]
        
        for termo in termos_juridicos:
            if termo in pergunta_lower:
                topicos.append(termo)
        
        # Extrair nomes próprios (possíveis magistrados, promotores)
        palavras = pergunta.split()
        for palavra in palavras:
            if palavra[0].isupper() and len(palavra) > 3:
                topicos.append(palavra)
        
        # Extrair números de processo (formato CNJ)
        processos = re.findall(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', pergunta)
        topicos.extend(processos)
        
        return topicos
    
    def validar_resposta(self, resposta: str, pergunta: str) -> Tuple[bool, Optional[str]]:
        """
        Valida se a resposta está relacionada à pergunta e é apropriada
        
        Returns:
            (é_válida, resposta_corrigida)
        """
        # PRIMEIRO: Verificar ataques de segurança na resposta também
        tem_ataque, tipo_ataque, msg_erro = self.detectar_ataques_seguranca(resposta)
        if tem_ataque:
            logger.error(f"Resposta da IA contém ataque detectado: {tipo_ataque}")
            return False, (
                "⚠️ **Erro de Segurança:** A resposta gerada não pode ser exibida por questões de segurança.\n\n"
                "Por favor, reformule sua pergunta."
            )
        
        # Sanitizar resposta antes de processar
        resposta = self.sanitizar_texto(resposta)
        
        resposta_lower = resposta.lower()
        pergunta_lower = pergunta.lower()
        
        # Verificar se resposta contém tópicos proibidos
        for topico in self.TOPICOS_PROIBIDOS:
            if topico in resposta_lower:
                return False, "⚠️ Não posso fornecer informações sobre esse assunto."
        
        # Verificar se resposta parece estar respondendo a pergunta
        # (análise básica - pode ser melhorada)
        palavras_chave_pergunta = set(pergunta_lower.split())
        palavras_chave_resposta = set(resposta_lower.split())
        
        # Interseção mínima esperada
        palavras_comuns = palavras_chave_pergunta.intersection(palavras_chave_resposta)
        
        # Se não há palavras em comum e resposta é muito curta, pode estar errada
        if len(palavras_comuns) == 0 and len(resposta.split()) < 10:
            logger.warning("Resposta pode não estar relacionada à pergunta")
            # Não bloquear, apenas avisar
        
        return True, resposta
    
    def buscar_referencias_kermartin(self, topicos: List[str], limit: int = 5) -> List[Dict]:
        """
        Busca referências no Kermartin baseado nos tópicos extraídos
        
        Args:
            topicos: Lista de tópicos/chaves extraídas da pergunta
            limit: Número máximo de referências a retornar
            
        Returns:
            Lista de referências encontradas
        """
        referencias = []
        
        if not topicos:
            return referencias
        
        try:
            # Importar kermartin_service apenas quando necessário
            from services.kermartin_service import kermartin_service
            
            # Buscar processos RAG relacionados aos tópicos
            for topico in topicos[:3]:  # Limitar busca aos 3 primeiros tópicos
                try:
                    # Buscar por termos no RAG
                    filtro = {}
                    
                    # Se for número de processo, buscar diretamente
                    if re.match(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', topico):
                        processo = kermartin_service.buscar_processo_por_numero(topico)
                        if processo:
                            referencias.append({
                                'tipo': 'Processo',
                                'titulo': f"Processo {topico}",
                                'numero': topico,
                                'fonte': 'Kermartin',
                                'descricao': processo.get('assunto', '')
                            })
                        continue
                    
                    # Buscar na base RAG
                    processos_rag = kermartin_service.buscar_processos_rag(filtro)
                    
                    # Filtrar por tópico relevante
                    for processo in processos_rag[:limit]:
                        # Verificar se o processo contém o tópico
                        conteudo = str(processo.get('content', '') + ' ' + 
                                     str(processo.get('metadata_json', ''))).lower()
                        
                        if topico.lower() in conteudo:
                            numero = processo.get('processo_numero') or processo.get('numero')
                            referencias.append({
                                'tipo': 'Jurisprudência',
                                'titulo': processo.get('titulo', f"Processo {numero or 'N/A'}"),
                                'numero': numero,
                                'fonte': 'Kermartin RAG',
                                'descricao': processo.get('content', '')[:200] + '...' if processo.get('content') else ''
                            })
                            
                            if len(referencias) >= limit:
                                break
                
                except Exception as e:
                    logger.warning(f"Erro ao buscar referência para tópico '{topico}': {e}")
                    continue
            
            # Remover duplicatas (por número de processo)
            referencias_unicas = []
            numeros_vistos = set()
            
            for ref in referencias:
                numero = ref.get('numero')
                if numero and numero not in numeros_vistos:
                    referencias_unicas.append(ref)
                    numeros_vistos.add(numero)
                elif not numero:
                    referencias_unicas.append(ref)
            
            return referencias_unicas[:limit]
            
        except ImportError:
            logger.warning("KermartinService não disponível para buscar referências")
            return []
        except Exception as e:
            logger.error(f"Erro ao buscar referências no Kermartin: {e}")
            return []
    
    def formatar_resposta_com_referencias(self, resposta: str, referencias: List[Dict]) -> str:
        """
        Formata resposta incluindo referências do Kermartin
        
        Args:
            resposta: Resposta da IA
            referencias: Lista de referências encontradas no Kermartin
            
        Returns:
            Resposta formatada com referências
        """
        if not referencias:
            return resposta
        
        # Adicionar seção de referências
        resposta_formatada = resposta
        
        # Separador
        resposta_formatada += "\n\n" + "─" * 35 + "\n\n"
        resposta_formatada += "📚 **Referências:**\n\n"
        
        for i, ref in enumerate(referencias[:5], 1):  # Máximo 5 referências
            tipo = ref.get('tipo', 'Fonte')
            titulo = ref.get('titulo', ref.get('nome', 'N/A'))
            fonte = ref.get('fonte', 'Kermartin')
            
            resposta_formatada += f"**{i}.** {titulo}\n"
            resposta_formatada += f"   📌 Tipo: {tipo}\n"
            resposta_formatada += f"   📄 Fonte: {fonte}\n"
            
            # Adicionar link ou número se disponível
            if ref.get('numero'):
                resposta_formatada += f"   🔗 Processo: `{ref['numero']}`\n"
            if ref.get('url'):
                resposta_formatada += f"   🔗 Link: {ref['url']}\n"
            
            # Adicionar descrição se disponível
            if ref.get('descricao'):
                desc = ref['descricao'][:150] + '...' if len(ref['descricao']) > 150 else ref['descricao']
                resposta_formatada += f"   📝 {desc}\n"
            
            resposta_formatada += "\n"
        
        if len(referencias) > 5:
            resposta_formatada += f"\n... e mais {len(referencias) - 5} referência(s).\n"
        
        resposta_formatada += "\n💡 Dados coletados da base Kermartin"
        
        return resposta_formatada
    
    async def processar_com_guardrails(
        self, 
        pergunta: str, 
        resposta_ia: str,
        buscar_referencias: bool = True
    ) -> Tuple[str, List[Dict]]:
        """
        Processa pergunta e resposta com guardrails completos
        
        Args:
            pergunta: Pergunta do usuário
            resposta_ia: Resposta gerada pela IA
            buscar_referencias: Se deve buscar referências no Kermartin
            
        Returns:
            (resposta_final, referencias_encontradas)
        """
        # 0. Sanitizar entrada primeiro
        pergunta = self.sanitizar_texto(pergunta)
        
        # 0.5. Sanitizar resposta da IA ANTES de qualquer processamento (crítico!)
        # Isso previne erros de escape antes de validar_resposta
        try:
            resposta_ia = self.sanitizar_texto(resposta_ia)
        except (ValueError, SyntaxError) as e:
            error_msg = str(e).lower()
            if "incomplete escape" in error_msg or "\\x" in error_msg:
                logger.warning(f"Erro de escape ao sanitizar resposta_ia no guardrails: {e}")
                # Sanitização agressiva como fallback
                try:
                    resposta_ia_bytes = str(resposta_ia).encode('utf-8', errors='ignore')
                    resposta_ia = resposta_ia_bytes.decode('utf-8', errors='ignore')
                    resposta_ia = ''.join(c for c in resposta_ia if ord(c) >= 32 or c in ['\n', '\r', '\t'])
                except Exception:
                    resposta_ia = "Resposta não disponível devido a erro de processamento."
            else:
                raise
        
        # 1. Validar pergunta (inclui detecção de ataques)
        pergunta_valida, msg_erro = self.validar_pergunta(pergunta)
        if not pergunta_valida:
            logger.warning(f"Pergunta bloqueada: {pergunta[:50]}...")
            return msg_erro, []
        
        # 2. Validar resposta da IA (inclui detecção de ataques)
        try:
            resposta_valida, resposta_corrigida = self.validar_resposta(resposta_ia, pergunta)
        except (ValueError, SyntaxError) as e:
            error_msg = str(e).lower()
            if "incomplete escape" in error_msg or "\\x" in error_msg:
                logger.warning(f"Erro de escape ao validar resposta: {e}")
                # Usar resposta já sanitizada como resposta válida
                resposta_valida = True
                resposta_corrigida = resposta_ia
            else:
                raise
        if not resposta_valida:
            logger.error(f"Resposta da IA bloqueada por segurança")
            return resposta_corrigida, []
        
        resposta_final = resposta_corrigida
        referencias = []
        
        # 3. Buscar referências no Kermartin se solicitado
        if buscar_referencias:
            try:
                topicos = self.extrair_topicos_da_pergunta(pergunta)
                if topicos:
                    # Sanitizar tópicos antes de buscar
                    topicos_sanitizados = [self.sanitizar_texto(t) for t in topicos]
                    referencias = self.buscar_referencias_kermartin(topicos_sanitizados, limit=5)
                    
                    # Se encontrou referências, formatar resposta com elas
                    if referencias:
                        resposta_final = self.formatar_resposta_com_referencias(
                            resposta_final, 
                            referencias
                        )
            except Exception as e:
                logger.warning(f"Erro ao buscar referências: {e}")
                # Continuar sem referências se houver erro
        
        return resposta_final, referencias
    
    def adicionar_disclaimer_juridico(self, resposta: str) -> str:
        """
        Adiciona disclaimer jurídico padrão à resposta
        
        Args:
            resposta: Resposta original
            
        Returns:
            Resposta com disclaimer
        """
        disclaimer = (
            "\n\n" + "─" * 35 + "\n"
            "⚠️ **Aviso Legal:**\n"
            "Esta resposta é apenas informativa e não constitui consultoria jurídica.\n"
            "Sempre consulte um advogado para orientação específica ao seu caso."
        )
        
        # Verificar se já tem disclaimer para não duplicar
        if "aviso legal" not in resposta.lower() and "disclaimer" not in resposta.lower():
            resposta += disclaimer
        
        return resposta


# Instância global
guardrails_service = GuardrailsService()

