#!/bin/bash

echo "🤖 Iniciando Bot de Telegram Genesys..."

cd "$(dirname "$0")"

# Ativar venv
source venv/bin/activate

# Configurar PYTHONPATH
export PYTHONPATH="$(pwd)"

# Carregar variáveis do .env
set -a
source .env
set +a

echo "✅ Configuração carregada"
echo "📱 Token: ${TELEGRAM_BOT_TOKEN:0:20}..."
echo "🧠 IA: ${OPENAI_API_KEY:+✅ OpenAI} ${GEMINI_API_KEY:+✅ Gemini}"

# Rodar bot
python bot-telegram/src/bot.py

