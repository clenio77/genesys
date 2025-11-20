"""
Configuração do banco de dados PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import Generator

from .settings import settings

# Criar engine
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,
    echo=False,
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Base class
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency injection para obter sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados (cria todas as tabelas)
    """
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Remove todas as tabelas do banco de dados
    """
    Base.metadata.drop_all(bind=engine)

