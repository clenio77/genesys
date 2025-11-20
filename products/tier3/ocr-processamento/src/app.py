"""
OCR & Processamento de Documentos - FastAPI App Principal
Sistema completo de extração e análise inteligente de documentos jurídicos
"""

import sys
from pathlib import Path
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn

from src.config import Config
from src.database import get_db, init_db, SessionLocal
from src.services.document_uploader import DocumentUploader
from src.services.ocr_engine import OCREngine
from src.services.data_extractor import DataExtractor
from src.services.ai_analyzer import AIAnalyzer
from src.services.classifier import Classifier
from src.services.search_engine import SearchEngine
from src.tasks import process_document_task, extract_data_task, analyze_document_task, batch_process_task
from src.api.task_status import router as task_router
from sqlalchemy.orm import Session

# Setup
app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION,
    description="Sistema de OCR e processamento inteligente de documentos jurídicos"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_uploader = DocumentUploader()
ocr_engine = OCREngine()
data_extractor = DataExtractor()
ai_analyzer = AIAnalyzer()
classifier = Classifier()
search_engine = SearchEngine()

# Include routers
app.include_router(task_router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Inicializa banco de dados na inicialização"""
    init_db()


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "service": Config.APP_NAME,
        "version": Config.APP_VERSION,
        "status": "online",
        "endpoints": {
            "upload": "/api/documents/upload",
            "list": "/api/documents/",
            "details": "/api/documents/{id}",
            "extract": "/api/documents/{id}/extract",
            "analyze": "/api/documents/{id}/analyze",
            "search": "/api/documents/search",
            "stats": "/api/documents/stats",
            "batch": "/api/documents/batch"
        }
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "version": Config.APP_VERSION
    }


@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Upload de documento para processamento
    
    Endpoint: POST /api/documents/upload
    """
    try:
        # Validar arquivo
        if not document_uploader.validate_file(file):
            raise HTTPException(
                status_code=400,
                detail="Formato de arquivo não suportado ou arquivo muito grande"
            )
        
        # Upload e validação
        document_data = await document_uploader.upload_file(file)
        
        # Salvar no banco de dados
        document = document_uploader.create_document(document_data, db)
        
        # Processar em background usando Celery
        if Config.ENABLE_BATCH_PROCESSING:
            # Usar Celery task
            task = process_document_task.delay(document.id)
            return {
                "success": True,
                "document_id": document.id,
                "filename": document.filename,
                "status": document.status,
                "task_id": task.id,
                "message": "Documento enviado com sucesso. Processamento em andamento."
            }
        elif background_tasks:
            # Fallback para background tasks do FastAPI
            background_tasks.add_task(process_document_async, document.id)
        
        return {
            "success": True,
            "document_id": document.id,
            "filename": document.filename,
            "status": document.status,
            "message": "Documento enviado com sucesso. Processamento em andamento."
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents/")
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Listar documentos
    
    Endpoint: GET /api/documents/
    """
    try:
        documents = await document_uploader.list_documents(
            db=db,
            skip=skip,
            limit=limit,
            status=status
        )
        return {
            "success": True,
            "count": len(documents),
            "documents": [
                {
                    "id": doc.id,
                    "filename": doc.filename,
                    "file_size": doc.file_size,
                    "file_type": doc.file_type,
                    "status": doc.status,
                    "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None
                }
                for doc in documents
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents/{document_id}")
async def get_document_details(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Obter detalhes de um documento
    
    Endpoint: GET /api/documents/{id}
    """
    try:
        document = await document_uploader.get_document(document_id, db)
        if not document:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        
        return {
            "success": True,
            "document": {
                "id": document.id,
                "filename": document.filename,
                "stored_filename": document.stored_filename,
                "file_size": document.file_size,
                "file_type": document.file_type,
                "status": document.status,
                "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else None,
                "processed_at": document.processed_at.isoformat() if document.processed_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents/{document_id}/extract")
async def extract_data(
    document_id: int,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Extrair dados estruturados do documento
    
    Endpoint: POST /api/documents/{id}/extract
    """
    try:
        document = await document_uploader.get_document(document_id, db)
        if not document:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        
        # Processar OCR se necessário
        ocr_result = await ocr_engine.process_document(document_id, db)
        
        # Extrair dados
        if Config.ENABLE_BATCH_PROCESSING:
            task = extract_data_task.delay(document_id)
            return {
                "success": True,
                "message": "Extração iniciada em background",
                "document_id": document_id,
                "task_id": task.id
            }
        elif background_tasks:
            background_tasks.add_task(extract_data_async, document_id)
            return {
                "success": True,
                "message": "Extração iniciada em background",
                "document_id": document_id
            }
        else:
            extracted_data = await data_extractor.extract(document_id, db)
            return {
                "success": True,
                "document_id": document_id,
                "extracted_data": [
                    {
                        "field": item.field,
                        "value": item.value,
                        "confidence": item.confidence
                    }
                    for item in extracted_data
                ]
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents/{document_id}/analyze")
async def analyze_document(
    document_id: int,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Análise inteligente do documento com IA
    
    Endpoint: POST /api/documents/{id}/analyze
    """
    try:
        document = await document_uploader.get_document(document_id, db)
        if not document:
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        
        if Config.ENABLE_BATCH_PROCESSING:
            task = analyze_document_task.delay(document_id)
            return {
                "success": True,
                "message": "Análise iniciada em background",
                "document_id": document_id,
                "task_id": task.id
            }
        elif background_tasks:
            background_tasks.add_task(analyze_document_async, document_id)
            return {
                "success": True,
                "message": "Análise iniciada em background",
                "document_id": document_id
            }
        else:
            analysis = await ai_analyzer.analyze(document_id, db)
            return {
                "success": True,
                "document_id": document_id,
                "analysis": {
                    "summary": analysis.summary,
                    "key_points": analysis.key_points,
                    "risk_score": analysis.risk_score,
                    "recommendations": analysis.recommendations,
                    "sentiment": analysis.sentiment,
                    "confidence": analysis.confidence
                }
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents/search")
async def search_documents(
    query: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Buscar documentos (semântica)
    
    Endpoint: GET /api/documents/search?query=...
    """
    try:
        results = await search_engine.search(query, limit=limit, db=db)
        return {
            "success": True,
            "query": query,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Estatísticas dos documentos
    
    Endpoint: GET /api/documents/stats
    """
    try:
        stats = await document_uploader.get_stats(db)
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents/batch")
async def batch_process(
    document_ids: List[int],
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Processar lote de documentos
    
    Endpoint: POST /api/documents/batch
    Body: {"document_ids": [1, 2, 3]}
    """
    try:
        if Config.ENABLE_BATCH_PROCESSING:
            # Usar Celery para processamento em lote
            task = batch_process_task.delay(document_ids)
            return {
                "success": True,
                "message": f"Processamento em lote iniciado para {len(document_ids)} documentos",
                "document_ids": document_ids,
                "task_id": task.id,
                "total": len(document_ids)
            }
        elif background_tasks:
            background_tasks.add_task(batch_process_async, document_ids)
            return {
                "success": True,
                "message": f"Processamento em lote iniciado para {len(document_ids)} documentos",
                "document_ids": document_ids
            }
        else:
            # Processar síncrono (não recomendado para muitos documentos)
            results = []
            for doc_id in document_ids:
                document = await document_uploader.get_document(doc_id, db)
                if document:
                    result = await process_document_async(doc_id)
                    results.append(result)
            
            return {
                "success": True,
                "processed": len(results),
                "results": results
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Background tasks
async def process_document_async(document_id: int):
    """Processar documento completo em background"""
    db = SessionLocal()
    try:
        # Atualizar status para processing
        document = await document_uploader.get_document(document_id, db)
        if document:
            document.status = "processing"
            db.commit()
        
        # OCR
        await ocr_engine.process_document(document_id, db)
        
        # Extração
        await data_extractor.extract(document_id, db)
        
        # Classificação
        await classifier.classify(document_id, db)
        
        # Análise IA
        await ai_analyzer.analyze(document_id, db)
        
        # Indexar para busca
        await search_engine.index_document(document_id, db)
        
        # Atualizar status para processed
        if document:
            document.status = "processed"
            from datetime import datetime
            document.processed_at = datetime.utcnow()
            db.commit()
        
    except Exception as e:
        print(f"Erro ao processar documento {document_id}: {e}")
        # Marcar como failed
        try:
            document = await document_uploader.get_document(document_id, db)
            if document:
                document.status = "failed"
                db.commit()
        except:
            pass
    finally:
        db.close()


async def extract_data_async(document_id: int):
    """Extrair dados em background"""
    db = SessionLocal()
    try:
        await ocr_engine.process_document(document_id, db)
        await data_extractor.extract(document_id, db)
    except Exception as e:
        print(f"Erro ao extrair dados do documento {document_id}: {e}")
    finally:
        db.close()


async def analyze_document_async(document_id: int):
    """Analisar documento em background"""
    db = SessionLocal()
    try:
        await ai_analyzer.analyze(document_id, db)
    except Exception as e:
        print(f"Erro ao analisar documento {document_id}: {e}")
    finally:
        db.close()


async def batch_process_async(document_ids: List[int]):
    """Processar lote em background"""
    for doc_id in document_ids:
        await process_document_async(doc_id)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=Config.PORT,
        reload=Config.DEBUG
    )

