"""
Database setup para RAG Avançado
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import NullPool
from typing import Generator

from src.config import Config

# Engine
engine = create_engine(
    Config.DATABASE_URL,
    poolclass=NullPool,
    echo=Config.DEBUG,
    future=True
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Base para modelos
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco
    
    Yields:
        Session do SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Inicializa banco de dados - cria todas as tabelas"""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Remove todas as tabelas (usar com cuidado)"""
    Base.metadata.drop_all(bind=engine)

