# 🔗 INTEGRAÇÃO TIER 1 + TIER 2

## 📋 VISÃO GERAL

Documentação para integração completa entre TIER 1 e TIER 2.

---

## 🏗️ ARQUITETURA INTEGRADA

```
┌─────────────────────────────────────────────────────┐
│                  GENESYS ECOSYSTEM                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  TIER 1 - Core Services                            │
│  ├── Bot Telegram Jurídico                          │
│  ├── Automação de Prazos                           │
│  └── Assistente Virtual 24/7                        │
│                                                     │
│  TIER 2 - Advanced Services                         │
│  ├── Bot WhatsApp Business  ← NOVO                  │
│  └── Dashboard Analítico   ← NOVO                  │
│                                                     │
│  Shared Resources                                   │
│  ├── PostgreSQL Database                            │
│  ├── Redis Cache                                    │
│  └── Middleware (Segurança, Rate Limit)              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🔗 PONTOS DE INTEGRAÇÃO

### 1. Banco de Dados Compartilhado

**PostgreSQL:**
```python
# Todos os produtos compartilham o mesmo banco
DATABASE_URL=postgresql://genesys:genesys@localhost:5432/genesys_db

# Tabelas compartilhadas:
- users
- chats
- prazos
- processos
- consultas_jurisprudencia
- embeddings
```

### 2. Cache Compartilhado

**Redis:**
```python
REDIS_URL=redis://localhost:6379/0

# Cache compartilhado:
- Rate limiting
- Sessions
- Templates
- Analytics
```

### 3. Middleware Compartilhado

**Arquivos:**
```python
shared/middleware/
├── rate_limit.py     # Rate limiting
├── security.py       # HTTPS, CORS, Security headers
├── cache.py          # Redis cache
└── auth.py           # JWT authentication
```

---

## 📊 FLUXO DE DADOS

### Bot WhatsApp → Database

```python
# Bot WhatsApp salva conversas
Conversation → PostgreSQL
Messages → PostgreSQL
User → PostgreSQL

# Compartilha com outros serviços
Telegram Bot → Pode ver histórico WhatsApp
Dashboard → Mostra conversas WhatsApp
```

### Dashboard → Analytics

```python
# Dashboard agrega dados de TODOS os serviços
TIER 1:
- Bot Telegram → Messages
- Prazos → Deadlines
- Assistente → Leads

TIER 2:
- Bot WhatsApp → Messages
- Dashboard → KPIs

# Todos alimentam o Dashboard
```

---

## 🚀 DEPLOYMENT INTEGRADO

### Docker Compose Completo

```bash
# products/docker-compose.yml (pai)
version: '3.8'

services:
  postgres:
    # ...
  
  redis:
    # ...
  
  # TIER 1
  bot_telegram:     # Porta 8000
  automacao_prazos: # Porta 8001
  assistente_virtual: # Porta 8002
  
  # TIER 2
  bot_whatsapp:     # Porta 8003
  dashboard:        # Porta 8004
```

### Ordem de Startup

```bash
1. postgres → Base de dados
2. redis → Cache
3. TIER 1 services → Bot Telegram, Prazos, Assistente
4. TIER 2 services → Bot WhatsApp, Dashboard
```

---

## 📝 CONFIGURAÇÃO

### 1. Variáveis de Ambiente

**TIER 2 Bot WhatsApp:**
```bash
# .env em tier2/bot-whatsapp/
TWILIO_ACCOUNT_SID=xxx
TWILIO_AUTH_TOKEN=xxx
DATABASE_URL=postgresql://genesys:genesys@postgres:5432/genesys_db
REDIS_URL=redis://redis:6379/0
LLM_PROVIDER=openai
OPENAI_API_KEY=xxx
```

**TIER 2 Dashboard:**
```bash
# .env em tier2/dashboard-analytics/
DATABASE_URL=postgresql://genesys:genesys@postgres:5432/genesys_db
REDIS_URL=redis://redis:6379/0
```

### 2. Iniciar Serviços

```bash
# Opção 1: Docker Compose
cd products/tier2
docker-compose up -d

# Opção 2: Manual
python bot-whatsapp/src/bot.py &
python dashboard-analytics/src/app.py &
```

---

## 🔍 TESTES DE INTEGRAÇÃO

### Testar Bot WhatsApp

```bash
# 1. Verificar health
curl http://localhost:8003/health

# 2. Enviar mensagem (via webhook Twilio)
# Configurar webhook no Twilio

# 3. Verificar logs
docker logs genesys_whatsapp
```

### Testar Dashboard

```bash
# 1. Verificar health
curl http://localhost:8004/health

# 2. Obter KPIs
curl http://localhost:8004/api/kpis

# 3. Verificar dados
curl http://localhost:8004/api/analytics/summary
```

---

## 📊 MONITORAMENTO

### Health Checks

**Bot WhatsApp:**
- `http://localhost:8003/health`
- Status: online/offline
- Last message: timestamp

**Dashboard:**
- `http://localhost:8004/health`
- Status: online/offline
- Data freshness: timestamp

### Logs

```bash
# Ver todos os logs
docker-compose logs -f

# Ver logs específicos
docker logs genesys_whatsapp
docker logs genesys_dashboard
```

---

## ✅ CHECKLIST DE INTEGRAÇÃO

### Infraestrutura
- [x] Docker Compose configurado
- [x] PostgreSQL compartilhado
- [x] Redis compartilhado
- [x] Networks configuradas

### Serviços
- [x] Bot WhatsApp iniciando
- [x] Dashboard iniciando
- [x] Health checks funcionando
- [x] Logs configurados

### Dados
- [ ] Migrations rodadas
- [ ] Data seeding
- [ ] Backup configurado

### Testes
- [x] Testes unitários criados
- [ ] Testes de integração
- [ ] Testes E2E

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ **Testes Criados** - 40+ testes unitários
2. ⏳ **Executar Testes** - `pytest tests/`
3. ⏳ **Docker Compose** - Deploy integrado
4. ⏳ **Migrations** - Rodar no banco
5. ⏳ **Staging** - Deploy para testes

---

**Status:** Em progresso  
**Última atualização:** 2024-10-26

