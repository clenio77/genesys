# 📦 Guia de Deploy do Bot Telegram - Estrutura Necessária

## ⚠️ Importante: Você NÃO precisa apenas da pasta `bot-telegram/`

O bot do Telegram possui **dependências obrigatórias** de outras pastas do projeto.

## 📁 Estrutura Mínima Necessária para Deploy

Para hospedar o bot, você precisa das seguintes pastas/arquivos:

### ✅ Pastas Obrigatórias

```
tier1/
├── bot-telegram/          # ✅ Código do bot (obrigatório)
│   ├── src/
│   │   ├── bot.py
│   │   ├── handlers/
│   │   ├── services/
│   │   └── requirements.txt
│   └── Dockerfile
│
├── shared/                # ✅ Código compartilhado (OBRIGATÓRIO)
│   ├── config/
│   │   ├── settings.py    # Configurações do sistema
│   │   └── database.py   # Configuração do banco
│   ├── database/
│   │   └── models.py      # Modelos SQLAlchemy
│   └── utils/
│       └── logger.py      # Sistema de logging
│
└── config/                # ✅ Configurações (opcional, mas recomendado)
    ├── requirements.txt   # Dependências principais
    ├── alembic.ini        # Migrações do banco
    └── env.example        # Exemplo de variáveis de ambiente
```

## 🔍 Por que precisa da pasta `shared/`?

O bot importa diretamente módulos de `shared/`:

```python
from shared.config.settings import settings
from shared.utils.logger import bot_telegram_logger as logger
from shared.config.database import get_db
from shared.database.models import User, Chat, Prazo, Notificacao
```

**Sem a pasta `shared/`, o bot não funcionará!**

## 🚀 Opções de Deploy

### Opção 1: Deploy Completo (Recomendado)

Incluir toda a estrutura `tier1/` no servidor:

```bash
# Estrutura no servidor:
/app/
├── bot-telegram/
├── shared/
└── config/
```

**Vantagens:**
- ✅ Funciona imediatamente
- ✅ Acesso a todas as configurações
- ✅ Fácil manutenção

### Opção 2: Deploy Mínimo (Apenas Bot + Shared)

Copiar apenas o necessário:

```bash
# No servidor, criar estrutura mínima:
/app/
├── bot-telegram/
│   └── src/
│       └── bot.py
└── shared/
    ├── config/
    ├── database/
    └── utils/
```

**Importante:** Ajustar `PYTHONPATH` para incluir `/app` na raiz.

## 🐳 Docker - Ajuste Necessário

O `Dockerfile` atual precisa ser modificado para incluir a pasta `shared/`.

### Dockerfile Corrigido para Deploy

Se você vai fazer deploy APENAS com `bot-telegram/`, precisa modificar o Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar código do bot
COPY bot-telegram/src/ ./bot-telegram/src/
COPY shared/ ./shared/
COPY config/requirements.txt ./requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Comando para iniciar o bot
WORKDIR /app/bot-telegram
CMD ["python", "src/bot.py"]
```

**OU** se tiver toda a estrutura `tier1/`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar tudo (estrutura completa)
COPY . .

# Instalar dependências
RUN pip install --no-cache-dir -r config/requirements.txt && \
    pip install -r bot-telegram/src/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app/bot-telegram
CMD ["python", "src/bot.py"]
```

## 📝 Checklist para Deploy

### Antes de fazer deploy:

- [ ] **Pasta `bot-telegram/`** com todo o código fonte
- [ ] **Pasta `shared/`** completa (config, database, utils)
- [ ] **Arquivo `.env`** com variáveis de ambiente:
  - `TELEGRAM_BOT_TOKEN`
  - `DATABASE_URL`
  - `REDIS_URL` (opcional)
  - `OPENAI_API_KEY` ou `GEMINI_API_KEY`
- [ ] **Banco de dados PostgreSQL** configurado
- [ ] **Migrações do banco** executadas (`alembic upgrade head`)
- [ ] **Requirements.txt** acessível (em `config/` ou copiado)

### Variáveis de Ambiente Mínimas

```bash
TELEGRAM_BOT_TOKEN=seu_token_aqui
DATABASE_URL=postgresql://user:password@host:5432/database
# Escolha um:
OPENAI_API_KEY=sua_chave  # OU
GEMINI_API_KEY=sua_chave
```

## 🏗️ Estrutura para Render.com / Heroku / Railway

Para serviços como Render, você pode:

### Opção A: Repositório Completo
- Fazer deploy de toda a pasta `tier1/`
- Configurar `Start Command`: `cd bot-telegram && python src/bot.py`

### Opção B: Apenas Bot + Shared
- Criar um repositório com apenas:
  ```
  bot-telegram/
  shared/
  requirements.txt  (copiado de config/)
  .env
  ```

## 🔧 Comando de Start para Render

Se usar Render.com com estrutura completa:

```bash
cd bot-telegram && python src/bot.py
```

**OU** se todas as pastas estiverem na raiz:

```bash
python bot-telegram/src/bot.py
```

## ❌ O que NÃO precisa

Você **NÃO precisa** para o bot funcionar:
- ❌ `assistente-virtual/`
- ❌ `automacao-prazos/`
- ❌ `tests/`
- ❌ `docs/`
- ❌ `documentacao/`
- ❌ `relatorios/`
- ❌ `scripts/`
- ❌ `logs/` (criado automaticamente)
- ❌ `venv/`

## ✅ Resumo Final

**Mínimo necessário:**
1. ✅ `bot-telegram/` (código do bot)
2. ✅ `shared/` (módulos compartilhados - OBRIGATÓRIO)
3. ✅ `.env` (variáveis de ambiente)
4. ✅ `requirements.txt` (dependências Python)

**Recomendado adicional:**
- `config/alembic.ini` (para migrações)
- `config/requirements.txt` (dependências principais)

**IMPORTANTE:** Não tente fazer deploy apenas com `bot-telegram/`. Sem `shared/`, o bot não iniciará!

