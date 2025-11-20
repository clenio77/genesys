# 🚀 SETUP - OCR & Processamento

## Pré-requisitos

- Python 3.11+
- PostgreSQL 12+
- Redis (opcional, para cache)
- Tesseract OCR instalado

## Instalação Rápida

### 1. Instalar Dependências do Sistema

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    poppler-utils \
    libpoppler-cpp-dev \
    libtesseract-dev \
    libleptonica-dev \
    postgresql \
    postgresql-contrib
```

**macOS:**
```bash
brew install tesseract tesseract-lang poppler postgresql
```

### 2. Configurar PostgreSQL

```bash
# Criar banco de dados
sudo -u postgres createdb genesys_db

# Criar usuário (se necessário)
sudo -u postgres psql -c "CREATE USER genesys WITH PASSWORD 'genesys';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE genesys_db TO genesys;"
```

### 3. Instalar Dependências Python

```bash
cd products/tier3/ocr-processamento
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
cp env.example .env
# Editar .env com suas credenciais
```

**Variáveis importantes:**
- `DATABASE_URL` - URL do PostgreSQL
- `OPENAI_API_KEY` - Para análise IA (opcional)
- `GOOGLE_VISION_API_KEY` - Para OCR avançado (opcional)

### 5. Inicializar Banco de Dados

**Opção 1: Usando script**
```bash
python scripts/init_db.py
```

**Opção 2: Usando Alembic**
```bash
# Criar migration inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migration
alembic upgrade head
```

### 6. Executar Aplicação

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8001 --reload
```

A API estará disponível em: `http://localhost:8001`

## Verificação

### Health Check
```bash
curl http://localhost:8001/health
```

### Documentação API
Acesse: `http://localhost:8001/docs` (Swagger UI)

## Uso Básico

### Upload de Documento
```bash
curl -X POST "http://localhost:8001/api/documents/upload" \
  -F "file=@documento.pdf"
```

### Listar Documentos
```bash
curl "http://localhost:8001/api/documents/"
```

### Buscar Documentos
```bash
curl "http://localhost:8001/api/documents/search?query=petição"
```

## Docker

### Build
```bash
docker build -t ocr-processamento .
```

### Run
```bash
docker run -p 8001:8001 --env-file .env ocr-processamento
```

## Troubleshooting

### Erro: Tesseract não encontrado
```bash
# Verificar instalação
tesseract --version

# Verificar idiomas instalados
tesseract --list-langs
```

### Erro: PostgreSQL connection
- Verificar se PostgreSQL está rodando
- Verificar `DATABASE_URL` no `.env`
- Verificar permissões do usuário

### Erro: OpenAI API
- Verificar `OPENAI_API_KEY` no `.env`
- Sistema funciona sem OpenAI (usando fallback)

## Próximos Passos

1. ✅ Setup completo
2. ⏳ Configurar Celery para processamento assíncrono
3. ⏳ Adicionar testes
4. ⏳ Configurar CI/CD
5. ⏳ Deploy em produção

