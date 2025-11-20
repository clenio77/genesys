# 🤖 Bot de Telegram Jurídico - Genesys Tecnologia

Bot inteligente de Telegram para consultas jurídicas com IA integrada.

## ✨ Funcionalidades

### 🧠 Inteligência Artificial
- ✅ Respostas inteligentes usando OpenAI GPT-4 ou Google Gemini
- ✅ Processamento de linguagem natural
- ✅ Contexto jurídico especializado
- ✅ Fallback automático quando IA não está disponível

### 📋 Comandos Disponíveis
- `/start` - Iniciar o bot
- `/help` - Ver ajuda completa
- `/buscar` - Buscar jurisprudência
- `/prazos` - Ver prazos processuais pendentes
- `/alerta` - Configurar alertas automáticos
- `/processo` - Consultar processo
- `/config` - Configurações
- `/perfil` - Meu perfil

### 💾 Banco de Dados
- ✅ Armazenamento de usuários
- ✅ Histórico de conversas
- ✅ Integração com prazos processuais
- ✅ Salvamento de consultas

## 🚀 Instalação

### 1. Requisitos
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Token do Telegram Bot (obter em @BotFather)

### 2. Configuração

```bash
# Clonar repositório
cd products/tier1/bot-telegram

# Copiar arquivo de exemplo
cp ../../env.example .env

# Editar configurações
nano .env
```

**Variáveis obrigatórias:**
```bash
TELEGRAM_BOT_TOKEN=seu_token_aqui
DATABASE_URL=postgresql://genesys:genesys@localhost:5432/genesys_db
REDIS_URL=redis://localhost:6379/0

# Escolha um provedor de IA:
OPENAI_API_KEY=sua_chave_openai    # OU
GEMINI_API_KEY=sua_chave_gemini
```

### 3. Instalar Dependências

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r src/requirements.txt
```

### 4. Configurar Banco de Dados

```bash
# Criar banco de dados
sudo -u postgres psql -c "CREATE DATABASE genesys_db;"
sudo -u postgres psql -c "CREATE USER genesys WITH PASSWORD 'genesys';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE genesys_db TO genesys;"

# Rodar migrações
cd ../..
alembic upgrade head
```

### 5. Iniciar o Bot

```bash
# Modo desenvolvimento
python src/bot.py

# Modo produção (com Docker)
docker build -t genesys-telegram-bot .
docker run -d --env-file .env genesys-telegram-bot
```

## 🐳 Docker

```bash
# Build
docker build -t genesys-telegram-bot .

# Run
docker run -d \
  --env-file .env \
  --name genesys-bot \
  genesys-telegram-bot

# Logs
docker logs -f genesys-bot
```

## 🧪 Testar o Bot

1. **Inicie o bot** (python src/bot.py ou docker)
2. **Abra o Telegram**
3. **Busque seu bot** pelo nome que você configurou no @BotFather
4. **Envie** `/start`
5. **Teste os comandos:**

```
/help
/buscar
/prazos
/alerta
```

**Envie uma mensagem em linguagem natural:**
```
Oi, como funciona a prescrição trabalhista?
```

## 📊 Funcionalidades Implementadas

### ✅ Pronto
- Integração com OpenAI/Gemini
- Processamento de mensagens com IA
- Salvamento de conversas
- Busca de prazos no banco
- Callbacks de botões inline
- Criação automática de usuários
- Histórico de conversas

### ⏳ Em Desenvolvimento
- Busca avançada de jurisprudência com RAG
- Integração com API de processos
- Exportação de dados
- Estatísticas de uso

## 🔧 Configuração Avançada

### Usar OpenAI
```bash
# Em .env
OPENAI_API_KEY=sk-...
```

### Usar Google Gemini (Recomendado)
```bash
# Em .env
GEMINI_API_KEY=...
```

### Personalizar Prompt do AI
Edite `src/services/ia_service.py` e modifique o `system_prompt` na classe `OpenAIProvider` ou `GeminiProvider`.

## 📝 Logs

Os logs são salvos automaticamente em:
- Console (stdout)
- Arquivo: `genesys.log`

## 🐛 Troubleshooting

### Bot não responde
```bash
# Verificar se o token está correto
echo $TELEGRAM_BOT_TOKEN

# Verificar logs
docker logs genesys-bot
```

### Erro de conexão com banco
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar se o banco existe
psql -U genesys -d genesys_db -c "SELECT 1;"
```

### IA não funciona
```bash
# Verificar se API key está configurada
python -c "from shared.config.settings import settings; print(settings.OPENAI_API_KEY or settings.GEMINI_API_KEY)"
```

## 📞 Contato

- **Email**: contato@genesys-tecnologia.com.br
- **WhatsApp**: +55 34 99826-4603
- **Site**: https://genesys-tecnologia.com.br

## 📄 Licença

Proprietário: Genesys Tecnologia

