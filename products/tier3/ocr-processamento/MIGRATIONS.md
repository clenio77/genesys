# 📦 Migrations - OCR & Processamento

## Como criar migrations

```bash
# Criar nova migration
alembic revision --autogenerate -m "Descrição da migration"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Ver histórico
alembic history

# Ver migration atual
alembic current
```

## Criar migration inicial

```bash
cd products/tier3/ocr-processamento
alembic revision --autogenerate -m "Initial migration - OCR tables"
alembic upgrade head
```

## Estrutura das tabelas

### documents
- id (PK)
- filename
- stored_filename
- file_path
- file_hash (unique)
- file_size
- file_type
- status
- uploaded_at
- processed_at

### ocr_results
- id (PK)
- document_id (FK)
- text
- confidence
- language
- method
- pages (JSON)
- created_at

### extracted_data
- id (PK)
- document_id (FK)
- field
- value
- confidence
- metadata (JSON)
- extracted_at

### document_classifications
- id (PK)
- document_id (FK)
- category
- confidence
- urgency
- urgency_confidence
- tags (JSON)
- classified_at

### analysis_results
- id (PK)
- document_id (FK)
- summary
- key_points (JSON)
- risk_score
- recommendations (JSON)
- sentiment
- confidence
- analyzed_at

### document_index
- id (PK)
- document_id (FK, unique)
- embeddings (JSON)
- metadata (JSON)
- indexed_at

