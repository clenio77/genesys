# 🔄 Celery - Processamento Assíncrono

## Configuração

O sistema usa Celery para processamento assíncrono de documentos, permitindo que operações pesadas sejam executadas em background sem bloquear a API.

## Arquitetura

### Queues (Filas)
- `documents` - Processamento completo de documentos
- `extraction` - Extração de dados
- `analysis` - Análise com IA
- `batch` - Processamento em lote

### Tasks Disponíveis

1. **process_document_task** - Processa documento completo
   - OCR
   - Extração de dados
   - Classificação
   - Análise IA
   - Indexação

2. **extract_data_task** - Extrai dados estruturados
   - Processa OCR se necessário
   - Extrai prazos, valores, partes, etc.

3. **analyze_document_task** - Análise com IA
   - Gera resumo
   - Calcula risco
   - Gera recomendações

4. **batch_process_task** - Processa lote de documentos
   - Enfileira múltiplos documentos
   - Retorna status de cada um

5. **index_document_task** - Indexa documento para busca
   - Gera embeddings
   - Salva índice

## Execução

### Iniciar Worker

```bash
# Opção 1: Script bash
./scripts/run_celery.sh

# Opção 2: Comando direto
celery -A src.celery_app worker \
    --loglevel=info \
    --concurrency=4 \
    --queues=documents,extraction,analysis,batch
```

### Monitorar Tasks

**Usando Flower (recomendado):**
```bash
celery -A src.celery_app flower
```

Acesse: `http://localhost:5555`

**Via API:**
```bash
# Verificar status de uma task
curl http://localhost:8001/api/tasks/{task_id}
```

## Uso na API

### Upload com Processamento Assíncrono

```bash
curl -X POST "http://localhost:8001/api/documents/upload" \
  -F "file=@documento.pdf"
```

Resposta inclui `task_id`:
```json
{
  "success": true,
  "document_id": 1,
  "task_id": "abc123-def456-...",
  "message": "Documento enviado com sucesso. Processamento em andamento."
}
```

### Verificar Status

```bash
curl "http://localhost:8001/api/tasks/abc123-def456-..."
```

### Processar Lote

```bash
curl -X POST "http://localhost:8001/api/documents/batch" \
  -H "Content-Type: application/json" \
  -d '{"document_ids": [1, 2, 3]}'
```

## Configuração

### Variáveis de Ambiente

```bash
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
ENABLE_BATCH_PROCESSING=True
```

### Timeouts

- **Task Time Limit:** 30 minutos
- **Task Soft Time Limit:** 25 minutos
- **Max Retries:** 3 tentativas

## Monitoramento

### Logs

Worker logs mostram:
- Tasks iniciadas
- Progresso
- Erros
- Tempo de execução

### Métricas

Flower fornece:
- Tasks por segundo
- Worker status
- Queue length
- Task history

## Troubleshooting

### Worker não inicia
- Verificar Redis está rodando
- Verificar `CELERY_BROKER_URL` correto
- Verificar dependências instaladas

### Tasks ficam pendentes
- Verificar worker está rodando
- Verificar queue name correto
- Verificar conexão com Redis

### Tasks falham
- Verificar logs do worker
- Verificar banco de dados acessível
- Verificar APIs externas (OpenAI, Google Vision)

