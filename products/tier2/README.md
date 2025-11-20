# 🚀 TIER 2 - Genesys Tecnologia

Produtos avançados de automação e analytics para escritórios jurídicos.

## 📦 PRODUTOS

### 1. 🤖 Bot WhatsApp Business
Atendimento automatizado 24/7 com IA integrada.

### 2. 📊 Dashboard Analítico Jurídico
BI e analytics em tempo real para escritórios.

---

## 🚀 QUICK START

### Setup Completo

```bash
# 1. Instalar dependências
cd products/tier2
pip install -r bot-whatsapp/requirements.txt
pip install -r dashboard-analytics/requirements.txt

# 2. Configurar ambiente
cp bot-whatsapp/env.example bot-whatsapp/.env
cp dashboard-analytics/env.example dashboard-analytics/.env

# Editar com suas credenciais
nano bot-whatsapp/.env
nano dashboard-analytics/.env

# 3. Iniciar com Docker
docker-compose up -d

# 4. Verificar serviços
curl http://localhost:8003/health  # Bot WhatsApp
curl http://localhost:8004/health  # Dashboard
```

---

## 📊 ARQUITETURA

Todos os produtos seguem **METHOD-BMAD**:
- **B** - Backend: FastAPI
- **M** - Modelo: Microserviços
- **A** - API: RESTful
- **D** - Data: PostgreSQL + Redis

---

## 🔗 INTEGRAÇÃO COM TIER 1

### Banco de Dados Compartilhado

```python
# Todos usam o mesmo PostgreSQL
DATABASE_URL=postgresql://genesys:genesys@localhost:5432/genesys_db

# Tabelas compartilhadas:
- users, chats, prazos
- consultas_jurisprudencia
- lead_qualifications
```

### Cache Compartilhado

```python
# Redis compartilhado
REDIS_URL=redis://localhost:6379/0

# Rate limiting distribuído
# Cache de respostas
# Analytics cache
```

---

## 🧪 TESTES

```bash
# Executar testes
pytest tests/ -v

# Com coverage
pytest tests/ --cov=src --cov-report=html
```

---

## 📚 DOCUMENTAÇÃO

- [Arquitetura Completa](./ARQUITETURA_TIER2_BMAD.md)
- [Produtos Sugeridos](./PRODUTOS_SUGERIDOS.md)
- [Integração TIER1+TIER2](./INTEGRACAO_TIER1_TIER2.md)
- [Resumo Executivo](./RESUMO_EXECUTIVO.md)

---

## 🎯 STATUS

- ✅ Arquitetura definida
- ✅ Bot WhatsApp implementado
- ✅ Dashboard implementado
- ✅ Testes criados
- ✅ Documentação completa
- ⏳ Deploy staging

---

**Desenvolvido por:** Genesys Tecnologia  
**Versão:** 1.0.0

