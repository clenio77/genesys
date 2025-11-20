"""
Serviço de IA para processar mensagens e gerar respostas
"""

import sys
from pathlib import Path
from typing import Optional, Dict, List
from abc import ABC, abstractmethod

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.config.settings import settings
from shared.utils.logger import bot_telegram_logger as logger
from services.guardrails_service import guardrails_service


class AIProvider(ABC):
    """Interface para provedores de IA"""
    
    @abstractmethod
    async def generate_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Gera resposta para uma mensagem"""
        pass


class OpenAIProvider(AIProvider):
    """Provedor OpenAI GPT"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            logger.warning("OPENAI_API_KEY não configurado")
    
    async def generate_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Gera resposta usando OpenAI"""
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.api_key)
            
            system_prompt = """Você é um assistente jurídico especializado da Genesys Tecnologia.
            Forneça respostas precisas, educadas e profissionais sobre questões jurídicas brasileiras.
            Se não tiver certeza, admita e recomende consultar um advogado.
            Seja conciso e objetivo nas respostas."""
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
            
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            resposta_texto = response.choices[0].message.content or ""
            
            # Sanitizar IMEDIATAMENTE após capturar do OpenAI
            from shared.utils.text_sanitizer import sanitize_text
            resposta_texto = sanitize_text(resposta_texto)
            
            return resposta_texto
            
        except Exception as e:
            logger.error(f"Erro ao chamar OpenAI: {e}")
            return self._fallback_response(message)
    
    def _fallback_response(self, message: str) -> str:
        """Resposta fallback quando OpenAI falha"""
        return "⚠️ No momento estou tendo dificuldades técnicas. Por favor, tente novamente ou use os comandos disponíveis (/help)."


class GeminiProvider(AIProvider):
    """Provedor Google Gemini"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY não configurado")
    
    def _safe_get_response_text(self, response) -> str:
        """
        Captura texto da resposta do Gemini de forma ULTRA SEGURA
        Evita erros de escape antes da sanitização usando múltiplas estratégias
        
        CRÍTICO: O erro pode ocorrer ao acessar response.text se o texto contém escapes inválidos.
        Esta função usa métodos que não dependem de acesso direto à propriedade.
        """
        from shared.utils.text_sanitizer import sanitize_text
        
        # Método 1: Tentar acessar via parts primeiro (mais seguro)
        try:
            if hasattr(response, 'parts') and response.parts:
                text_parts = []
                for part in response.parts:
                    if hasattr(part, 'text'):
                        try:
                            # Tentar acessar part.text de forma segura
                            part_text = part.text
                            # Converter para bytes imediatamente para evitar interpretação de escapes
                            part_bytes = str(part_text).encode('utf-8', errors='ignore')
                            part_text_safe = part_bytes.decode('utf-8', errors='ignore')
                            text_parts.append(part_text_safe)
                        except (ValueError, SyntaxError) as e:
                            error_msg = str(e).lower()
                            if "incomplete escape" in error_msg or "\\x" in error_msg:
                                logger.warning(f"Erro de escape em part.text, ignorando esta parte")
                                continue
                            else:
                                raise
                if text_parts:
                    combined_text = ''.join(text_parts)
                    return sanitize_text(combined_text)
        except Exception as e:
            logger.warning(f"Erro ao acessar parts (método 1): {e}")
        
        # Método 2: Usar object.__getattribute__ para acessar sem propriedade
        try:
            if hasattr(response, '__dict__'):
                # Tentar pegar o texto diretamente do dict sem usar propriedade
                response_dict = object.__getattribute__(response, '__dict__')
                if 'text' in response_dict:
                    raw_text = response_dict['text']
                    # Converter para bytes imediatamente
                    raw_bytes = str(raw_text).encode('utf-8', errors='ignore')
                    raw_text_safe = raw_bytes.decode('utf-8', errors='ignore')
                    return sanitize_text(raw_text_safe)
        except Exception as e:
            logger.warning(f"Erro ao acessar __dict__ (método 2): {e}")
        
        # Método 3: Tentar acessar diretamente MAS com tratamento de erro
        try:
            raw_text = response.text
            # Se chegou aqui, conseguiu acessar - converter para bytes IMEDIATAMENTE
            raw_bytes = str(raw_text).encode('utf-8', errors='ignore')
            raw_text_safe = raw_bytes.decode('utf-8', errors='ignore')
            return sanitize_text(raw_text_safe)
        except (ValueError, SyntaxError) as e:
            error_msg = str(e).lower()
            if "incomplete escape" in error_msg or "\\x" in error_msg:
                logger.warning(f"Erro de escape ao acessar response.text diretamente: {e}")
                # Continuar para métodos alternativos
            else:
                raise
        
        # Método 4: Usar getattr com tratamento de erro
        try:
            raw_text = getattr(response, 'text', None)
            if raw_text is not None:
                # Converter para bytes imediatamente
                raw_bytes = str(raw_text).encode('utf-8', errors='ignore')
                raw_text_safe = raw_bytes.decode('utf-8', errors='ignore')
                return sanitize_text(raw_text_safe)
        except (ValueError, SyntaxError) as e:
            error_msg = str(e).lower()
            if "incomplete escape" in error_msg or "\\x" in error_msg:
                logger.warning(f"Erro de escape ao usar getattr (método 4): {e}")
            else:
                raise
        
        # Método 5: Último recurso - usar repr() do objeto
        try:
            # Converter o objeto response para string usando método seguro
            raw_str = str(response)
            # Converter para bytes e depois de volta (remove escapes inválidos)
            raw_bytes = raw_str.encode('utf-8', errors='ignore')
            raw_text = raw_bytes.decode('utf-8', errors='ignore')
            return sanitize_text(raw_text)
        except Exception as e:
            logger.warning(f"Erro ao converter response (método 5): {e}")
        
        # Fallback final: retornar string vazia sanitizada
        logger.error("Todos os métodos de captura falharam, retornando string vazia")
        return sanitize_text("")
    
    async def generate_response(self, message: str, context: Optional[Dict] = None) -> str:
        """Gera resposta usando Google Gemini"""
        try:
            import google.generativeai as genai
            from shared.utils.text_sanitizer import sanitize_text
            
            genai.configure(api_key=self.api_key)
            
            system_instruction = """Você é um assistente jurídico especializado da Genesys Tecnologia.
            Forneça respostas precisas, educadas e profissionais sobre questões jurídicas brasileiras.
            Se não tiver certeza, admita e recomende consultar um advogado.
            Seja conciso e objetivo nas respostas."""
            
            model = genai.GenerativeModel(
                'gemini-2.5-flash',
                system_instruction=system_instruction
            )
            
            response = model.generate_content(message)
            
            # Capturar resposta usando método ultra-seguro
            resposta_texto = self._safe_get_response_text(response)
            
            # Sanitização adicional (redundante, mas garante segurança total)
            resposta_texto = sanitize_text(resposta_texto)
            
            return resposta_texto
            
        except Exception as e:
            logger.error(f"Erro ao chamar Gemini: {e}")
            import traceback
            logger.debug(f"Traceback: {traceback.format_exc()}")
            return self._fallback_response(message)
    
    def _fallback_response(self, message: str) -> str:
        """Resposta fallback quando Gemini falha"""
        return "⚠️ No momento estou tendo dificuldades técnicas. Por favor, tente novamente ou use os comandos disponíveis (/help)."


