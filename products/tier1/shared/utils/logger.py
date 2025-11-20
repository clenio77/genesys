"""
Sistema de logging compartilhado
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from ..config.settings import settings


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: Optional[str] = None
) -> logging.Logger:
    """
    Configura um logger para o serviço
    
    Args:
        name: Nome do logger
        log_file: Arquivo de log (opcional)
        level: Nível de log (opcional)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    # Nível de log
    log_level = level or settings.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (se especificado)
    if log_file:
        log_path = Path(settings.BASE_DIR) / "logs" / log_file
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Loggers globais para cada serviço
bot_telegram_logger = setup_logger("bot_telegram", "bot_telegram.log")
automacao_logger = setup_logger("automacao_prazos", "automacao_prazos.log")
assistente_logger = setup_logger("assistente_virtual", "assistente_virtual.log")

