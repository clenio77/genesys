# 📖 GUIA DE USO - RAG Avançado

## 🚀 Quick Start

### 1. Instalação
```bash
cd products/tier3/rag-avancado
pip install -r requirements.txt
```

### 2. Configuração
```bash
cp env.example .env
# Editar .env:
# - DATABASE_URL
# - OPENAI_API_KEY
# - CHROMADB_PATH (verificar path do Kermartin)
```

### 3. Iniciar Servidor
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8002 --reload
```

### 4. Acessar Documentação
- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc

---

## 📡 API REST

### 1. Consulta RAG
```bash
curl -X POST "http://localhost:8002/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Qual a jurisprudência sobre dano moral em caso de atraso de voo?",
    "session_id": "user_123"
  }'
```

**Resposta:**
```json
{
  "success": true,
  "query_id": 1,
  "query": "Qual a jurisprudência sobre dano moral...",
  "answer": "De acordo com a jurisprudência...",
  "confidence": 0.89,
  "citations": [
    {
      "document_number": 1,
      "citation_abnt": "TJSP. Processo 1234567...",
      "excerpt": "..."
    }
  ],
  "metadata": {
    "documents_found": 5,
    "processing_time_ms": 1234
  }
}
```

### 2. Histórico
```bash
curl "http://localhost:8002/api/rag/history?session_id=user_123&limit=10"
```

### 3. Citações
```bash
curl "http://localhost:8002/api/rag/citations/1"
```

### 4. Feedback
```bash
curl -X POST "http://localhost:8002/api/rag/feedback/1" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "is_helpful": true,
    "comment": "Resposta muito útil!"
  }'
```

### 5. Indexar Documento
```bash
curl -X POST "http://localhost:8002/api/rag/index" \
  -H "Content-Type: application/json" \
  -d '{
    "document_id": "doc_001",
    "content": "Texto do documento...",
    "metadata": {
      "tipo": "jurisprudencia",
      "tribunal": "TJMG"
    }
  }'
```

### 6. Estatísticas
```bash
curl "http://localhost:8002/api/rag/stats"
```

---

## 💬 WebSocket Chat

### Cliente Python
```python
import asyncio
import websockets
import json

async def chat():
    uri = "ws://localhost:8002/ws/chat/my_session"
    
    async with websockets.connect(uri) as websocket:
        # Enviar mensagem
        await websocket.send(json.dumps({
            "type": "message",
            "content": "Como funciona recurso de apelação?"
        }))
        
        # Receber respostas
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            
            print(f"Tipo: {data['type']}")
            
            if data['type'] == 'answer':
                print(f"Resposta: {data['answer']}")
                break
            elif data['type'] == 'status':
                print(f"Status: {data['message']}")

asyncio.run(chat())
```

### Cliente JavaScript
```javascript
const ws = new WebSocket('ws://localhost:8002/ws/chat/my_session');

ws.onopen = () => {
    ws.send(JSON.stringify({
        type: 'message',
        content: 'Como funciona recurso de apelação?'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Tipo:', data.type);
    
    if (data.type === 'answer') {
        console.log('Resposta:', data.answer);
    } else if (data.type === 'status') {
        console.log('Status:', data.message);
    }
};
```

---

## 🧪 Testes

### Teste de Integração ChromaDB
```bash
python tests/test_chromadb_integration.py
```

### Teste de API
```bash
pytest tests/ -v
```

---

## 🔧 Troubleshooting

### ChromaDB não encontrado
```bash
# Verificar path
ls -la /home/clenio/Documentos/Meusagentes/kermartin/knowledge_base/chroma/

# Atualizar .env
CHROMADB_PATH=/caminho/correto/para/chroma
```

### OpenAI API Error
```bash
# Verificar API key
echo $OPENAI_API_KEY

# Testar API
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### PostgreSQL Connection Error
```bash
# Verificar PostgreSQL
psql -U genesys -d genesys_db -h localhost

# Verificar DATABASE_URL
echo $DATABASE_URL
```

---

## 📚 Exemplos Avançados

### Consulta com Contexto
```python
import requests

response = requests.post("http://localhost:8002/api/rag/query", json={
    "query": "E sobre recursos?",
    "session_id": "user_123",
    "context": {
        "conversation_history": [
            {"query": "Como funciona apelação?", "answer": "..."}
        ]
    }
})
```

### Busca por Magistrado
```bash
curl -X POST "http://localhost:8002/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Qual o perfil de decisões do magistrado João Silva?"
  }'
```

### Análise de Tendência
```bash
curl -X POST "http://localhost:8002/api/rag/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Qual a tendência de decisões sobre dano moral no TJMG em 2023?"
  }'
```

---

## 💡 Dicas

1. **Use session_id** para manter contexto entre queries
2. **Forneça feedback** para melhorar o sistema
3. **Consulte citações** para referências completas
4. **Use WebSocket** para interações em tempo real
5. **Monitore stats** para acompanhar performance

---

**Versão:** 1.0.0  
**Data:** 2024-10-26

