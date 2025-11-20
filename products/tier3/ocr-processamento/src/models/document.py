"""
Modelos de dados SQLAlchemy para documentos
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

# Importar Base do database para usar a mesma instância
from src.database import Base


class Document(Base):
    """Modelo de documento"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_hash = Column(String(64), unique=True, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(10), nullable=False)
    status = Column(String(50), default="uploaded")  # uploaded, processing, processed, failed
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    # Relationships
    ocr_results = relationship("OCRResult", back_populates="document", cascade="all, delete-orphan")
    extracted_data = relationship("ExtractedData", back_populates="document", cascade="all, delete-orphan")
    classifications = relationship("DocumentClassification", back_populates="document", cascade="all, delete-orphan")
    analysis_results = relationship("AnalysisResult", back_populates="document", cascade="all, delete-orphan")
    index = relationship("DocumentIndex", back_populates="document", uselist=False, cascade="all, delete-orphan")


class OCRResult(Base):
    """Resultado do OCR"""
    __tablename__ = "ocr_results"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    text = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    language = Column(String(10), default="por")
    method = Column(String(50))  # tesseract, google_vision
    pages = Column(JSON, nullable=True)  # Para PDFs multi-página
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    document = relationship("Document", back_populates="ocr_results")


class ExtractedData(Base):
    """Dados extraídos do documento"""
    __tablename__ = "extracted_data"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    field = Column(String(100), nullable=False)  # prazo, valor, parte, processo, etc
    value = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    metadata = Column(JSON, nullable=True)  # Informações adicionais
    extracted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    document = relationship("Document", back_populates="extracted_data")


class DocumentClassification(Base):
    """Classificação do documento"""
    __tablename__ = "document_classifications"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    category = Column(String(100), nullable=False)  # petição_inicial, sentença, etc
    confidence = Column(Float, nullable=False)
    urgency = Column(String(50), default="média")  # urgente, alta, média, baixa
    urgency_confidence = Column(Float, nullable=True)
    tags = Column(JSON, nullable=True)  # Lista de tags
    classified_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    document = relationship("Document", back_populates="classifications")


class AnalysisResult(Base):
    """Resultado da análise com IA"""
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    summary = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)  # Lista de pontos-chave
    risk_score = Column(Float, nullable=True)  # 0-10
    recommendations = Column(JSON, nullable=True)  # Lista de recomendações
    sentiment = Column(String(50), nullable=True)  # positive, neutral, negative
    confidence = Column(Float, nullable=False)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    document = relationship("Document", back_populates="analysis_results")


class DocumentIndex(Base):
    """Índice para busca semântica"""
    __tablename__ = "document_index"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), unique=True, nullable=False)
    embeddings = Column(JSON, nullable=True)  # Vetor de embeddings
    metadata = Column(JSON, nullable=True)  # Metadados para busca
    indexed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    document = relationship("Document", back_populates="index")

