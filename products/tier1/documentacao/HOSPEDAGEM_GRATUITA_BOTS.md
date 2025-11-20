# 🌐 Plataformas Gratuitas para Hospedagem de Bots do Telegram

Pesquisa realizada em 2025 sobre as melhores opções gratuitas para hospedar bots do Telegram 24/7.

---

## 📋 Sumário

1. [Render](#1-render) ⭐ **RECOMENDADO**
2. [Pella](#2-pella) ⭐ **MELHOR FREE**
3. [Replit](#3-replit)
4. [PythonAnywhere](#4-pythonanywhere)
5. [AWS Lambda](#5-aws-lambda)
6. [Outras Opções](#6-outras-opções)

---

## 1. Render

### 🎯 Descrição
Plataforma moderna similar ao Heroku (que descontinuou o tier gratuito). Suporta Python, Node.js e outras tecnologias.

### ✅ Vantagens
- **Plano gratuito permanente**
- Suporta Python e Node.js
- Deploy automático via Git
- PostgreSQL gratuito (com limitações)
- Interface moderna e intuitiva
- Auto-deploy com cada push

### ⚠️ Limitações do Free Tier
- **750 horas/mês** (~31 dias)
- **Spins down após 15 minutos** sem tráfego (demora ~1 minuto para voltar)
- Não suporta persistent disks
- Sem SSH
- Apenas 1 instância

### 💰 Preço
- **Plano Free:** Grátis
- Plano Starter: $19/mês

### 📚 Documentação
- Site: https://render.com
- Docs: https://render.com/docs/free

### 🔧 Como Deployar
1. Conecte seu repositório Git
2. Selecione "Web Service"
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`

---

## 2. Pella ⭐ DESTAQUE

### 🎯 Descrição
Plataforma especializada em hosting de bots (Discord e Telegram) com foco em free tier.

### ✅ Vantagens
- **Plano totalmente gratuito** (sempre)
- **99.9% uptime**
- **Não requer cartão de crédito**
- Sempre online (não spin down)
- Deploy em menos de 1 minuto
- Suporte via Discord
- Servidores em US e EU

### ⚠️ Limitações do Free Tier
- **100 MB RAM**
- **0.1 CPU**
- 5 GB Disk
- Sempre localizado em US (premium pode escolher EU)

### 💰 Preço
- **Plano Free:** Grátis
- Plano Nano: $3/ano (256 MB RAM)
- Plano Mini: $1.80/trimestre (512 MB RAM)
- Plano Small: $1.25/mês (1 GB RAM)

### 📚 Documentação
- Site: https://www.pella.app
- Telegram Support: @thestonechat

### 🎯 Por que é a melhor opção gratuita?
- Não entra em "sleep mode" como Render
- Especializado em bots
- Suporte ativo na comunidade
- Uptime garantido de 99.9%

---

## 3. Replit

### 🎯 Descrição
Plataforma com IA integrada para desenvolvimento e deploy de bots.

### ✅ Vantagens
- Editor integrado online
- Colaboração em tempo real
- Templates prontos para Python e Node.js
- Deploy com 1 clique
- AI para debug e autocomplete

### ⚠️ Limitações do Free Tier
- Requer atividade manual para manter online
- Limites de CPU e RAM

### 💰 Preço
- Plano Starter: Grátis
- Plano Core: $15/mês

### 📚 Documentação
- Site: https://replit.com

---

## 4. PythonAnywhere

### 🎯 Descrição
Especializado em hospedar projetos Python.

### ✅ Vantagens
- Configuração simples
- Focado em Python
- IDE integrado
- Escalável

### ⚠️ Limitações do Free Tier
- Plano Basic: $5/mês (mínimo pago)
- Plano Web Dev: $12/mês

### 💰 Preço
- **Básico:** $5/mês (mínimo)
- Não há plano verdadeiramente gratuito

---

## 5. AWS Lambda

### 🎯 Descrição
Modelo serverless - paga apenas pelo que usar.

### ✅ Vantagens
- **Free tier generoso:** 1 milhão de requisições/mês
- 400,000 GB-segundo
- Alta escalabilidade
- Integração com outros serviços AWS

### ⚠️ Limitações
- Requer configuração de webhook
- Menos prático para iniciantes
- Requer cartão de crédito
- Timeout de execução (até 15 min)

### 💰 Preço
- **Free Tier:** Até 1 milhão de requisições
- Após free tier: $0.20 por 1M de requisições

### 📚 Documentação
- Site: https://aws.amazon.com/lambda

---

## 6. Outras Opções

### Heroku
- ❌ Descontinuou plano gratuito em 2022
- Não recomendado

### Vercel
- ✅ Grátis
- Focado em serverless
- Bom para webhooks
- Site: https://vercel.com

### Oracle Cloud
- ✅ 30 dias grátis
- Complexo para configuração
- Site: https://www.oracle.com/cloud/free

### Railway
- ⚠️ Plano gratuito limitado
- Site: https://railway.app

### Fly.io
- ⚠️ Plano gratuito limitado
- Site: https://fly.io

---

## 🏆 Recomendações por Caso de Uso

### Para Bot Simples (Menos de 100 usuários)
**Pella** - Free tier é perfeito, sempre online

### Para Bot Médio (100-500 usuários)
**Render** ou **Pella Small** ($1.25/mês)

### Para Bot Grande (500+ usuários)
**AWS Lambda** ou **Render** (plano pago)

### Para Testes/Desenvolvimento
**Render** ou **Replit**

---

## 📊 Comparação Rápida

| Plataforma | Free Forever | Uptime 24/7 | Sem Cartão | RAM Free |
|------------|--------------|-------------|------------|----------|
| **Pella** | ✅ | ✅ | ✅ | 100 MB |
| **Render** | ✅ | ⚠️ (spin down) | ✅ | 512 MB |
| **Replit** | ✅ | ❌ | ✅ | Limitado |
| **AWS Lambda** | ✅ | ✅ | ❌ | Serverless |

---

## 🚀 Próximos Passos

### Para Deploy Imediato (Recomendado)
1. **Crie conta na Pella:** https://www.pella.app/signup
2. **Conecte seu repositório** ou faça upload dos arquivos
3. **Configure as variáveis de ambiente:**
   - `TELEGRAM_BOT_TOKEN`
   - `GEMINI_API_KEY`
   - Outras variáveis necessárias
4. **Deploy automático em menos de 1 minuto!**

### Arquivos Necessários
- `bot.py` (arquivo principal)
- `requirements.txt` (dependências Python)
- `.env` ou configure variáveis na plataforma

### Exemplo de requirements.txt
```txt
python-telegram-bot==20.0
google-generativeai==0.3.0
sqlalchemy==2.0.0
```

---

## 💡 Dicas Importantes

### ✅ Melhores Práticas
1. **Use variáveis de ambiente** para tokens
2. **Implemente health checks** para manter o bot ativo
3. **Configure logs** para debugging
4. **Use webhooks** ao invés de polling quando possível

### ⚠️ Problemas Comuns
- **Bot para de responder:** Verifique logs e uptime
- **Timeout:** Aumente RAM ou otimize código
- **Token inválido:** Verifique variáveis de ambiente

---

## 📞 Suporte

- **Pella:** Discord e Telegram @thestonechat
- **Render:** Suporte via email e docs completos
- **AWS Lambda:** Fóruns da comunidade AWS

---

## 📝 Conclusão

Para o nosso bot juridico Genesys, as **melhores opções** são:

1. **Pella** - Para manter 24/7 com zero custo
2. **Render** - Para estabilidade com limites aceitáveis
3. **AWS Lambda** - Para escalabilidade futura

**Recomendação final:** Comece com **Pella** (free forever) e migre para **Render** ou **AWS Lambda** quando necessário escalar.

---

## 🔗 Links Úteis

- [Pella - Free Telegram Bot Hosting](https://www.pella.app/free-telegram-bot-hosting)
- [Render - Free Deploy](https://render.com/docs/free)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Documentação Render](https://render.com/docs)

---

**Pesquisa realizada em:** Outubro 2025  
**Próxima atualização:** Verificar status das plataformas periodicamente

