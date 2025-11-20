#!/bin/bash
# Script para criar arquivo ZIP para deploy no Pella

echo "📦 Preparando arquivo ZIP para deploy no Pella..."

# Obter diretório do script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Nome do arquivo ZIP
ZIP_FILE="$PROJECT_ROOT/bot-pella-deploy.zip"

# Remover ZIP anterior se existir
if [ -f "$ZIP_FILE" ]; then
    echo "🗑️  Removendo ZIP anterior..."
    rm "$ZIP_FILE"
fi

# Criar diretório temporário
TEMP_DIR=$(mktemp -d)
echo "📁 Diretório temporário: $TEMP_DIR"

# Copiar pastas necessárias
echo "📋 Copiando pastas necessárias..."
cp -r "$PROJECT_ROOT/bot-telegram" "$TEMP_DIR/"
cp -r "$PROJECT_ROOT/shared" "$TEMP_DIR/"
cp "$PROJECT_ROOT/requirements.txt" "$TEMP_DIR/"

# Verificar se .pellaignore existe e aplicar
if [ -f .pellaignore ]; then
    echo "🚫 Aplicando .pellaignore..."
    cd "$TEMP_DIR"
    
    # Remover arquivos ignorados
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
    find . -type d -name "*.pyc" -exec rm -rf {} + 2>/dev/null
    
    cd - > /dev/null
fi

# Criar ZIP
echo "📦 Criando arquivo ZIP..."
cd "$TEMP_DIR"
zip -r "$PROJECT_ROOT/bot-pella-deploy.zip" . -q
cd "$PROJECT_ROOT" > /dev/null

# Verificar tamanho ANTES de limpar
ZIP_FILE_FINAL="$PROJECT_ROOT/bot-pella-deploy.zip"
if [ -f "$ZIP_FILE_FINAL" ]; then
    SIZE=$(du -h "$ZIP_FILE_FINAL" | cut -f1)
    SIZE_BYTES=$(du -b "$ZIP_FILE_FINAL" | cut -f1)
    SIZE_MB=$((SIZE_BYTES / 1024 / 1024))
    
    echo "✅ ZIP criado com sucesso!"
    echo "📊 Tamanho: $SIZE ($SIZE_MB MB)"
    echo "📁 Arquivo: $ZIP_FILE_FINAL"
    
    if [ "$SIZE_MB" -gt 30 ]; then
        echo ""
        echo "⚠️  ATENÇÃO: O arquivo tem mais de 30MB!"
        echo "   Pella aceita no máximo 30MB."
        echo "   Verifique o que está sendo incluído no ZIP."
    fi
else
    echo "❌ Erro ao criar ZIP!"
fi

# Limpar diretório temporário
rm -rf "$TEMP_DIR"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Limite máximo no Pella: 30MB"
echo "   - Se o arquivo for maior, verifique o que está sendo incluído"
echo ""
echo "🚀 Próximo passo:"
echo "   1. Acesse https://www.pella.app"
echo "   2. Vá em 'Code Source' → 'File Upload'"
echo "   3. Faça upload do arquivo: $ZIP_FILE_FINAL"

