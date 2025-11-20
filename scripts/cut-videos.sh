#!/bin/bash

# Script para Cortar Vídeos de Depoimentos
# Uso: bash scripts/cut-videos.sh

echo "🎬 Script de Corte de Vídeos - Genesys Tecnologia"
echo "=================================================="
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Diretórios
INPUT_DIR="public/videos"
OUTPUT_DIR="public/videos/cortados"
BACKUP_DIR="public/videos/originais"

# Criar diretórios
mkdir -p "$OUTPUT_DIR"
mkdir -p "$BACKUP_DIR"

echo -e "${BLUE}📁 Vídeos encontrados:${NC}"
echo ""

# Listar vídeos
videos=($(ls $INPUT_DIR/*.mp4 2>/dev/null))

if [ ${#videos[@]} -eq 0 ]; then
    echo -e "${RED}❌ Nenhum vídeo encontrado em $INPUT_DIR${NC}"
    exit 1
fi

for i in "${!videos[@]}"; do
    video="${videos[$i]}"
    basename=$(basename "$video")
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video")
    echo -e "${YELLOW}$((i+1)). $basename${NC} - Duração: ${duration}s"
done

echo ""
echo -e "${BLUE}================================================${NC}"
echo ""

# Função para cortar vídeo
cut_video() {
    local input=$1
    local output=$2
    local start=$3
    local duration=$4
    
    echo -e "${YELLOW}⏳ Cortando vídeo...${NC}"
    
    # Comando FFmpeg para cortar
    ffmpeg -i "$input" \
        -ss "$start" \
        -t "$duration" \
        -c:v libx264 -preset fast -crf 23 \
        -c:a aac -b:a 128k \
        -y \
        "$output" 2>&1 | grep -E "(Duration|time=)" || true
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Vídeo cortado com sucesso!${NC}"
        
        # Mostrar tamanho
        original_size=$(du -h "$input" | cut -f1)
        new_size=$(du -h "$output" | cut -f1)
        echo -e "${GREEN}   Original: $original_size → Cortado: $new_size${NC}"
        return 0
    else
        echo -e "${RED}❌ Erro ao cortar vídeo${NC}"
        return 1
    fi
}

# Processar cada vídeo
for video in "${videos[@]}"; do
    basename=$(basename "$video")
    name="${basename%.*}"
    
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📹 Processando: $basename${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    # Obter duração
    duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$video")
    echo -e "${YELLOW}Duração total: ${duration}s${NC}"
    echo ""
    
    # Perguntar se quer cortar
    read -p "$(echo -e ${GREEN}Deseja cortar este vídeo? [s/N]: ${NC})" -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
        echo -e "${YELLOW}⏭️  Pulando...${NC}"
        continue
    fi
    
    # Pedir tempo de início
    echo ""
    echo -e "${YELLOW}Em que segundo a fala termina?${NC}"
    echo -e "${YELLOW}(Exemplo: 5.5 para 5.5 segundos)${NC}"
    read -p "Tempo final (em segundos): " end_time
    
    # Validar entrada
    if ! [[ "$end_time" =~ ^[0-9]+\.?[0-9]*$ ]]; then
        echo -e "${RED}❌ Tempo inválido. Pulando...${NC}"
        continue
    fi
    
    # Calcular duração do corte
    cut_duration=$end_time
    
    echo ""
    echo -e "${GREEN}📊 Resumo do corte:${NC}"
    echo -e "   Início: 0s"
    echo -e "   Fim: ${end_time}s"
    echo -e "   Duração: ${cut_duration}s"
    echo ""
    
    # Confirmar
    read -p "$(echo -e ${GREEN}Confirmar corte? [s/N]: ${NC})" -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
        echo -e "${YELLOW}⏭️  Cancelado${NC}"
        continue
    fi
    
    # Fazer backup
    echo ""
    echo -e "${BLUE}💾 Fazendo backup do original...${NC}"
    cp "$video" "$BACKUP_DIR/$basename"
    echo -e "${GREEN}✅ Backup salvo em: $BACKUP_DIR/$basename${NC}"
    
    # Cortar vídeo
    echo ""
    output_file="$OUTPUT_DIR/${name}_cortado.mp4"
    
    if cut_video "$video" "$output_file" "0" "$cut_duration"; then
        echo ""
        echo -e "${GREEN}✅ Vídeo cortado salvo em: $output_file${NC}"
        
        # Perguntar se quer substituir o original
        echo ""
        read -p "$(echo -e ${YELLOW}Substituir o original pelo cortado? [s/N]: ${NC})" -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[SsYy]$ ]]; then
            cp "$output_file" "$video"
            echo -e "${GREEN}✅ Original substituído!${NC}"
        fi
    fi
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Processamento concluído!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📁 Arquivos:${NC}"
echo -e "   Originais (backup): $BACKUP_DIR/"
echo -e "   Cortados: $OUTPUT_DIR/"
echo ""
echo -e "${YELLOW}💡 Dica: Teste os vídeos cortados antes de substituir os originais!${NC}"
echo ""
