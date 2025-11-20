#!/usr/bin/env python3
"""
Script para rodar o bot com configuração correta
"""

import os
import sys
from pathlib import Path

# Adicionar diretório ao path
base_dir = Path(__file__).parent
sys.path.insert(0, str(base_dir))

# Carregar variáveis de ambiente do .env
from dotenv import load_dotenv
load_dotenv(base_dir / '.env')

# Configurar PYTHONPATH
os.environ['PYTHONPATH'] = str(base_dir)

# Importar e rodar
from bot_telegram.src.bot import main
import asyncio

if __name__ == '__main__':
    print("🚀 Iniciando Bot de Telegram...")
    asyncio.run(main())

