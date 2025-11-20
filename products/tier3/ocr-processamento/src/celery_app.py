"""
Configuração do Celery para processamento assíncrono
"""

from celery import Celery
from src.config import Config

# Criar instância do Celery
celery_app = Celery(
    "ocr_processamento",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=["src.tasks"]
)

# Configurações do Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

# Nomes das tasks
celery_app.conf.task_routes = {
    "src.tasks.process_document_task": {"queue": "documents"},
    "src.tasks.extract_data_task": {"queue": "extraction"},
    "src.tasks.analyze_document_task": {"queue": "analysis"},
    "src.tasks.batch_process_task": {"queue": "batch"},
}

