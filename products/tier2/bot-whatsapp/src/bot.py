"""
Bot WhatsApp Business Principal
Integra Twilio, LLM e lógica de conversação
"""

import sys
from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

# Adiciona paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "tier1" / "shared"))

from shared.middleware.security import configure_cors_seguro, add_security_middleware
from shared.middleware.rate_limit import rate_limit_dependency
from shared.middleware.cache import init_cache, cached_response
from shared.utils.logger import setup_logger

from src.config import Config
from src.services.message_handler import MessageHandler
from src.services.nlp_processor import NLPProcessor
from src.services.dialog_manager import DialogManager
from src.services.response_generator import ResponseGenerator

# Setup
logger = setup_logger("whatsapp_bot", "whatsapp_bot.log")
app = FastAPI(title="Genesys WhatsApp Bot", version="1.0.0")

# Configure security
configure_cors_seguro(
    app,
    allowed_origins=[
        "https://genesys.com.br",
        "https://whatsapp.genesys.com.br",
        "http://localhost:3000"
    ]
)
add_security_middleware(app)

# Initialize cache
init_cache(Config.REDIS_URL)

# Initialize Twilio Client
twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

# Initialize services
nlp_processor = NLPProcessor()
dialog_manager = DialogManager()
response_generator = ResponseGenerator()
message_handler = MessageHandler(
    nlp_processor,
    dialog_manager,
    response_generator,
    twilio_client
)


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "service": "Genesys WhatsApp Bot",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy"}


@app.post("/webhook")
async def webhook(
    request: Request,
    _ = Depends(rate_limit_dependency(max_requests=100, window_seconds=60))
):
    """
    Webhook principal do Twilio para receber mensagens WhatsApp
    """
    form_data = await request.form()
    
    incoming_message = form_data.get('Body', '')
    sender_phone = form_data.get('From', '')
    
    logger.info(f"Received message from {sender_phone}: {incoming_message}")
    
    try:
        # Processar mensagem
        response_text = await message_handler.process_message(
            message=incoming_message,
            sender_phone=sender_phone
        )
        
        # Criar resposta TwiML
        resp = MessagingResponse()
        resp.message(response_text)
        
        return Response(content=str(resp), media_type="application/xml")
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        resp = MessagingResponse()
        resp.message("Desculpe, ocorreu um erro. Tente novamente.")
        return Response(content=str(resp), media_type="application/xml")


@app.post("/api/message/send")
async def send_message(
    phone: str,
    message: str,
    _ = Depends(rate_limit_dependency())
):
    """Enviar mensagem via API"""
    
    try:
        message_handler.send_message(
            to_phone=phone,
            message=message
        )
        return {"status": "success"}
    
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise


@app.get("/api/stats")
@cached_response(ttl=300)  # Cache por 5 minutos
async def get_stats(request: Request = None):
    """Estatísticas do bot"""
    
    return {
        "total_conversations": 0,  # TODO: implementar
        "active_users": 0,
        "total_messages": 0,
        "avg_response_time": 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=Config.PORT)

