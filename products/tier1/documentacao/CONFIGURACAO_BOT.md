# ⚙️ Configuração do Bot de Telegram

## 📍 Localização do arquivo `.env`

O arquivo `.env` foi criado em: `/home/clenio/Documentos/Meusagentes/genesys/products/tier1/.env`

## 🔧 Configuração Necessária

### 1. Obter Token do Bot

1. Abra o Telegram e busque por **@BotFather**
2. Envie `/newbot`
3. Escolha um nome para seu bot (ex: Genesys Bot)
4. Escolha um username único (ex: genesys_legal_bot)
5. Copie o token fornecido

### 2. Editar o arquivo `.env`

```bash
nano products/tier1/.env
```

### 3. Variáveis OBRIGATÓRIAS para o Bot

```bash
# Telegram Bot (OBRIGATÓRIO)
TELEGRAM_BOT_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# AI Provider (escolha UM)
OPENAI_API_KEY=sk-proj-...    # OU
GEMINI_API_KEY=AIza...         # (Mais barato)
```

### 4. Configurações Opcionais

```bash
# Database (se já tiver configurado)
DATABASE_URL=postgresql://genesys:genesys@localhost:5432/genesys_db

# Redis (se já tiver configurado)
REDIS_URL=redis://localhost:6379/0
```

## 🚀 Como Editar o .env

### Opção 1: Editor de Texto

```bash
nano products/tier1/.env
# ou
code products/tier1/.env
```

### Opção 2: Via Terminal (substituir valores)

```bash
# Substituir token do Telegram
sed -i 's/TELEGRAM_BOT_TOKEN=.*/TELEGRAM_BOT_TOKEN=SEU_TOKEN_AQUI/' products/tier1/.env

# Substituir API key
sed -i 's/OPENAI_API_KEY=.*/OPENAI_API_KEY=sua_chave_aqui/' products/tier1/.env
```

## ✅ Testar Configuração

Após configurar, verifique se está tudo certo:

```bash
cd products/tier1
python -c "from shared.config.settings import settings; print(f'Token: {settings.TELEGRAM_BOT_TOKEN[:10]}...' if settings.TELEGRAM_BOT_TOKEN else '❌ Token não configurado')"
```

## 🎯 Configuração Mínima para Testar

**Para testar o bot sem IA:**

```bash
# Edite apenas esta linha:
TELEGRAM_BOT_TOKEN=seu_token_aqui
```

O bot funcionará, mas com respostas básicas (sem IA).

**Para usar IA:**

Adicione uma das duas:
```bash
OPENAI_API_KEY=sk-proj-...     # Recomendado
GEMINI_API_KEY=AIza...         # Mais barato
```

## 📝 Exemplo Completo

```bash
# Bot básico funcionando
TELEGRAM_BOT_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Com IA gratuita (Gemini)
GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnop

# Banco de dados local
DATABASE_URL=postgresql://genesys:genesys@localhost:5432/genesys_db
REDIS_URL=redis://localhost:6379/0

ENABLE_TELEGRAM_BOT=true
LOG_LEVEL=INFO
```

## 🔒 Segurança

⚠️ **IMPORTANTE:**
- Nunca commite o arquivo `.env` no Git
- O arquivo `.env` já está no `.gitignore`
- Não compartilhe suas API keys

## 📞 Precisa de Ajuda?

Se tiver dificuldades para obter o token ou configuração:

1. **Token do Telegram:** @BotFather no Telegram
2. **OpenAI API:** https://platform.openai.com/api-keys
3. **Google Gemini:** https://makersuite.google.com/app/apikey

