# 🚀 Genesys Products

Produtos separados e escaláveis da Genesys Tecnologia.

## 📦 Estrutura

```
products/
├── tier1/                  # Produtos TIER 1 (Backend completo)
│   ├── bot-telegram/       # Bot de Telegram Jurídico
│   ├── automacao-prazos/   # Automação de Prazos
│   └── assistente-virtual/ # Assistente 24/7
│
└── shared/                 # Código compartilhado
    ├── database/
    ├── config/
    └── utils/
```

## 🎯 Produtos Disponíveis

### 1. Bot de Telegram Jurídico
Assistente de IA para consultas jurídicas via Telegram.

**Deployment:**
- Backend: Python + FastAPI
- Database: PostgreSQL
- Infra: Docker

**URL:** `https://bot.genesys.com.br`

### 2. Automação de Prazos Processuais
Sistema inteligente de alertas para prazos.

**Deployment:**
- Backend: Python + FastAPI
- Frontend: Dashboard web próprio
- Database: PostgreSQL
- Infra: Docker

**URL:** `https://prazos.genesys.com.br`

### 3. Assistente Virtual 24/7
Chatbot inteligente para atendimento.

**Deployment:**
- Backend: Python + FastAPI
- Widget: Integrado ao site Genesys
- Database: PostgreSQL
- Infra: Docker

**URL:** `https://assistente.genesys.com.br`

## 🚀 Como Usar

Cada produto tem seu próprio README na pasta `tier1/`.

Consulte:
- [tier1/README.md](tier1/README.md) - Documentação completa
- [tier1/QUICKSTART.md](tier1/QUICKSTART.md) - Guia rápido

## 📊 Arquitetura Recomendada

```
genesys.com.br (Site institucional)
    ↓
    ├── Apresenta os produtos
    │   │
    │   ├── Bot de Telegram
    │   │   └── Redireciona para bot.genesys.com.br
    │   │
    │   ├── Automação de Prazos
    │   │   └── Redireciona para prazos.genesys.com.br
    │   │
    │   └── Assistente Virtual
    │       └── Widget embutido no site
    │
    ↓
Cada produto roda independente
```

## 🔧 Configuração

Cada produto tem seu próprio:
- `.env` (variáveis de ambiente)
- `docker-compose.yml` (deployment)
- `requirements.txt` (dependências)

## 📞 Contato

- **Email**: contato@genesys-tecnologia.com.br
- **WhatsApp**: +55 34 99826-4603

