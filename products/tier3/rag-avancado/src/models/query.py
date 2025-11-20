"""
Modelos de dados para queries RAG
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from datetime import datetime

from src.database import Base


class QueryHistory(Base):
    """Histórico de consultas RAG"""
    __tablename__ = "query_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=True)
    session_id = Column(String(100), index=True)
    
    # Query
    query_text = Column(Text, nullable=False)
    query_type = Column(String(50), default="semantic")  # semantic, keyword, hybrid
    
    # Results
    results_count = Column(Integer, default=0)
    top_similarity_score = Column(Float, nullable=True)
    
    # Answer
    answer_text = Column(Text, nullable=True)
    answer_confidence = Column(Float, nullable=True)
    
    # Citations
    citations = Column(JSON, nullable=True)
    sources = Column(JSON, nullable=True)
    
    # Performance
    processing_time_ms = Column(Integer, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    
    # Feedback
    rating = Column(Integer, nullable=True)  # 1-5
    feedback_text = Column(Text, nullable=True)
    is_helpful = Column(Boolean, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<QueryHistory(id={self.id}, query='{self.query_text[:50]}...')>"


class Citation(Base):
    """Citações e referências"""
    __tablename__ = "citations"
    
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, index=True)
    
    # Source
    document_id = Column(String(255), nullable=False)
    document_type = Column(String(50))  # processo, jurisprudencia, legislacao
    
    # Content
    text_excerpt = Column(Text, nullable=False)
    relevance_score = Column(Float, nullable=False)
    
    # Metadata
    metadata_json = Column(JSON, nullable=True)
    
    # Citation format
    citation_abnt = Column(Text, nullable=True)
    citation_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<Citation(id={self.id}, document_id='{self.document_id}')>"


class UserSession(Base):
    """Sessões de usuário para chat"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    user_id = Column(String(100), index=True, nullable=True)
    
    # Session data
    context = Column(JSON, nullable=True)
    conversation_history = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_activity = Column(DateTime, server_default=func.now())
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<UserSession(session_id='{self.session_id}')>"


class DocumentCache(Base):
    """Cache de documentos processados"""
    __tablename__ = "document_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(String(255), unique=True, index=True, nullable=False)
    
    # Content
    content = Column(Text, nullable=False)
    embeddings_computed = Column(Boolean, default=False)
    
    # Metadata
    document_type = Column(String(50))
    metadata_json = Column(JSON, nullable=True)
    
    # Stats
    query_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, server_default=func.now())
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<DocumentCache(document_id='{self.document_id}')>"

