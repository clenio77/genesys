#!/bin/bash

# Script para executar testes do Tier 1

echo "🧪 Executando testes do Tier 1..."
echo ""

# Corrigir imports
export PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/shared:$(pwd)/bot-telegram/src:$(pwd)/automacao-prazos/src:$(pwd)/assistente-virtual/src"

# Executar testes
pytest tests/ -v

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Todos os testes passaram!"
else
    echo ""
    echo "❌ Alguns testes falharam. Verifique os logs acima."
fi

