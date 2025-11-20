# 📦 Instalar Dependências do Bot

## 🚀 Instalação Rápida

### Passo 1: Criar Ambiente Virtual

```bash
cd products/tier1
python3 -m venv venv
```

### Passo 2: Ativar Ambiente Virtual

```bash
source venv/bin/activate
```

Você verá `(venv)` no início do prompt.

### Passo 3: Instalar Dependências

```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências principais
pip install -r requirements.txt

# Instalar dependências específicas do bot
pip install -r bot-telegram/src/requirements.txt
```

## 🐳 OU: Usar Docker (Mais Simples)

```bash
cd products/tier1

# Build e Run
docker-compose up -d bot-telegram

# Ver logs
docker-compose logs -f bot-telegram
```

## ✅ Verificar Instalação

```bash
# Verificar se está instalado
python3 -c "import telegram; print('✅ Telegram instalado')"
python3 -c "import openai; print('✅ OpenAI instalado')"
python3 -c "import google.generativeai; print('✅ Gemini instalado')"
```

## 📋 Dependências Principais

- `python-telegram-bot==20.7` - Bot do Telegram
- `openai==1.3.9` - API OpenAI
- `google-generativeai==0.3.0` - API Gemini
- `langchain` - Framework de IA
- `faiss-cpu==1.7.4` - Busca vetorial
- `SQLAlchemy` - ORM para banco de dados
- `psycopg2` - Driver PostgreSQL
- `redis` - Cache
- `APScheduler` - Agendamento de tarefas

## 🎯 Próximo Passo

Após instalar as dependências, execute:

```bash
python3 bot-telegram/src/bot.py
```

