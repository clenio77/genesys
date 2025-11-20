"""
Configurações para RAG Avançado
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações globais do RAG Avançado"""
    
    # App
    APP_NAME = "Genesys RAG Avançado"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8002))
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://genesys:genesys@localhost:5432/genesys_db"
    )
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
    
    # ChromaDB - Integração com Kermartin
    CHROMADB_PATH = os.getenv(
        "CHROMADB_PATH",
        "/home/clenio/Documentos/Meusagentes/kermartin/chroma_db"
    )
    CHROMADB_COLLECTION = os.getenv("CHROMADB_COLLECTION", "legal_knowledge")
    
    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))
    MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", 4000))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.7))
    
    # LangChain
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
    
    # Rate Limiting
    MAX_QUERIES_PER_HOUR = int(os.getenv("MAX_QUERIES_PER_HOUR", 100))
    MAX_CONCURRENT_QUERIES = int(os.getenv("MAX_CONCURRENT_QUERIES", 10))
    
    # Features
    ENABLE_CHAT = os.getenv("ENABLE_CHAT", "True").lower() == "true"
    ENABLE_CITATIONS = os.getenv("ENABLE_CITATIONS", "True").lower() == "true"
    ENABLE_FEEDBACK = os.getenv("ENABLE_FEEDBACK", "True").lower() == "true"
    ENABLE_HISTORY = os.getenv("ENABLE_HISTORY", "True").lower() == "true"
    
    # Security
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "rag_avancado.log")
    ENABLE_LOGGING = os.getenv("ENABLE_LOGGING", "True").lower() == "true"
    
    # Validação
    @classmethod
    def validate(cls):
        """Valida configurações críticas"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não configurado")
        
        if not Path(cls.CHROMADB_PATH).exists():
            raise ValueError(f"ChromaDB path não existe: {cls.CHROMADB_PATH}")
        
        return True

