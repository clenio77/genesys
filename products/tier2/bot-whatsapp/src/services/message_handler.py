"""
Message Handler - Processador principal de mensagens
"""

from typing import Optional
from twilio.rest import Client
from datetime import datetime

from src.services.nlp_processor import NLPProcessor
from src.services.dialog_manager import DialogManager
from src.services.response_generator import ResponseGenerator


class MessageHandler:
    """Handle incoming WhatsApp messages"""
    
    def __init__(
        self,
        nlp_processor: NLPProcessor,
        dialog_manager: DialogManager,
        response_generator: ResponseGenerator,
        twilio_client: Client
    ):
        self.nlp_processor = nlp_processor
        self.dialog_manager = dialog_manager
        self.response_generator = response_generator
        self.twilio_client = twilio_client
    
    async def process_message(self, message: str, sender_phone: str) -> str:
        """
        Processa uma mensagem recebida
        
        Args:
            message: Conteúdo da mensagem
            sender_phone: Número do remetente
        
        Returns:
            Resposta a ser enviada
        """
        # Adicionar ao histórico
        self.dialog_manager.add_message_to_history(sender_phone, message, from_user=True)
        
        # Detectar intenção
        intent_obj = self.nlp_processor.detect_intent(message)
        intent = intent_obj.name
        
        # Obter contexto
        context = self.dialog_manager.get_or_create_conversation(sender_phone)
        
        # Gerar resposta
        response = await self.response_generator.generate_response(
            intent=intent,
            context=context.context,
            message=message
        )
        
        # Adicionar resposta ao histórico
        self.dialog_manager.add_message_to_history(sender_phone, response, from_user=False)
        
        return response
    
    def send_message(self, to_phone: str, message: str):
        """
        Envia mensagem via Twilio
        
        Args:
            to_phone: Número de destino
            message: Mensagem a enviar
        """
        try:
            from src.config import Config
            
            self.twilio_client.messages.create(
                from_=f"whatsapp:{Config.TWILIO_WHATSAPP_NUMBER}",
                body=message,
                to=f"whatsapp:{to_phone}"
            )
        
        except Exception as e:
            print(f"Error sending message: {e}")
            raise

