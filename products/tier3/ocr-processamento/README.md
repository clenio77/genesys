# 📄 OCR & Processamento de Documentos - Tier 3

Sistema completo de extração e análise inteligente de documentos jurídicos usando OCR avançado e IA.

## 🏗️ Arquitetura METHOD-BMAD

### B - Backend
- **FastAPI** - API REST moderna e assíncrona
- **Tesseract OCR** - OCR open-source
- **Google Vision API** - OCR avançado com alta precisão
- **OpenAI GPT-4** - Análise inteligente de conteúdo
- **PostgreSQL** - Armazenamento de documentos e resultados
- **Redis** - Cache e filas
- **Celery** - Processamento assíncrono

### M - Modelo (Microserviços)
1. **Document Uploader** - Upload e validação de arquivos
2. **OCR Engine** - Extração de texto (Tesseract + Google Vision)
3. **Data Extractor** - Extração de dados estruturados
4. **AI Analyzer** - Análise inteligente com GPT-4
5. **Classifier** - Classificação automática de documentos
6. **Search Engine** - Busca semântica em documentos

### A - API
8 endpoints REST:
- `POST /api/documents/upload` - Upload de documento
- `GET /api/documents/` - Listar documentos
- `GET /api/documents/{id}` - Detalhes do documento
- `POST /api/documents/{id}/extract` - Extrair dados
- `POST /api/documents/{id}/analyze` - Análise IA
- `GET /api/documents/search` - Buscar documentos
- `GET /api/documents/stats` - Estatísticas
- `POST /api/documents/batch` - Processar lote

### D - Data
Tabelas PostgreSQL:
- `documents` - Documentos
- `ocr_results` - Resultados OCR
- `extracted_data` - Dados extraídos
- `document_classifications` - Classificações
- `analysis_results` - Análises IA
- `document_index` - Índice para busca

## 🚀 Instalação

### Pré-requisitos
- Python 3.11+
- PostgreSQL
- Redis
- Tesseract OCR
- Google Vision API key (opcional)
- OpenAI API key

### Setup

1. **Clonar e instalar dependências:**
```bash
cd products/tier3/ocr-processamento
pip install -r requirements.txt
```

2. **Configurar variáveis de ambiente:**
```bash
cp env.example .env
# Editar .env com suas credenciais
```

3. **Configurar banco de dados:**
```bash
# Criar banco de dados
createdb genesys_db

# Executar migrations (quando disponíveis)
alembic upgrade head
```

4. **Instalar Tesseract OCR:**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-por tesseract-ocr-eng

# macOS
brew install tesseract tesseract-lang
```

5. **Executar aplicação:**
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8001 --reload
```

## 📦 Docker

### Build Individual
```bash
# Build
docker build -t ocr-processamento .

# Run
docker run -p 8001:8001 --env-file .env ocr-processamento
```

### Docker Compose (Recomendado)
```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Serviços disponíveis:
# - API: http://localhost:8001
# - Flower (Celery Monitor): http://localhost:5555
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

## 🔧 Configuração

### Google Vision API
1. Criar projeto no Google Cloud
2. Habilitar Vision API
3. Criar chave de API
4. Adicionar `GOOGLE_VISION_API_KEY` no `.env`

### OpenAI
1. Obter API key em https://platform.openai.com
2. Adicionar `OPENAI_API_KEY` no `.env`

## 📊 Uso

### Upload de documento
```bash
curl -X POST "http://localhost:8001/api/documents/upload" \
  -F "file=@documento.pdf"
```

### Extrair dados
```bash
curl -X POST "http://localhost:8001/api/documents/1/extract"
```

### Análise IA
```bash
curl -X POST "http://localhost:8001/api/documents/1/analyze"
```

### Buscar documentos
```bash
curl "http://localhost:8001/api/documents/search?query=petição inicial"
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/

# Executar com coverage
pytest tests/ --cov=src --cov-report=html

# Executar testes específicos
pytest tests/test_document_uploader.py -v
```

## 🔄 Celery (Processamento Assíncrono)

### Iniciar Worker
```bash
# Script helper
./scripts/run_celery.sh

# Ou manualmente
celery -A src.celery_app worker --loglevel=info --concurrency=4
```

### Monitorar Tasks
```bash
# Flower (interface web)
celery -A src.celery_app flower

# Acesse: http://localhost:5555
```

Veja mais detalhes em [CELERY.md](./CELERY.md)

## 📈 Funcionalidades

- ✅ OCR multi-idioma (português e inglês)
- ✅ Extração de dados estruturados (prazos, valores, partes)
- ✅ Classificação automática de documentos
- ✅ Análise inteligente com GPT-4
- ✅ Busca semântica em documentos
- ✅ Processamento em lote
- ✅ Processamento assíncrono com Celery
- ✅ Cache com Redis

## 🎯 Roadmap

- [ ] Integração completa com banco de dados
- [ ] Sistema de filas com Celery
- [ ] Interface web para visualização
- [ ] Webhooks para notificações
- [ ] Integração com ClamAV para antivírus
- [ ] Suporte a mais formatos de arquivo
- [ ] Métricas e monitoramento

## 📝 Licença

Genesys Tecnologia - Todos os direitos reservados

## 👥 Equipe

Tier 3 - OCR & Processamento  
Versão: 1.0.0

