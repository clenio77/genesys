#!/bin/bash

# Script para rodar o bot localmente

echo "🚀 Iniciando Bot de Telegram Localmente..."

# Ir para o diretório do script
cd "$(dirname "$0")"

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "💡 Execute primeiro: python -m venv venv"
    exit 1
fi

# Ativar venv
source venv/bin/activate

# Configurar PYTHONPATH
export PYTHONPATH=$(pwd)

# Carregar todas as variáveis do .env se existir
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "✅ Configuração carregada do .env"
else
    echo "⚠️  Arquivo .env não encontrado"
    echo "💡 Certifique-se de ter TELEGRAM_BOT_TOKEN configurado"
fi

# Verificar token
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN não configurado!"
    echo "💡 Configure no arquivo .env ou como variável de ambiente"
    exit 1
fi

echo ""
echo "📱 Bot: ${TELEGRAM_BOT_TOKEN:0:20}..."
[ -n "$GEMINI_API_KEY" ] && echo "🧠 Gemini: ${GEMINI_API_KEY:0:15}..." || echo "🧠 Gemini: Não configurado"
[ -n "$OPENAI_API_KEY" ] && echo "🧠 OpenAI: ✅ Configurado" || echo "🧠 OpenAI: Não configurado"
echo ""

# Rodar bot com IA (versão completa)
echo "🤖 Iniciando bot com IA..."
python bot-telegram/src/bot_com_ia.py

