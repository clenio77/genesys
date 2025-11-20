"""
Aplicação FastAPI principal - RAG Avançado
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import time
from datetime import datetime

from src.config import Config
from src.database import get_db, init_db, SessionLocal
from src.models.query import QueryHistory, Citation, UserSession
from src.services import (
    QueryProcessor,
    Retriever,
    ContextBuilder,
    AnswerGenerator,
    CitationManager,
    FeedbackCollector
)
from sqlalchemy.orm import Session

# Setup
app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION,
    description="Sistema avançado de RAG para consultas jurídicas"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar serviços
query_processor = QueryProcessor()
retriever = Retriever()
context_builder = ContextBuilder()
answer_generator = AnswerGenerator()
citation_manager = CitationManager()
feedback_collector = FeedbackCollector()


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Inicializa banco de dados"""
    init_db()
    print(f"✅ {Config.APP_NAME} v{Config.APP_VERSION} iniciado!")


# Pydantic Models
class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    context: Optional[dict] = None


class FeedbackRequest(BaseModel):
    rating: Optional[int] = None  # 1-5
    is_helpful: Optional[bool] = None
    comment: Optional[str] = None


class IndexDocumentRequest(BaseModel):
    document_id: str
    content: str
    metadata: dict


# Endpoints

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "name": Config.APP_NAME,
        "version": Config.APP_VERSION,
        "status": "online",
        "endpoints": {
            "query": "/api/rag/query",
            "history": "/api/rag/history",
            "citations": "/api/rag/citations/{query_id}",
            "feedback": "/api/rag/feedback/{query_id}",
            "index": "/api/rag/index",
            "stats": "/api/rag/stats"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "chromadb": "connected" if retriever.collection else "disconnected"
    }


