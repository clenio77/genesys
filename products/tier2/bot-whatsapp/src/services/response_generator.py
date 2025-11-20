"""
Response Generator - Gera respostas com LLM
"""

import os
from typing import Optional
from src.config import Config


class ResponseGenerator:
    """Gera respostas inteligentes usando LLM"""
    
    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.fallback_enabled = True
        
        # Templates de resposta
        self.templates = {
            'greeting': [
                "Olá! 👋 Bem-vindo à *Genesys Tecnologia*!",
                "Como posso ajudá-lo hoje?"
            ],
            'help': [
                "Estou aqui para ajudar! 💼",
                "",
                "📋 *Opções disponíveis:*",
                "• /ajuda - Ver este menu",
                "• /consultar - Consultar jurisprudência",
                "• /prazos - Verificar prazos processuais",
                "• /agendar - Agendar consulta",
                "• /contato - Informações de contato",
                "",
                "Como posso ajudá-lo?"
            ],
            'not_understood': [
                "Desculpe, não entendi. 😅",
                "",
                "Tente uma das opções:",
                "• Digite 'ajuda' para ver opções",
                "• 'consultar' para buscar juris",
                "• 'prazos' para prazos processuais",
                "",
                "Como posso ajudá-lo?"
            ]
        }
    
    async def generate_response(self, intent: str, context: dict, message: str = "") -> str:
        """
        Gera resposta baseada na intenção e contexto
        
        Args:
            intent: Intenção detectada
            context: Contexto da conversa
            message: Mensagem original
        
        Returns:
            Resposta gerada
        """
        # Respostas simples sem LLM para MVP
        if intent == 'saudacao':
            return "\n".join(self.templates['greeting'])
        
        if intent == 'ajuda':
            return "\n".join(self.templates['help'])
        
        if intent == 'contato':
            return self._generate_contact_response()
        
        if intent == 'agendamento':
            return self._generate_scheduling_response()
        
        if intent == 'consulta':
            return self._generate_consultation_response(message)
        
        if intent == 'prazo':
            return self._generate_prazo_response()
        
        # Fallback
        return "\n".join(self.templates['not_understood'])
    
    def _generate_contact_response(self) -> str:
        """Gera resposta de contato"""
        return (
            "📞 *Informações de Contato*\n\n"
            "🏢 Genesys Tecnologia\n"
            "🌐 Website: genesys.com.br\n"
            "📧 Email: contato@genesys.com.br\n"
            "📱 WhatsApp: +55 34 99826-4603\n"
            "📍 Endereço: Uberlândia, MG\n\n"
            "Como posso ajudá-lo mais?"
        )
    
    def _generate_scheduling_response(self) -> str:
        """Gera resposta de agendamento"""
        return (
            "📅 *Agendamento de Consulta*\n\n"
            "Para agendar uma consulta, preciso de algumas informações:\n\n"
            "1️⃣ Nome completo\n"
            "2️⃣ Tipo de serviço desejado\n"
            "3️⃣ Data e horário preferidos\n\n"
            "Digite 'voltar' para cancelar.\n\n"
            "Qual seu nome?"
        )
    
    def _generate_consultation_response(self, message: str) -> str:
        """Gera resposta de consulta jurídica"""
        return (
            "⚖️ *Consulta Jurídica*\n\n"
            "Para consultar jurisprudência, preciso saber:\n\n"
            "1️⃣ Area do direito (civil, trabalhista, criminal, etc)\n"
            "2️⃣ Palavras-chave ou termos específicos\n\n"
            "Digite 'exemplo: Trabalhista demissão por justa causa'\n\n"
            "Ou digite 'voltar' para cancelar."
        )
    
    def _generate_prazo_response(self) -> str:
        """Gera resposta sobre prazos"""
        return (
            "📆 *Prazos Processuais*\n\n"
            "Para verificar prazos, preciso do número do processo.\n\n"
            "Digite o número do processo ou digite 'voltar' para cancelar."
        )
    
    async def generate_ai_response(self, prompt: str) -> Optional[str]:
        """
        Gera resposta usando LLM (OpenAI/Gemini)
        
        Args:
            prompt: Prompt para o LLM
        
        Returns:
            Resposta gerada ou None
        """
        if not Config.ENABLE_AI_RESPONSES:
            return None
        
        try:
            if self.provider == "openai" and Config.OPENAI_API_KEY:
                return await self._generate_openai_response(prompt)
            
            if self.provider == "gemini" and Config.GEMINI_API_KEY:
                return await self._generate_gemini_response(prompt)
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return None
        
        return None
    
    async def _generate_openai_response(self, prompt: str) -> Optional[str]:
        """Gera resposta usando OpenAI"""
        try:
            import openai
            openai.api_key = Config.OPENAI_API_KEY
            
            response = await openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente jurídico profissional da Genesys Tecnologia."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            
            return response.choices[0].message.content
        
        except Exception:
            return None
    
    async def _generate_gemini_response(self, prompt: str) -> Optional[str]:
        """Gera resposta usando Google Gemini"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            
            model = genai.GenerativeModel('gemini-pro')
            response = await model.generate_content(prompt)
            
            return response.text
        
        except Exception:
            return None

