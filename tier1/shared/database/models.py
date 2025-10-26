"""
Modelos SQLAlchemy para o banco de dados
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey, BigInteger, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..config.database import Base


class User(Base):
    """Modelo de usuário"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20), nullable=True)
    role = Column(String(50), default="user")
    token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    chats = relationship("Chat", back_populates="user")
    prazos = relationship("Prazo", back_populates="user")
    notificacoes = relationship("Notificacao", back_populates="user")


class Chat(Base):
    """Modelo de histórico de conversas"""
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service = Column(String(50))  # 'telegram', 'whatsapp', 'web'
    message = Column(Text)
    response = Column(Text)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="chats")


class Prazo(Base):
    """Modelo de prazos processuais"""
    __tablename__ = "prazos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tipo = Column(String(100))  # 'contestacao', 'recurso', 'embargos', etc
    processo = Column(String(50), nullable=True)
    tribunal = Column(String(100), nullable=True)
    data_vencimento = Column(Date, nullable=False)
    status = Column(String(50), default="pendente")  # 'pendente', 'concluido', 'cancelado'
    alertas_enviados = Column(Integer, default=0)
    ultima_notificacao = Column(DateTime, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="prazos")
    notificacoes = relationship("Notificacao", back_populates="prazo")


class Notificacao(Base):
    """Modelo de notificações enviadas"""
    __tablename__ = "notificacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    prazo_id = Column(Integer, ForeignKey("prazos.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    canal = Column(String(50))  # 'email', 'whatsapp', 'telegram'
    mensagem = Column(Text)
    status = Column(String(50), default="enviada")  # 'enviada', 'falhou', 'pendente'
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    prazo = relationship("Prazo", back_populates="notificacoes")
    user = relationship("User", back_populates="notificacoes")


class Alerta(Base):
    """Modelo de alertas gerais"""
    __tablename__ = "alertas"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    tipo = Column(String(100))  # 'prazo', 'movimentacao', 'legislativo'
    titulo = Column(String(255))
    mensagem = Column(Text)
    prioridade = Column(String(50), default="media")  # 'baixa', 'media', 'alta', 'critica'
    lido = Column(Boolean, default=False)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())


class ConsultaJurisprudencia(Base):
    """Modelo de consultas de jurisprudência"""
    __tablename__ = "consultas_jurisprudencia"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    query = Column(Text)
    results = Column(JSON)
    service = Column(String(50))  # 'telegram', 'whatsapp', 'web'
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())

