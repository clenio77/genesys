# 🚀 TIER 1 - Genesys Tecnologia

Serviços de alta demanda e máximo impacto para a Genesys Tecnologia.

## 📋 Serviços Incluídos

### 1. 🤖 Bot de Telegram Jurídico
Assistente de IA para consultas jurídicas via Telegram.

**Funcionalidades:**
- Busca de jurisprudência com IA
- Consulta de prazos processuais
- Alertas automáticos
- Análise de processos

### 2. 📅 Automação de Prazos Processuais
Sistema inteligente de alertas para prazos.

**Funcionalidades:**
- Notificações antecipadas (7, 3, 1 dias)
- Dashboard de prazos
- Alertas de prescrição
- API REST para integrações

### 3. 💬 Assistente Virtual 24/7
Chatbot inteligente para atendimento.

**Funcionalidades:**
- Atendimento 24/7
- Qualificação de leads
- Agendamento automático
- FAQ com IA

## 🚀 Instalação Rápida

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Instalação com Docker

```bash
# Clone o repositório
git clone <repo-url>
cd tier1

# Copiar arquivo de configuração
cp env.example .env

# Editar variáveis de ambiente
nano .env

# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Instalação Manual

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
sudo -u postgres psql -c "CREATE DATABASE genesys_db;"
sudo -u postgres psql -c "CREATE USER genesys WITH PASSWORD 'genesys';"

# Rodar migrações
alembic upgrade head

# Iniciar serviços
python bot-telegram/src/bot.py &
python automacao-prazos/src/scheduler.py &
python assistente-virtual/src/chatbot.py &
```

## 📖 Documentação

- [README Detalhado](./docs/README_TIER1.md)
- [API Documentation](./docs/API.md)
- [Database Schema](./docs/DATABASE.md)
- [Deployment Guide](./docs/DEPLOYMENT.md)

## 🔧 Configuração

Copie o arquivo `env.example` para `.env` e configure:

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=seu_token_aqui

# WhatsApp
WHATSAPP_ACCESS_TOKEN=seu_token_aqui

# AI APIs
OPENAI_API_KEY=sua_chave_aqui
GEMINI_API_KEY=sua_chave_aqui
```

## 🧪 Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=. --cov-report=html
```

## 📊 Status

- ✅ Estrutura criada
- ✅ Database models
- ✅ Configuração base
- ⏳ Bot de Telegram (em desenvolvimento)
- ⏳ Automação de Prazos (em desenvolvimento)
- ⏳ Assistente Virtual (em desenvolvimento)

## 🐛 Troubleshooting

### Bot não conecta
- Verificar `TELEGRAM_BOT_TOKEN` no `.env`
- Verificar se o bot está ativo no @BotFather

### Erro de conexão com banco
- Verificar se PostgreSQL está rodando
- Verificar `DATABASE_URL` no `.env`

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é propriedade da Genesys Tecnologia.

## 📞 Contato

- **Email**: contato@genesys-tecnologia.com.br
- **WhatsApp**: +55 34 99826-4603
- **Site**: https://genesys-tecnologia.com.br

