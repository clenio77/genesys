# 🚀 Como Iniciar o Bot - Passo a Passo

## ✅ Você já fez:
- [x] Criou o bot no @BotFather
- [x] Conseguiu o token

## 📝 Passo 1: Configurar o Token

### Editar o arquivo .env

```bash
nano products/tier1/.env
```

Ou abra no editor de código:
```bash
code products/tier1/.env
```

### Adicionar seu token

Encontre esta linha:
```bash
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

Substitua por (exemplo):
```bash
TELEGRAM_BOT_TOKEN=1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

**Salve o arquivo!** (Ctrl+O no nano, depois Ctrl+X)

## 📝 Passo 2: Instalar Dependências (Se ainda não instalou)

```bash
cd products/tier1

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

## 📝 Passo 3: Iniciar o Bot

### Opção A: Execução Direta (Recomendado para testes)

```bash
cd products/tier1

# Verificar se o token está configurado
python -c "from shared.config.settings import settings; print('✅ Token configurado!' if settings.TELEGRAM_BOT_TOKEN != 'your_telegram_bot_token_here' else '❌ Configure o token!')"

# Iniciar o bot
python bot-telegram/src/bot.py
```

### Opção B: Com Docker (Produção)

```bash
cd products/tier1

# Build da imagem
docker build -f bot-telegram/Dockerfile -t genesys-telegram-bot .

# Executar
docker run -d \
  --env-file .env \
  --name genesys-bot \
  genesys-telegram-bot

# Ver logs
docker logs -f genesys-bot
```

## ✅ Passo 4: Testar o Bot

1. **Abra o Telegram** no celular ou desktop
2. **Busque pelo username** que você criou (ex: genesys_legal_bot)
3. **Envie** `/start`
4. **Receba** a mensagem de boas-vindas!

## 🧪 Comandos para Testar

Teste estes comandos no Telegram:

```
/start
/help
/prazos
/alerta
/config
/perfil
```

**Teste de IA:**
```
Envie qualquer mensagem em linguagem natural, tipo:
"Como funciona a prescrição trabalhista?"
```

## 📊 Verificar se Está Funcionando

### Ver logs em tempo real:

Se executou com `python bot-telegram/src/bot.py`, os logs aparecem no terminal.

Se executou com Docker:
```bash
docker logs -f genesys-bot
```

### Procurar por mensagens de sucesso:
```
INFO: Bot iniciado com sucesso!
INFO: Usuário XXXXX enviou: ...
```

## 🐛 Problemas Comuns

### ❌ "TELEGRAM_BOT_TOKEN não configurado"

**Solução:** Edite o `.env` e adicione o token correto.

### ❌ "Erro de conexão com banco"

O bot funciona sem banco! As funcionalidades que precisam de DB mostrarão mensagens, mas o bot responde.

**Para ativar banco completo:**
```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Criar banco
sudo -u postgres psql -c "CREATE DATABASE genesys_db;"
sudo -u postgres psql -c "CREATE USER genesys WITH PASSWORD 'genesys';"

# Instalar Redis
sudo apt install redis-server
```

### ❌ "ModuleNotFoundError"

**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### ❌ Bot não responde

**Verificações:**
1. Bot está online? Olhe os logs
2. Token está correto? Use `/token` no @BotFather para gerar novo
3. Você está enviando mensagem para o bot correto?

## 🎯 Próximos Passos

Após confirmar que funciona:

1. ✅ **Testar comandos** básicos
2. ✅ **Adicionar API de IA** (OpenAI ou Gemini) para respostas inteligentes
3. ✅ **Configurar banco de dados** para salvar conversas
4. ✅ **Implementar funcionalidades** avançadas

## 📞 Precisa de Ajuda?

- **Token não funciona:** Use `/token` no @BotFather para gerar novo
- **Bot não responde:** Verifique logs com `docker logs genesys-bot`
- **Erro de importação:** Ative o ambiente virtual `source venv/bin/activate`

