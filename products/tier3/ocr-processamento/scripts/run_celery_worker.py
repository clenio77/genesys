#!/usr/bin/env python3
"""
Script para executar Celery Worker
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.celery_app import celery_app

if __name__ == "__main__":
    celery_app.start()

