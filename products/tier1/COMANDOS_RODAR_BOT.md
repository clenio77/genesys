# 🚀 Comandos para Rodar o Bot

## 📋 Opções Disponíveis

### Opção 1: Script Rápido (bot_com_ia.py - Recomendado)

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
./scripts/ativar_bot_ia.sh
```

**Ou manualmente:**
```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
source venv/bin/activate
export PYTHONPATH=$(pwd)
python bot-telegram/src/bot_com_ia.py
```

---

### Opção 2: Script Alternativo (bot.py)

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
./scripts/start_bot.sh
```

**Ou manualmente:**
```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
source venv/bin/activate
export PYTHONPATH=$(pwd)
python bot-telegram/src/bot.py
```

---

## ⚙️ Configuração Necessária

### 1. Variáveis de Ambiente (arquivo `.env`)

Certifique-se de ter o arquivo `.env` na raiz do projeto com:

```bash
TELEGRAM_BOT_TOKEN=seu_token_aqui
GEMINI_API_KEY=sua_chave_gemini
# OU
OPENAI_API_KEY=sua_chave_openai

DATABASE_URL=postgresql://user:pass@localhost:5432/database
# OU para SQLite
# DATABASE_URL=sqlite:///./bot.db
```

### 2. Banco de Dados

Se estiver usando PostgreSQL, certifique-se de que:
- PostgreSQL está rodando
- Banco de dados existe
- Tabelas criadas (rodar migrações se necessário)

**Para SQLite:**
```bash
# Não precisa de nada - cria automaticamente
```

---

## 🔧 Verificar Configuração

### Testar se tudo está OK:

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1

# Verificar .env
[ -f .env ] && echo "✅ .env existe" || echo "❌ .env não encontrado"

# Verificar venv
[ -d venv ] && echo "✅ venv existe" || echo "❌ venv não encontrado"

# Testar importações
source venv/bin/activate
python -c "from shared.config.settings import settings; print('✅ Imports OK')"
```

---

## 🐛 Troubleshooting

### Erro: "TELEGRAM_BOT_TOKEN não configurado"
**Solução:** Criar/atualizar arquivo `.env` com o token

### Erro: "ModuleNotFoundError: No module named 'shared'"
**Solução:** 
```bash
export PYTHONPATH=$(pwd)
```

### Erro: "connection to server failed" (PostgreSQL)
**Soluções:**
- Verificar se PostgreSQL está rodando: `sudo systemctl status postgresql`
- Usar SQLite temporariamente: `DATABASE_URL=sqlite:///./bot.db`
- Verificar credenciais no `.env`

### Erro: "No such table: users"
**Solução:** Rodar migração ou criar tabelas:
```bash
# Se usar Alembic
alembic upgrade head

# OU criar manualmente (SQLite)
python -c "from shared.config.database import init_db; init_db(); print('✅ Tabelas criadas')"
```

---

## 📝 Logs

O bot salva logs automaticamente em:
- Console (stdout)
- Arquivo: `logs/bot_telegram.log`

---

## ✅ Comando Mais Rápido (Recomendado)

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1 && ./scripts/ativar_bot_ia.sh
```

---

**Última atualização:** 2025-10-29