class AIService:
    """Serviço principal de IA para o bot"""
    
    def __init__(self):
        # Priorizar Gemini (mais barato), fallback para OpenAI
        if settings.GEMINI_API_KEY:
            self.provider = GeminiProvider()
            logger.info("Usando Google Gemini como provedor de IA")
        elif settings.OPENAI_API_KEY:
            self.provider = OpenAIProvider()
            logger.info("Usando OpenAI como provedor de IA")
        else:
            self.provider = None
            logger.warning("Nenhum provedor de IA configurado")
    
    async def process_message(
        self, 
        message: str, 
        context: Optional[Dict] = None,
        usar_guardrails: bool = True,
        buscar_referencias: bool = True
    ) -> str:
        """
        Processa uma mensagem e retorna resposta gerada por IA com guardrails
        
        Args:
            message: Mensagem do usuário
            context: Contexto adicional (opcional)
            usar_guardrails: Se deve aplicar guardrails (validação, referências)
            buscar_referencias: Se deve buscar referências no Kermartin
        
        Returns:
            Resposta gerada pela IA (com guardrails aplicados)
        """
        # Validar pergunta com guardrails ANTES de processar
        if usar_guardrails:
            pergunta_valida, msg_erro = guardrails_service.validar_pergunta(message)
            if not pergunta_valida:
                logger.info(f"Pergunta bloqueada pelos guardrails: {message[:50]}...")
                return msg_erro
        
        if not self.provider:
            resposta = self._default_response(message)
        else:
            try:
                # Gerar resposta da IA
                # A sanitização já acontece dentro do provider (Gemini/OpenAI)
                resposta_ia = await self.provider.generate_response(message, context)
                logger.info(f"IA processou mensagem: {message[:50]}...")
                
                # Sanitização adicional (redundante, mas garante segurança)
                if resposta_ia:
                    try:
                        from shared.utils.text_sanitizer import sanitize_text
                        resposta_ia = sanitize_text(resposta_ia)
                    except (ValueError, SyntaxError) as sanitize_error:
                        error_msg = str(sanitize_error).lower()
                        if "incomplete escape" in error_msg or "\\x" in error_msg:
                            logger.warning(f"Erro de escape ao sanitizar resposta da IA: {sanitize_error}")
                            # Sanitização agressiva como fallback
                            resposta_ia_bytes = str(resposta_ia).encode('utf-8', errors='ignore')
                            resposta_ia = resposta_ia_bytes.decode('utf-8', errors='ignore')
                            resposta_ia = ''.join(c for c in resposta_ia if ord(c) >= 32 or c in ['\n', '\r', '\t'])
                        else:
                            raise
                
                # Aplicar guardrails na resposta com tratamento de erro
                if usar_guardrails:
                    try:
                        resposta, referencias = await guardrails_service.processar_com_guardrails(
                            pergunta=message,
                            resposta_ia=resposta_ia,
                            buscar_referencias=buscar_referencias
                        )
                        
                        # Adicionar disclaimer jurídico
                        resposta = guardrails_service.adicionar_disclaimer_juridico(resposta)
                        
                        logger.info(f"Guardrails aplicados. Referências encontradas: {len(referencias)}")
                    except (ValueError, SyntaxError) as guardrails_error:
                        error_msg = str(guardrails_error).lower()
                        if "incomplete escape" in error_msg or "\\x" in error_msg:
                            logger.warning(f"Erro de escape ao aplicar guardrails: {guardrails_error}")
                            # Usar resposta da IA diretamente sem guardrails
                            resposta = resposta_ia
                        else:
                            raise
                else:
                    resposta = resposta_ia
                
                return resposta
                
            except (ValueError, SyntaxError) as e:
                error_msg = str(e).lower()
                if "incomplete escape" in error_msg or "\\x" in error_msg:
                    logger.error(f"Erro de escape ao processar mensagem com IA: {e}")
                    import traceback
                    logger.debug(f"Traceback: {traceback.format_exc()}")
                    resposta = self._default_response(message)
                else:
                    raise
            except Exception as e:
                logger.error(f"Erro ao processar mensagem com IA: {e}")
                import traceback
                logger.debug(f"Traceback: {traceback.format_exc()}")
                resposta = self._default_response(message)
        
        # Adicionar disclaimer mesmo para respostas padrão
        if usar_guardrails:
            resposta = guardrails_service.adicionar_disclaimer_juridico(resposta)
        
        return resposta
    
    def _default_response(self, message: str) -> str:
        """Resposta padrão quando não há IA disponível"""
        # Respostas inteligentes básicas sem IA
        message_lower = message.lower()
        
        if any(p in message_lower for p in ['jurisprudência', 'decisão', 'acórdão', 'precedente']):
            return "🔍 **Busca de Jurisprudência**\n\nEstou configurando a busca inteligente de jurisprudência. Use o comando /buscar quando estiver pronto para usar essa funcionalidade!"
        
        elif any(p in message_lower for p in ['prazo', 'vencimento', 'processo']):
            return "📅 **Prazos Processuais**\n\nUse o comando /prazos para ver seus prazos pendentes ou /alerta para configurar notificações automáticas!"
        
        elif any(p in message_lower for p in ['contato', 'suporte', 'ajuda']):
            return "💬 **Contato Genesys**\n\n📧 Email: contato@genesys-tecnologia.com.br\n📱 WhatsApp: +55 34 99826-4603\n🌐 Site: https://genesys-tecnologia.com.br"
        
        else:
            return "🤖 **Genesys IA Jurídica**\n\nPara ativar respostas inteligentes com IA, configure sua API key:\n• OPENAI_API_KEY ou\n• GEMINI_API_KEY\n\nUse /help para ver comandos disponíveis!"


# Instância global do serviço de IA
ai_service = AIService()

