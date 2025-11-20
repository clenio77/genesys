"""
Configurações para o Bot WhatsApp Business
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações globais do Bot WhatsApp"""
    
    # Twilio WhatsApp API
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # openai, gemini
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://genesys:genesys@localhost:5432/genesys_db"
    )
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # App Configuration
    APP_NAME = "Genesys WhatsApp Bot"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8000))
    
    # Features
    ENABLE_AI_RESPONSES = True
    ENABLE_LEAD_QUALIFICATION = True
    ENABLE_ANALYTICS = True
    
    # Rate Limiting
    MAX_MESSAGES_PER_USER = 100
    RATE_LIMIT_WINDOW = 3600  # 1 hora
    
    # Templates
    DEFAULT_LANGUAGE = "pt-BR"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "whatsapp_bot.log"

