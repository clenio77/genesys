"""
Microserviço 6: Search Engine
Responsável por busca semântica em documentos
"""

from typing import Dict, List, Optional
from datetime import datetime
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import or_

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from src.config import Config
from src.models.document import Document, DocumentIndex, OCRResult
from src.services.document_uploader import DocumentUploader


class SearchEngine:
    """Motor de busca semântica em documentos"""
    
    def __init__(self):
        self.enable_semantic = Config.ENABLE_SEMANTIC_SEARCH
        self.embedding_model = Config.EMBEDDING_MODEL
        self.document_uploader = DocumentUploader()
        
        if OPENAI_AVAILABLE and Config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        else:
            self.openai_client = None
            self.enable_semantic = False
        
        # Cache de embeddings (em produção seria Redis ou DB)
        self.embeddings_cache = {}
    
    async def search(self, query: str, limit: int = 10, db: Session = None) -> List[Dict]:
        """
        Busca documentos por query
        
        Args:
            query: Texto de busca
            limit: Limite de resultados
            db: Sessão do banco de dados (opcional)
            
        Returns:
            Lista de documentos encontrados
        """
        if db and self.enable_semantic and self.openai_client:
            return await self.semantic_search(query, limit, db)
        elif db:
            return await self.keyword_search(query, limit, db)
        else:
            # Fallback sem banco
            return await self.keyword_search(query, limit)
    
    async def semantic_search(self, query: str, limit: int = 10, db: Session = None) -> List[Dict]:
        """
        Busca semântica usando embeddings
        
        Args:
            query: Texto de busca
            limit: Limite de resultados
            db: Sessão do banco de dados
            
        Returns:
            Lista de documentos com scores de relevância
        """
        if not db:
            return await self.keyword_search(query, limit)
        
        try:
            # Gerar embedding da query
            query_embedding = await self._get_embedding(query)
            
            if not query_embedding:
                # Fallback para keyword search se não conseguir gerar embedding
                return await self.keyword_search(query, limit, db)
            
            # Buscar documentos indexados do banco
            indexed_docs = db.query(DocumentIndex).all()
            
            if not indexed_docs:
                # Se não há documentos indexados, usar keyword search
                return await self.keyword_search(query, limit, db)
            
            # Calcular similaridade com documentos indexados
            results = []
            query_vec = np.array(query_embedding)
            
            for doc_index in indexed_docs:
                if doc_index.embeddings:
                    doc_vec = np.array(doc_index.embeddings)
                    similarity = self._cosine_similarity(query_vec, doc_vec)
                    
                    # Buscar documento completo
                    document = db.query(Document).filter(
                        Document.id == doc_index.document_id
                    ).first()
                    
                    if document:
                        # Buscar OCR para snippet
                        ocr_result = db.query(OCRResult).filter(
                            OCRResult.document_id == document.id
                        ).first()
                        
                        snippet = ""
                        if ocr_result:
                            # Criar snippet com palavras-chave
                            text_lower = ocr_result.text.lower()
                            query_lower = query.lower()
                            query_words = query_lower.split()
                            
                            # Encontrar primeira ocorrência
                            for word in query_words:
                                if word in text_lower:
                                    idx = text_lower.find(word)
                                    start = max(0, idx - 50)
                                    end = min(len(ocr_result.text), idx + len(word) + 50)
                                    snippet = ocr_result.text[start:end]
                                    if snippet:
                                        snippet = "..." + snippet + "..."
                                    break
                        
                        results.append({
                            "document_id": document.id,
                            "filename": document.filename,
                            "score": float(similarity),
                            "relevance": "high" if similarity > 0.8 else "medium" if similarity > 0.6 else "low",
                            "snippet": snippet or f"Documento {document.filename}",
                            "status": document.status
                        })
            
            # Ordenar por score
            results.sort(key=lambda x: x["score"], reverse=True)
            
            return results[:limit]
        
        except Exception as e:
            print(f"Erro na busca semântica: {e}")
            return await self.keyword_search(query, limit, db)
    
    async def keyword_search(self, query: str, limit: int = 10, db: Session = None) -> List[Dict]:
        """
        Busca por palavras-chave no banco de dados
        
        Args:
            query: Texto de busca
            limit: Limite de resultados
            db: Sessão do banco de dados
            
        Returns:
            Lista de documentos encontrados
        """
        if not db:
            return []
        
        keywords = query.lower().split()
        
        # Construir filtros de busca
        filters = []
        for keyword in keywords:
            filters.append(OCRResult.text.ilike(f"%{keyword}%"))
        
        if not filters:
            return []
        
        # Buscar OCR results que contenham pelo menos uma palavra-chave
        ocr_results = db.query(OCRResult).filter(
            or_(*filters)
        ).limit(limit * 2).all()  # Buscar mais para calcular scores
        
        if not ocr_results:
            return []
        
        # Calcular scores baseado em quantas palavras foram encontradas
        results = []
        for ocr_result in ocr_results:
            text_lower = ocr_result.text.lower()
            matched_count = sum(1 for keyword in keywords if keyword in text_lower)
            score = matched_count / len(keywords) if keywords else 0
            
            # Buscar documento
            document = db.query(Document).filter(
                Document.id == ocr_result.document_id
            ).first()
            
            if document:
                # Criar snippet
                snippet = ""
                for keyword in keywords:
                    if keyword in text_lower:
                        idx = text_lower.find(keyword)
                        start = max(0, idx - 50)
                        end = min(len(ocr_result.text), idx + len(keyword) + 50)
                        snippet = ocr_result.text[start:end]
                        if snippet:
                            snippet = "..." + snippet + "..."
                        break
                
                results.append({
                    "document_id": document.id,
                    "filename": document.filename,
                    "score": score,
                    "relevance": "high" if score > 0.8 else "medium" if score > 0.5 else "low",
                    "snippet": snippet or f"Documento {document.filename}",
                    "matched_keywords": [kw for kw in keywords if kw in text_lower],
                    "status": document.status
                })
        
        # Ordenar por score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]
    
    async def index_document(self, document_id: int, db: Session) -> DocumentIndex:
        """
        Indexa documento para busca e salva no banco
        
        Args:
            document_id: ID do documento
            db: Sessão do banco de dados
            
        Returns:
            DocumentIndex salvo no banco
        """
        try:
            # Verificar se já existe índice
            existing_index = db.query(DocumentIndex).filter(
                DocumentIndex.document_id == document_id
            ).first()
            
            if existing_index:
                return existing_index
            
            # Buscar texto OCR do banco
            ocr_result = db.query(OCRResult).filter(
                OCRResult.document_id == document_id
            ).first()
            
            if not ocr_result:
                raise ValueError(f"OCR não encontrado para documento {document_id}")
            
            # Gerar embedding do documento
            embedding = None
            if self.enable_semantic and self.openai_client:
                embedding = await self._get_embedding(ocr_result.text)
            
            # Salvar índice no banco
            document_index = DocumentIndex(
                document_id=document_id,
                embeddings=embedding.tolist() if embedding is not None else None,
                metadata={
                    "text_length": len(ocr_result.text),
                    "language": ocr_result.language,
                    "method": ocr_result.method
                }
            )
            
            db.add(document_index)
            db.commit()
            db.refresh(document_index)
            
            return document_index
        
        except Exception as e:
            print(f"Erro ao indexar documento {document_id}: {e}")
            raise
    
    async def _get_embedding(self, text: str) -> List[float]:
        """
        Gera embedding do texto usando OpenAI
        
        Args:
            text: Texto para gerar embedding
            
        Returns:
            Lista de valores do embedding
        """
        if not self.openai_client:
            raise Exception("OpenAI não disponível")
        
        try:
            # Limitar tamanho do texto
            max_chars = 8000
            if len(text) > max_chars:
                text = text[:max_chars]
            
            response = self.openai_client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            return response.data[0].embedding if response.data else []
        
        except Exception as e:
            raise Exception(f"Erro ao gerar embedding: {e}")
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calcula similaridade de cosseno entre dois vetores
        
        Args:
            vec1: Primeiro vetor
            vec2: Segundo vetor
            
        Returns:
            Score de similaridade (0-1)
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

