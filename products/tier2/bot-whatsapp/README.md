# 🤖 Bot WhatsApp Business - Genesys

Bot inteligente para WhatsApp com IA integrada.

## 🚀 Funcionalidades

- ✅ Atendimento 24/7 automatizado
- ✅ Respostas com IA (OpenAI/Gemini)
- ✅ Processamento de linguagem natural
- ✅ Gestão de contexto e conversas
- ✅ Templates e respostas rápidas
- ✅ Qualificação de leads
- ✅ Analytics

## 🏗️ Arquitetura METHOD-BMAD

### B - Backend
- FastAPI
- Twilio WhatsApp API
- LLM (OpenAI/Gemini)
- PostgreSQL + Redis

### M - Modelo
1. WhatsApp Handler - Recebe/envia mensagens
2. NLP Processor - Análise de intenção
3. Dialog Manager - Gestão de contexto
4. Response Generator - Geração de respostas
5. Notification Manager - Notificações agendadas
6. Analytics Engine - Métricas

### A - API
- `POST /webhook` - Webhook do Twilio
- `POST /api/message/send` - Enviar mensagem
- `GET /api/conversations/` - Listar conversas
- `GET /api/stats` - Estatísticas

### D - Data
- conversations, messages
- templates, analytics

## 🚀 Quick Start

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Ambiente

```bash
cp env.example .env
nano .env
```

### 3. Configurar Twilio

1. Criar conta no Twilio
2. Ativar WhatsApp Business API
3. Adicionar credentials ao `.env`

### 4. Iniciar Bot

```bash
python src/bot.py
```

### 5. Configurar Webhook

No Twilio Console:
- Webhook URL: `https://seu-dominio.com/webhook`
- Method: POST

## 📝 Uso

### Mensagens Disponíveis

- "oi" / "olá" - Saudação
- "ajuda" / "help" - Menu de ajuda
- "consultar" - Consultar jurisprudência
- "prazos" - Verificar prazos
- "agendar" - Agendar consulta
- "contato" - Informações de contato

## 🔐 Segurança

- ✅ Rate limiting
- ✅ HTTPS obrigatório
- ✅ CORS configurado
- ✅ Logging estruturado

## 📊 Monitoramento

Acesse: `http://localhost:8001/api/stats`

## 📚 Documentação

- [Arquitetura Completa](../ARQUITETURA_TIER2_BMAD.md)
- [Twilio Docs](https://www.twilio.com/docs/whatsapp)

---

**Desenvolvido por:** Genesys Tecnologia  
**Versão:** 1.0.0

