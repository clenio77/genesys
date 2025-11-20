#!/bin/bash

echo "🚀 Iniciando Bot com IA..."

cd "$(dirname "$0")"

# Ativar venv
source venv/bin/activate

# Configurar PYTHONPATH
export PYTHONPATH=$(pwd)

# Carregar todas as variáveis do .env
set -a
source .env
set +a

echo "✅ Configuração carregada"
echo "📱 Token: ${TELEGRAM_BOT_TOKEN:0:20}..."
echo "🧠 Gemini: ${GEMINI_API_KEY:0:15}..."
echo "🧠 OpenAI: ${OPENAI_API_KEY:+✅ Configurado}"

# Rodar bot
python bot-telegram/src/bot_com_ia.py