@app.post("/api/rag/query")
async def query_rag(
    request: QueryRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Endpoint principal: Consulta RAG
    
    Processo:
    1. Processar query
    2. Buscar documentos
    3. Construir contexto
    4. Gerar resposta
    5. Processar citações
    6. Salvar histórico
    """
    start_time = time.time()
    
    try:
        # 1. Processar query
        processed_query = query_processor.process_query(
            request.query,
            request.context
        )
        
        # 2. Buscar documentos relevantes
        documents = await retriever.retrieve(
            request.query,
            processed_query
        )
        
        if not documents:
            return {
                "success": False,
                "message": "Nenhum documento relevante encontrado",
                "query": request.query
            }
        
        # 3. Construir contexto
        context = await context_builder.build_context(
            processed_query,
            documents,
            request.context.get("conversation_history") if request.context else None
        )
        
        # 4. Gerar resposta
        answer_result = await answer_generator.generate_answer(context)
        
        # 5. Processar citações
        citations = await citation_manager.process_citations(
            answer_result.get("answer", ""),
            documents
        )
        
        # 6. Salvar no histórico
        processing_time = int((time.time() - start_time) * 1000)
        
        query_history = QueryHistory(
            user_id=request.session_id,
            session_id=request.session_id or "anonymous",
            query_text=request.query,
            query_type=processed_query.get("query_type"),
            results_count=len(documents),
            top_similarity_score=documents[0].get("similarity_score") if documents else 0,
            answer_text=answer_result.get("answer"),
            answer_confidence=answer_result.get("confidence"),
            processing_time_ms=processing_time,
            tokens_used=answer_result.get("tokens_used")
        )
        
        db.add(query_history)
        db.commit()
        db.refresh(query_history)
        
        # Salvar citações
        for citation in citations:
            citation["query_id"] = query_history.id
            citation_obj = Citation(
                query_id=query_history.id,
                document_id=citation["document_id"],
                document_type=citation["metadata"].get("tipo"),
                text_excerpt=citation["excerpt"],
                relevance_score=citation["relevance_score"],
                metadata_json=citation["metadata"],
                citation_abnt=citation["citation_abnt"],
                citation_url=citation.get("url")
            )
            db.add(citation_obj)
        
        db.commit()
        
        return {
            "success": True,
            "query_id": query_history.id,
            "query": request.query,
            "answer": answer_result.get("answer"),
            "confidence": answer_result.get("confidence"),
            "citations": citations,
            "metadata": {
                "documents_found": len(documents),
                "query_type": processed_query.get("query_type"),
                "processing_time_ms": processing_time,
                "tokens_used": answer_result.get("tokens_used")
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rag/history")
async def get_history(
    session_id: Optional[str] = None,
    limit: int = 20,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    """
    Retorna histórico de consultas
    """
    try:
        query = db.query(QueryHistory)
        
        if session_id:
            query = query.filter(QueryHistory.session_id == session_id)
        
        total = query.count()
        
        queries = query.order_by(
            QueryHistory.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return {
            "success": True,
            "total": total,
            "queries": [
                {
                    "id": q.id,
                    "query": q.query_text,
                    "answer": q.answer_text[:200] + "..." if len(q.answer_text or "") > 200 else q.answer_text,
                    "type": q.query_type,
                    "confidence": q.answer_confidence,
                    "rating": q.rating,
                    "created_at": q.created_at.isoformat() if q.created_at else None
                }
                for q in queries
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rag/citations/{query_id}")
async def get_citations(
    query_id: int,
    db: Session = Depends(get_db)
):
    """
    Retorna citações de uma query específica
    """
    try:
        citations = db.query(Citation).filter(
            Citation.query_id == query_id
        ).all()
        
        return {
            "success": True,
            "query_id": query_id,
            "citations": [
                {
                    "document_id": c.document_id,
                    "type": c.document_type,
                    "excerpt": c.text_excerpt,
                    "relevance": c.relevance_score,
                    "citation_abnt": c.citation_abnt,
                    "url": c.citation_url,
                    "metadata": c.metadata_json
                }
                for c in citations
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag/feedback/{query_id}")
async def submit_feedback(
    query_id: int,
    feedback: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submete feedback para uma query
    """
    try:
        result = await feedback_collector.collect_feedback(
            query_id,
            feedback.dict(),
            db
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag/index")
async def index_document(
    request: IndexDocumentRequest,
    db: Session = Depends(get_db)
):
    """
    Indexa novo documento no ChromaDB
    """
    try:
        success = await retriever.add_document(
            request.document_id,
            request.content,
            request.metadata
        )
        
        if success:
            return {
                "success": True,
                "document_id": request.document_id,
                "message": "Documento indexado com sucesso"
            }
        else:
            return {
                "success": False,
                "message": "Erro ao indexar documento"
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rag/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas do sistema
    """
    try:
        # Stats do banco
        total_queries = db.query(QueryHistory).count()
        
        from sqlalchemy import func
        avg_confidence = db.query(func.avg(QueryHistory.answer_confidence)).scalar()
        avg_processing_time = db.query(func.avg(QueryHistory.processing_time_ms)).scalar()
        
        # Stats do ChromaDB
        chroma_stats = await retriever.get_collection_stats()
        
        # Stats de feedback
        feedback_stats = await feedback_collector.get_feedback_stats(db)
        
        return {
            "success": True,
            "stats": {
                "queries": {
                    "total": total_queries,
                    "avg_confidence": round(avg_confidence, 4) if avg_confidence else 0,
                    "avg_processing_time_ms": round(avg_processing_time, 2) if avg_processing_time else 0
                },
                "chromadb": chroma_stats,
                "feedback": feedback_stats
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """
    WebSocket para chat em tempo real
    
    Cliente deve enviar mensagens no formato:
    {"type": "message", "content": "sua pergunta aqui"}
    """
    from src.api.websocket_chat import manager, handle_chat_message
    
    await manager.connect(websocket, session_id)
    
    try:
        # Enviar mensagem de boas-vindas
        await websocket.send_json({
            "type": "connected",
            "message": "Conectado ao RAG Avançado! Como posso ajudar?",
            "session_id": session_id
        })
        
        while True:
            # Receber mensagem
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            
            if message_type == "message":
                content = data.get("content", "")
                if content:
                    # Processar mensagem
                    await handle_chat_message(session_id, content)
            
            elif message_type == "ping":
                # Responder pong para keep-alive
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        print(f"❌ Erro no WebSocket: {e}")
        manager.disconnect(session_id)


if __name__ == "__main__":
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=Config.PORT,
        reload=Config.DEBUG
    )

