"""
Endpoint para verificar status de tasks Celery
"""

from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from src.celery_app import celery_app

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """
    Verifica status de uma task Celery
    
    Endpoint: GET /api/tasks/{task_id}
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        if task_result.state == "PENDING":
            response = {
                "task_id": task_id,
                "state": task_result.state,
                "status": "Aguardando processamento"
            }
        elif task_result.state == "PROGRESS":
            response = {
                "task_id": task_id,
                "state": task_result.state,
                "status": "Em processamento",
                "progress": task_result.info.get("progress", 0) if isinstance(task_result.info, dict) else None
            }
        elif task_result.state == "SUCCESS":
            response = {
                "task_id": task_id,
                "state": task_result.state,
                "status": "Concluída",
                "result": task_result.result
            }
        else:  # FAILURE
            response = {
                "task_id": task_id,
                "state": task_result.state,
                "status": "Falhou",
                "error": str(task_result.info) if task_result.info else "Erro desconhecido"
            }
        
        return {
            "success": True,
            **response
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

