"""
Configurações para OCR & Processamento de Documentos
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações globais do OCR & Processamento"""
    
    # Google Vision API
    GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY", "")
    GOOGLE_VISION_PROJECT_ID = os.getenv("GOOGLE_VISION_PROJECT_ID", "")
    
    # OpenAI GPT-4
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://genesys:genesys@localhost:5432/genesys_db"
    )
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")
    
    # App Configuration
    APP_NAME = "Genesys OCR & Processamento"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8001))
    
    # File Storage
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 50 * 1024 * 1024))  # 50MB
    ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".tif"}
    
    # OCR Configuration
    OCR_CONFIDENCE_THRESHOLD = float(os.getenv("OCR_CONFIDENCE_THRESHOLD", "0.85"))
    OCR_LANGUAGES = os.getenv("OCR_LANGUAGES", "por+eng").split("+")
    ENABLE_TESSERACT = os.getenv("ENABLE_TESSERACT", "True").lower() == "true"
    ENABLE_GOOGLE_VISION = os.getenv("ENABLE_GOOGLE_VISION", "True").lower() == "true"
    
    # AI Analysis
    ENABLE_AI_ANALYSIS = True
    AI_ANALYSIS_MODEL = "gpt-4"
    MAX_TOKENS_ANALYSIS = 2000
    
    # Classification
    ENABLE_AUTO_CLASSIFICATION = True
    
    # Search Engine
    ENABLE_SEMANTIC_SEARCH = True
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    
    # Features
    ENABLE_BATCH_PROCESSING = True
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
    
    # Rate Limiting
    MAX_UPLOADS_PER_HOUR = int(os.getenv("MAX_UPLOADS_PER_HOUR", 100))
    RATE_LIMIT_WINDOW = 3600  # 1 hora
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = "ocr_processamento.log"
    
    # Security
    ENABLE_VIRUS_SCAN = os.getenv("ENABLE_VIRUS_SCAN", "False").lower() == "true"
    CLAMAV_HOST = os.getenv("CLAMAV_HOST", "localhost")
    CLAMAV_PORT = int(os.getenv("CLAMAV_PORT", 3310))

