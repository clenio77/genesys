#!/bin/bash
# Script para executar Celery Worker

cd "$(dirname "$0")/.."

# Ativar venv se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Executar Celery Worker
celery -A src.celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --queues=documents,extraction,analysis,batch \
    --hostname=worker@%h

