"""
Configuração do banco de dados PostgreSQL
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from typing import Generator

from src.config import Config

# Criar engine
engine = create_engine(
    Config.DATABASE_URL,
    poolclass=NullPool,
    echo=Config.DEBUG,
    future=True
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)


def get_db() -> Generator[Session, None, None]:
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
    from src.models.document import Base
    Base.metadata.create_all(bind=engine)


def drop_db():
    """
    Remove todas as tabelas (cuidado!)
    """
    from src.models.document import Base
    Base.metadata.drop_all(bind=engine)

