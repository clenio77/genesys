"""
Configurações para Dashboard Analítico Jurídico
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações globais do Dashboard"""
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://genesys:genesys@localhost:5432/genesys_db"
    )
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # App Configuration
    APP_NAME = "Genesys Analytics Dashboard"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8002))
    
    # Features
    ENABLE_REAL_TIME = True
    ENABLE_EXPORTS = True
    ENABLE_ALERTS = True
    
    # Time Windows
    TODAY = "today"
    WEEK = "7d"
    MONTH = "30d"
    QUARTER = "90d"
    YEAR = "365d"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "dashboard_analytics.log"

