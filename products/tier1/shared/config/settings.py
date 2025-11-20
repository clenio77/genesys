"""
Configurações compartilhadas para todos os serviços Tier 1
"""

import os
from pathlib import Path
from typing import Optional

class Settings:
    """Configurações globais do sistema"""
    
    # Diretório base
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://genesys:genesys@localhost:5432/genesys_db"
    )
    
    # Redis
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        ""
    )
    
    # WhatsApp Business API
    WHATSAPP_ACCESS_TOKEN: str = os.getenv(
        "WHATSAPP_ACCESS_TOKEN",
        ""
    )
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv(
        "WHATSAPP_PHONE_NUMBER_ID",
        ""
    )
    WHATSAPP_VERIFY_TOKEN: str = os.getenv(
        "WHATSAPP_VERIFY_TOKEN",
        "genesys_verify_token"
    )
    
    # OpenAI/Gemini
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    
    # Email
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "genesys.log")
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    
    # Frontend URLs
    FRONTEND_URL: str = os.getenv(
        "FRONTEND_URL",
        "http://localhost:3000"
    )
    
    # Features
    ENABLE_TELEGRAM_BOT: bool = os.getenv("ENABLE_TELEGRAM_BOT", "true").lower() == "true"
    ENABLE_PRAZOS: bool = os.getenv("ENABLE_PRAZOS", "true").lower() == "true"
    ENABLE_ASSISTENTE: bool = os.getenv("ENABLE_ASSISTENTE", "true").lower() == "true"
    
    @classmethod
    def get_database_url(cls) -> str:
        """Retorna URL do banco de dados"""
        return cls.DATABASE_URL
    
    @classmethod
    def get_redis_url(cls) -> str:
        """Retorna URL do Redis"""
        return cls.REDIS_URL

# Instância global
settings = Settings()

