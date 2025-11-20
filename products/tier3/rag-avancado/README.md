# 🧠 RAG Avançado - Genesys

## 📋 Visão Geral

Sistema avançado de Retrieval-Augmented Generation (RAG) para consultas jurídicas inteligentes, integrado com a base de conhecimento do Kermartin.

## ✨ Funcionalidades

### 1. Consultas Semânticas
- Perguntas em linguagem natural
- Busca avançada com ChromaDB
- Ranking por relevância
- Contexto jurídico completo

### 2. Análise de Jurisprudência
- Padrões de decisões
- Teses vencedoras
- Perfil de magistrados
- Tendências temporais

### 3. Citações Automáticas
- Formato ABNT
- Links para processos
- Metadados completos
- Exportação

### 4. Chat Interativo
- WebSocket em tempo real
- Histórico de conversação
- Sugestões contextuais
- Refinamento iterativo

## 🏗️ Arquitetura METHOD-BMAD

### Backend
- FastAPI
- LangChain
- OpenAI GPT-4
- ChromaDB (Kermartin)
- PostgreSQL

### Microserviços (6)
1. **Query Processor** - Processa consultas
2. **Retriever** - Busca documentos
3. **Context Builder** - Constrói contexto
4. **Answer Generator** - Gera respostas
5. **Citation Manager** - Gerencia citações
6. **Feedback Collector** - Coleta feedback

### API (6 endpoints + WebSocket)
- `POST /api/rag/query` - Consulta semântica
- `POST /api/rag/index` - Indexar documento
- `GET /api/rag/history` - Histórico
- `GET /api/rag/citations` - Citações
- `POST /api/rag/feedback` - Feedback
- `WebSocket /ws/chat` - Chat tempo real

### Data
- ChromaDB (embeddings)
- PostgreSQL (cache, histórico)
- Redis (sessões)

## 🔄 Integração com Kermartin

### Base Compartilhada
```python
CHROMADB_PATH = "/home/clenio/Documentos/Meusagentes/kermartin/knowledge_base/chroma/"
```

### Coleções Disponíveis
- `processos_juridicos` - Processos coletados
- `jurisprudencias` - Decisões judiciais
- `perfis_magistrados` - Perfis de magistrados
- `decisoes_judiciais` - Base de decisões

## 🚀 Quick Start

### Instalação
```bash
cd products/tier3/rag-avancado
pip install -r requirements.txt
```

### Configuração
```bash
cp env.example .env
# Editar .env com suas credenciais
```

### Executar
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8002 --reload
```

## 📊 Status

**Versão:** 1.0.0  
**Status:** 🚧 Em Desenvolvimento  
**Progresso:** 0% → 100%

## 📝 Documentação

- [Instalação e Setup](./SETUP.md)
- [Guia de Uso](./USAGE.md)
- [API Reference](./API.md)
- [Integração Kermartin](./INTEGRACAO_KERMARTIN.md)

## 💰 Modelo de Negócio

**Receita Esperada:** $75,000/mês  
**Investimento:** $400-1,750/mês  
**ROI:** 4,200%+

**Público-Alvo:**
- Escritórios de advocacia
- Departamentos jurídicos
- Pesquisadores
- Estudantes de direito

## 🎯 Roadmap

- [x] Estrutura base criada
- [ ] Microserviços implementados
- [ ] Integração ChromaDB Kermartin
- [ ] API endpoints
- [ ] WebSocket chat
- [ ] Testes
- [ ] Deploy

---

**Desenvolvido por:** Genesys Tecnologia  
**Data:** 2024-10-26

