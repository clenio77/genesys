# 🚀 TIER 1 - IMPLEMENTAÇÃO DETALHADA

## 📋 Visão Geral

TIER 1 representa os serviços de **máxima prioridade** para a Genesys Tecnologia, focando em alta demanda do mercado e máximo impacto.

## 🎯 Serviços Incluídos

### 1. **Bot de Telegram Jurídico**
- Chat com IA para consultas jurídicas
- Busca semântica em jurisprudência
- Alertas de prazos processuais
- Notificações de movimentações
- Integração com base de conhecimento

### 2. **Automação de Prazos Processuais**
- Sistema de alertas inteligente
- Integração com calendário jurídico
- Notificações via email e WhatsApp
- Dashboard de controle
- API REST para integrações

### 3. **Assistente Virtual 24/7**
- Chatbot inteligente multi-idioma
- Qualificação automática de leads
- Agendamento de reuniões
- FAQ com IA
- Análise de conversões

## 📁 Estrutura de Diretórios

```
tier1/
├── bot-telegram/          # Bot de Telegram Jurídico
│   ├── src/
│   │   ├── bot.py         # Inicialização do bot
│   │   ├── handlers/      # Handlers de comandos
│   │   ├── services/      # Serviços de IA
│   │   └── utils/         # Utilitários
│   ├── config.py          # Configurações
│   └── requirements.txt   # Dependências
│
├── automacao-prazos/      # Automação de Prazos
│   ├── src/
│   │   ├── scheduler.py  # Agendador de tarefas
│   │   ├── notifier.py   # Notificações
│   │   ├── parser.py    # Parsing de prazos
│   │   └── api.py       # API REST
│   ├── config.py
│   └── requirements.txt
│
├── assistente-virtual/    # Assistente 24/7
│   ├── src/
│   │   ├── chatbot.py    # Chatbot principal
│   │   ├── qualifier.py  # Qualificação de leads
│   │   ├── scheduler.py  # Agendamento
│   │   └── analytics.py  # Analytics
│   ├── config.py
│   └── requirements.txt
│
├── shared/                 # Código compartilhado
│   ├── config/
│   │   ├── database.py   # Config DB
│   │   └── settings.py   # Settings globais
│   ├── database/
│   │   ├── models.py     # Modelos SQLAlchemy
│   │   └── repository.py # Repositórios
│   └── utils/
│       ├── logger.py      # Logging
│       └── helpers.py     # Helpers
│
└── docs/
    ├── README_TIER1.md   # Este arquivo
    ├── API.md            # Documentação API
    ├── DATABASE.md       # Schema do banco
    └── DEPLOYMENT.md     # Guia de deploy
```

## 🗄️ Banco de Dados

### PostgreSQL Schema

#### Tabela: `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'user',
    token VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabela: `chats` (Histórico de conversas)
```sql
CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    service VARCHAR(50), -- 'telegram', 'whatsapp', 'web'
    message TEXT,
    response TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabela: `prazos`
```sql
CREATE TABLE prazos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    tipo VARCHAR(100),
    processo VARCHAR(50),
    tribunal VARCHAR(100),
    data_vencimento DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'pendente',
    alertas_enviados INTEGER DEFAULT 0,
    ultima_notificacao TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabela: `notificacoes`
```sql
CREATE TABLE notificacoes (
    id SERIAL PRIMARY KEY,
    prazo_id INTEGER REFERENCES prazos(id),
    user_id INTEGER REFERENCES users(id),
    canal VARCHAR(50), -- 'email', 'whatsapp', 'telegram'
    mensagem TEXT,
    status VARCHAR(50) DEFAULT 'enviada',
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabela: `alertas`
```sql
CREATE TABLE alertas (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    tipo VARCHAR(100), -- 'prazo', 'movimentacao', 'legislativo'
    titulo VARCHAR(255),
    mensagem TEXT,
    prioridade VARCHAR(50),
    lido BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabela: `consultas_jurisprudencia`
```sql
CREATE TABLE consultas_jurisprudencia (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    query TEXT,
    results JSONB,
    service VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🔧 Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **FastAPI** - API REST
- **SQLAlchemy** - ORM
- **PostgreSQL** - Banco de dados
- **Redis** - Cache e filas
- **Celery** - Tasks assíncronas

### Bot de Telegram
- **python-telegram-bot** - Framework
- **LangChain** - RAG e LLM
- **FAISS** - Vector store

### Automação de Prazos
- **APScheduler** - Agendamento
- **Pandas** - Manipulação de dados
- **ReportLab** - PDF generation

### Assistente Virtual
- **Dialogflow** ou **Rasa** - NLP
- **OpenAI/Gemini** - LLM
- **WebSocket** - Real-time

## 🚀 Como Executar

### Pré-requisitos
```bash
# PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Redis
sudo apt-get install redis-server

# Python 3.11+
sudo apt-get install python3.11 python3-pip
```

### Instalação
```bash
# Clone o repositório
git clone https://github.com/genesys/genesys-tier1

# Entre no diretório
cd tier1

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
nano .env

# Inicie banco de dados
docker-compose up -d postgres redis

# Execute migrações
alembic upgrade head

# Inicie os serviços
python bot-telegram/src/bot.py &
python automacao-prazos/src/scheduler.py &
python assistente-virtual/src/chatbot.py &
```

## 📊 Métricas e Monitoramento

### KPIs Principais
- **Bot Telegram**: Número de consultas/mês
- **Automação Prazos**: Taxa de alertas enviados
- **Assistente Virtual**: Taxa de conversão de leads

### Ferramentas
- **Prometheus** - Métricas
- **Grafana** - Dashboards
- **Sentry** - Error tracking

## 💰 Custos Estimados

| Serviço | Infra/mês | Desenvolvimento |
|---------|-----------|-----------------|
| Bot Telegram | R$ 500-800 | 80-120h |
| Automação Prazos | R$ 600-1k | 100-150h |
| Assistente 24/7 | R$ 700-1.2k | 120-160h |

## 📝 Próximos Passos

1. ✅ Criar estrutura de pastas
2. ⏳ Configurar banco de dados
3. ⏳ Implementar Bot de Telegram
4. ⏳ Implementar Automação de Prazos
5. ⏳ Implementar Assistente Virtual
6. ⏳ Configurar Docker
7. ⏳ Deploy em produção

