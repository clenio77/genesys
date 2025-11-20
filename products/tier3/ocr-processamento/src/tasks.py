"""
Tasks Celery para processamento assíncrono
"""

from typing import List
from src.celery_app import celery_app
from src.database import SessionLocal
from src.services.document_uploader import DocumentUploader
from src.services.ocr_engine import OCREngine
from src.services.data_extractor import DataExtractor
from src.services.ai_analyzer import AIAnalyzer
from src.services.classifier import Classifier
from src.services.search_engine import SearchEngine
from datetime import datetime


# Inicializar serviços
document_uploader = DocumentUploader()
ocr_engine = OCREngine()
data_extractor = DataExtractor()
ai_analyzer = AIAnalyzer()
classifier = Classifier()
search_engine = SearchEngine()


@celery_app.task(name="process_document_task", bind=True, max_retries=3)
def process_document_task(self, document_id: int):
    """
    Task para processar documento completo em background
    
    Args:
        document_id: ID do documento
        
    Returns:
        Dict com resultado do processamento
    """
    db = SessionLocal()
    try:
        # Atualizar status para processing
        # Nota: get_document é async, mas em contexto Celery precisamos usar síncrono
        # Por enquanto, buscar diretamente do banco
        from src.models.document import Document
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            raise ValueError(f"Documento {document_id} não encontrado")
        
        document.status = "processing"
        db.commit()
        
        # Processar OCR (async)
        import asyncio
        ocr_result = asyncio.run(ocr_engine.process_document(document_id, db))
        
        # Extrair dados (async)
        extracted_data = asyncio.run(data_extractor.extract(document_id, db))
        
        # Classificar (async)
        classification = asyncio.run(classifier.classify(document_id, db))
        
        # Análise IA (async)
        analysis = asyncio.run(ai_analyzer.analyze(document_id, db))
        
        # Indexar para busca (async)
        index = asyncio.run(search_engine.index_document(document_id, db))
        
        # Atualizar status para processed
        document.status = "processed"
        document.processed_at = datetime.utcnow()
        db.commit()
        
        return {
            "success": True,
            "document_id": document_id,
            "ocr_confidence": ocr_result.confidence if ocr_result else 0.0,
            "extracted_fields": len(extracted_data) if extracted_data else 0,
            "category": classification.category if classification else None,
            "risk_score": analysis.risk_score if analysis else None,
            "indexed": index is not None
        }
    
    except Exception as e:
        # Marcar como failed
        try:
            from src.models.document import Document
            document = db.query(Document).filter(Document.id == document_id).first()
            if document:
                document.status = "failed"
                db.commit()
        except:
            pass
        
        # Retry se for erro temporário
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60)
        
        return {
            "success": False,
            "document_id": document_id,
            "error": str(e)
        }
    
    finally:
        db.close()


@celery_app.task(name="extract_data_task", bind=True, max_retries=2)
def extract_data_task(self, document_id: int):
    """
    Task para extrair dados de um documento
    
    Args:
        document_id: ID do documento
        
    Returns:
        Dict com dados extraídos
    """
    db = SessionLocal()
    try:
        # Processar OCR se necessário
        from src.models.document import OCRResult as OCRResultModel
        ocr_result = db.query(OCRResultModel).filter(
            OCRResultModel.document_id == document_id
        ).first()
        
        if not ocr_result:
            # Usar método síncrono para Celery
            import asyncio
            ocr_result = asyncio.run(ocr_engine.process_document(document_id, db))
        
        # Extrair dados
        import asyncio
        extracted_data = asyncio.run(data_extractor.extract(document_id, db))
        
        return {
            "success": True,
            "document_id": document_id,
            "extracted_count": len(extracted_data),
            "fields": [item.field for item in extracted_data]
        }
    
    except Exception as e:
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=30)
        
        return {
            "success": False,
            "document_id": document_id,
            "error": str(e)
        }
    
    finally:
        db.close()


@celery_app.task(name="analyze_document_task", bind=True, max_retries=2)
def analyze_document_task(self, document_id: int):
    """
    Task para analisar documento com IA
    
    Args:
        document_id: ID do documento
        
    Returns:
        Dict com análise
    """
    db = SessionLocal()
    try:
        import asyncio
        analysis = asyncio.run(ai_analyzer.analyze(document_id, db))
        
        return {
            "success": True,
            "document_id": document_id,
            "risk_score": analysis.risk_score,
            "sentiment": analysis.sentiment,
            "confidence": analysis.confidence
        }
    
    except Exception as e:
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=30)
        
        return {
            "success": False,
            "document_id": document_id,
            "error": str(e)
        }
    
    finally:
        db.close()


@celery_app.task(name="batch_process_task", bind=True)
def batch_process_task(self, document_ids: List[int]):
    """
    Task para processar lote de documentos
    
    Args:
        document_ids: Lista de IDs de documentos
        
    Returns:
        Dict com resultados
    """
    results = []
    for doc_id in document_ids:
        try:
            result = process_document_task.delay(doc_id)
            results.append({
                "document_id": doc_id,
                "task_id": result.id,
                "status": "queued"
            })
        except Exception as e:
            results.append({
                "document_id": doc_id,
                "status": "error",
                "error": str(e)
            })
    
    return {
        "success": True,
        "total": len(document_ids),
        "queued": len([r for r in results if r["status"] == "queued"]),
        "errors": len([r for r in results if r["status"] == "error"]),
        "results": results
    }


@celery_app.task(name="index_document_task")
def index_document_task(document_id: int):
    """
    Task para indexar documento para busca
    
    Args:
        document_id: ID do documento
        
    Returns:
        Dict com resultado
    """
    db = SessionLocal()
    try:
        import asyncio
        index = asyncio.run(search_engine.index_document(document_id, db))
        
        return {
            "success": True,
            "document_id": document_id,
            "indexed": index is not None
        }
    
    except Exception as e:
        return {
            "success": False,
            "document_id": document_id,
            "error": str(e)
        }
    
    finally:
        db.close()

