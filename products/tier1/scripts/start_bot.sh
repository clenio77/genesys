#!/bin/bash

# Script para iniciar o Bot de Telegram

echo "🚀 Iniciando Bot de Telegram..."

# Ir para o diretório correto
cd "$(dirname "$0")"

# Ativar ambiente virtual
source venv/bin/activate

# Configurar PYTHONPATH
export PYTHONPATH=$(pwd)

# Configurar token do Telegram (do .env)
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Iniciar o bot
python bot-telegram/src/bot.py

