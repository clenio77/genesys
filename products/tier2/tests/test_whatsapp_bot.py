"""
Testes unitários para Bot WhatsApp Business
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

# Mock imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestNLPProcessor:
    """Testes para NLP Processor"""
    
    def test_tokenize(self):
        """Testa tokenização de texto"""
        from bot_whatsapp.src.services.nlp_processor import NLPProcessor
        
        processor = NLPProcessor()
        text = "Oi, como posso consultar jurisprudência?"
        tokens = processor.tokenize(text)
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert "oi" not in tokens or "oi" not in processor.stop_words
    
    def test_detect_intent_saudacao(self):
        """Testa detecção de intenção de saudação"""
        from bot_whatsapp.src.services.nlp_processor import NLPProcessor
        
        processor = NLPProcessor()
        intent = processor.detect_intent("Olá, bom dia!")
        
        assert intent.name == "saudacao"
        assert intent.confidence > 0
    
    def test_detect_intent_ajuda(self):
        """Testa detecção de intenção de ajuda"""
        from bot_whatsapp.src.services.nlp_processor import NLPProcessor
        
        processor = NLPProcessor()
        intent = processor.detect_intent("Preciso de ajuda")
        
        assert intent.name == "ajuda"
        assert intent.confidence > 0
    
    def test_detect_intent_consulta(self):
        """Testa detecção de intenção de consulta"""
        from bot_whatsapp.src.services.nlp_processor import NLPProcessor
        
        processor = NLPProcessor()
        intent = processor.detect_intent("Quero consultar jurisprudência")
        
        assert intent.name == "consulta"
        assert intent.confidence > 0
    
    def test_analyze_sentiment_positive(self):
        """Testa análise de sentimento positivo"""
        from bot_whatsapp.src.services.nlp_processor import NLPProcessor, Sentiment
        
        processor = NLPProcessor()
        sentiment = processor.analyze_sentiment("Excelente atendimento, obrigado!")
        
        assert sentiment.label in ["positive", "neutral"]
        assert isinstance(sentiment, Sentiment)
    
    def test_extract_entities_email(self):
        """Testa extração de email"""
        from bot_whatsapp.src.services.nlp_processor import NLPProcessor
        
        processor = NLPProcessor()
        entities = processor.extract_entities("Meu email é teste@example.com")
        
        assert "email" in entities
        assert entities["email"] == "teste@example.com"


class TestDialogManager:
    """Testes para Dialog Manager"""
    
    def test_get_or_create_conversation(self):
        """Testa criação de conversa"""
        from bot_whatsapp.src.services.dialog_manager import DialogManager, Conversation
        
        manager = DialogManager()
        phone = "+5511999999999"
        
        conv = manager.get_or_create_conversation(phone)
        
        assert isinstance(conv, Conversation)
        assert conv.phone == phone
        assert "step" in conv.context
    
    def test_add_message_to_history(self):
        """Testa adição de mensagem ao histórico"""
        from bot_whatsapp.src.services.dialog_manager import DialogManager
        
        manager = DialogManager()
        phone = "+5511999999999"
        
        manager.add_message_to_history(phone, "Oi", from_user=True)
        manager.add_message_to_history(phone, "Olá!", from_user=False)
        
        conv = manager.get_or_create_conversation(phone)
        assert len(conv.history) == 2
        assert conv.history[0]["from_user"] == True
        assert conv.history[1]["from_user"] == False
    
    def test_set_and_get_context_data(self):
        """Testa definir e obter dados de contexto"""
        from bot_whatsapp.src.services.dialog_manager import DialogManager
        
        manager = DialogManager()
        phone = "+5511999999999"
        
        manager.set_context_data(phone, "nome", "João")
        value = manager.get_context_data(phone, "nome")
        
        assert value == "João"
    
    def test_set_and_get_step(self):
        """Testa definir e obter step"""
        from bot_whatsapp.src.services.dialog_manager import DialogManager
        
        manager = DialogManager()
        phone = "+5511999999999"
        
        manager.set_step(phone, "agendamento")
        step = manager.get_step(phone)
        
        assert step == "agendamento"


class TestResponseGenerator:
    """Testes para Response Generator"""
    
    def test_generate_response_greeting(self):
        """Testa geração de resposta para saudação"""
        from bot_whatsapp.src.services.response_generator import ResponseGenerator
        
        generator = ResponseGenerator()
        response = await generator.generate_response("saudacao", {})
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_generate_response_help(self):
        """Testa geração de resposta para ajuda"""
        from bot_whatsapp.src.services.response_generator import ResponseGenerator
        
        generator = ResponseGenerator()
        response = await generator.generate_response("ajuda", {})
        
        assert isinstance(response, str)
        assert "ajuda" in response.lower() or "opções" in response.lower()
    
    def test_generate_contact_response(self):
        """Testa geração de resposta de contato"""
        from bot_whatsapp.src.services.response_generator import ResponseGenerator
        
        generator = ResponseGenerator()
        response = generator._generate_contact_response()
        
        assert "contato" in response.lower() or "genesys" in response.lower()
    
    def test_generate_scheduling_response(self):
        """Testa geração de resposta de agendamento"""
        from bot_whatsapp.src.services.response_generator import ResponseGenerator
        
        generator = ResponseGenerator()
        response = generator._generate_scheduling_response()
        
        assert "agendamento" in response.lower() or "consulta" in response.lower()


class TestMessageHandler:
    """Testes para Message Handler"""
    
    def test_process_message(self):
        """Testa processamento de mensagem"""
        from bot_whatsapp.src.services.message_handler import MessageHandler
        from bot_whatsapp.src.services.nlp_processor import NLPProcessor
        from bot_whatsapp.src.services.dialog_manager import DialogManager
        from bot_whatsapp.src.services.response_generator import ResponseGenerator
        
        nlp = NLPProcessor()
        dialog = DialogManager()
        response_gen = ResponseGenerator()
        handler = MessageHandler(nlp, dialog, response_gen, Mock())
        
        response = await handler.process_message("Olá", "+5511999999999")
        
        assert isinstance(response, str)
        assert len(response) > 0


@pytest.mark.asyncio
class TestAsyncFeatures:
    """Testes assíncronos"""
    
    async def test_async_response_generation(self):
        """Testa geração assíncrona de resposta"""
        from bot_whatsapp.src.services.response_generator import ResponseGenerator
        
        generator = ResponseGenerator()
        response = await generator.generate_response("saudacao", {})
        
        assert isinstance(response, str)

