# 🚀 Guia de Deploy do Bot no Pella (Grátis 24/7)

Guia passo a passo para fazer deploy do bot Telegram no Pella, a melhor plataforma gratuita.

---

## 📋 Pré-requisitos

- ✅ Bot já funcionando localmente
- ✅ Conta no Pella (grátis)
- ✅ Token do Telegram Bot
- ✅ API Key do Gemini (ou OpenAI)

---

## 🔧 Passo 1: Preparar Arquivos

### ✅ Arquivos Já Preparados

Os arquivos necessários já estão prontos na raiz do projeto `tier1/`:
- ✅ `requirements.txt` (dependências otimizadas)
- ✅ `.pellaignore` (arquivos ignorados no deploy)

### 📁 Estrutura Necessária no Pella

**IMPORTANTE:** O bot precisa de **2 pastas obrigatórias**:
- ✅ `bot-telegram/` - Código do bot
- ✅ `shared/` - Módulos compartilhados (OBRIGATÓRIO)

**Não envie apenas `bot-telegram/`! O bot depende da pasta `shared/` para funcionar.**

---

## 📦 Passo 2: Configurar Variáveis de Ambiente

### Na dashboard do Pella, configure as seguintes variáveis:

#### 🔴 Obrigatórias:
```bash
TELEGRAM_BOT_TOKEN=seu_token_do_botfather
GEMINI_API_KEY=sua_chave_gemini
# OU (ao invés de GEMINI_API_KEY)
OPENAI_API_KEY=sua_chave_openai
```

#### 🟡 Recomendadas:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname
# OU para SQLite (mais simples, mas menos recomendado para produção)
# DATABASE_URL=sqlite:///bot.db

LOG_LEVEL=INFO
SECRET_KEY=uma_chave_secreta_aleatoria
```

**⚠️ IMPORTANTE:** 
- Nunca commite suas chaves no Git!
- Use variáveis de ambiente no dashboard do Pella
- Para SQLite no Pella, use caminho relativo: `sqlite:///./bot.db`

---

## 🌐 Passo 3: Deploy no Pella

### 3.1 Criar Conta

1. Acesse: https://www.pella.app/signup
2. Crie sua conta (não precisa de cartão de crédito)

### 3.2 Criar Novo Servidor

1. Clique em **"New Server"**
2. Selecione **"Free"** tier
3. Escolha **"Python"** como runtime
4. No campo **"Code Source"**, escolha **"File Upload"**

### 3.2.1 Preparar Arquivo ZIP

**IMPORTANTE:** O Pella requer upload em formato **.ZIP** (máximo 30MB)!

**Opção 1: Usar Script Automático (Recomendado)**
```bash
# Na raiz do projeto tier1/
./scripts/preparar_zip_pella.sh
```

Isso criará `bot-pella-deploy.zip` com todas as pastas necessárias.

**Opção 2: Criar ZIP Manualmente**

Crie um arquivo ZIP contendo:
```
bot-pella-deploy.zip
├── bot-telegram/
│   └── src/
├── shared/
│   ├── config/
│   ├── database/
│   └── utils/
└── requirements.txt
```

⚠️ **Não inclua:**
- `venv/`
- `__pycache__/`
- `.env`
- `logs/`
- `documentacao/`
- Arquivos de teste

### 3.3 Fazer Upload do ZIP

1. Clique em **"File Upload"** no dashboard do Pella
2. Arraste o arquivo `bot-pella-deploy.zip` OU clique para selecionar
3. Aguarde o upload concluir (verifique se está dentro do limite de 30MB)

### 3.4 Configurar Build e Start

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
cd bot-telegram && python src/bot_com_ia.py
```

**OU** se a estrutura permitir:
```bash
python bot-telegram/src/bot_com_ia.py
```

> **Nota:** Use `bot_com_ia.py` (com IA) ou `bot.py` (versão principal). Ambos funcionam.

### 3.5 Variáveis de Ambiente no Pella

No dashboard do Pella, vá em **Settings → Environment Variables** e adicione:

**Obrigatórias:**
- `TELEGRAM_BOT_TOKEN` - Token do seu bot (obtenha em @BotFather)
- `GEMINI_API_KEY` ou `OPENAI_API_KEY` - Escolha um provedor de IA

**Opcionais (com valores padrão):**
- `DATABASE_URL` - URL do banco (padrão: `sqlite:///./bot.db`)
- `LOG_LEVEL` - Nível de log (padrão: `INFO`)
- `SECRET_KEY` - Chave secreta para segurança

**💡 Dica:** Use SQLite se não tiver PostgreSQL. É mais simples para começar!

---

## ✅ Passo 4: Verificação

### 4.1 Verificar Status

No dashboard do Pella, verifique:
- ✅ Server está "Online"
- ✅ Sem erros nos logs
- ✅ Bot está respondendo no Telegram

### 4.2 Testar Bot

1. Abra seu bot no Telegram
2. Envie `/start`
3. Deve receber a mensagem de boas-vindas
4. Teste comandos: `/help`, `/prazos`, `/buscar`

---

## 🛠️ Troubleshooting

### Problema: Bot não inicia

**Solução:**
1. Verifique os logs no Pella dashboard
2. Confirme que `requirements.txt` está correto
3. Verifique que o start command está correto

### Problema: "Module not found" ou "No module named 'shared'"

**Solução:**
1. **Verifique se você enviou a pasta `shared/`** junto com `bot-telegram/`
2. Confirme que a estrutura no servidor está correta:
   ```
   /app/
   ├── bot-telegram/
   └── shared/
   ```
3. Verifique o PYTHONPATH - deve incluir a raiz do projeto
4. Adicione o módulo faltante no `requirements.txt` se necessário
5. Faça um redeploy

### Problema: Bot para de responder

**Solução:**
1. Verifique uptime no Pella (deve ser 99.9%)
2. Veja logs para erros
3. Confirme que variáveis de ambiente estão corretas

### Problema: Timeout em operações longas

**Solução:**
1. Upgrade para plano pago ($3/ano minimum)
2. Otimize código para operações assíncronas

---

## 📊 Monitoramento

### Logs em Tempo Real

Acesse o dashboard do Pella → View Logs para ver:
- Erros do bot
- Requisições processadas
- Status de saúde

### Métricas

No Pella dashboard, monitore:
- **CPU Usage:** Deve ser baixo (< 10%)
- **RAM Usage:** Deve ser < 100 MB (free tier)
- **Uptime:** Deve ser > 99%

---

## 🔄 Manutenção

### Atualizar Bot

1. Faça push para o Git
2. Pella detecta automaticamente
3. Faz redeploy automático

Ou:

1. Acesse dashboard
2. Clique em "Redeploy"
3. Aguarde concluir

### Adicionar Funcionalidades

1. Desenvolva localmente
2. Teste completamente
3. Faça deploy via Git push
4. Pella auto-deploy em segundos

---

## 💰 Planos Pella

### Free (Atual)
- ✅ 100 MB RAM
- ✅ 0.1 CPU
- ✅ 5 GB Disk
- ✅ Sempre online

### Nano ($3/ano)
- ✅ 256 MB RAM
- ✅ Todas as features free

### Small ($1.25/mês)
- ✅ 1 GB RAM
- ✅ Melhor performance

---

## 🎯 Próximos Passos

Após deploy bem-sucedido:

1. ✅ Teste todos os comandos
2. ✅ Configure alertas de monitoramento
3. ✅ Documente acesso ao dashboard
4. ✅ Compartilhe link do bot com usuários

---

## 📞 Suporte

- **Discord:** Comunidade Pella
- **Telegram:** @thestonechat
- **Email:** Via dashboard

---

## 🎉 Pronto!

Seu bot agora está rodando 24/7 de graça no Pella!

**Acesse:**
- Dashboard: https://www.pella.app
- Logs: Dashboard → View Logs
- Status: https://status.pella.app

---

**Data do Deploy:** [Preencher com data]  
**Versão Bot:** 1.0  
**Plataforma:** Pella Free Tier

---

## 📋 Checklist Rápido de Deploy

Antes de fazer deploy, certifique-se:

- [ ] ✅ Conta no Pella criada
- [ ] ✅ Token do Telegram Bot obtido (@BotFather)
- [ ] ✅ API Key do Gemini (ou OpenAI) configurada
- [ ] ✅ Pasta `bot-telegram/` pronta
- [ ] ✅ Pasta `shared/` pronta (OBRIGATÓRIO!)
- [ ] ✅ Arquivo `requirements.txt` na raiz
- [ ] ✅ Variáveis de ambiente configuradas no Pella
- [ ] ✅ Build Command: `pip install -r requirements.txt`
- [ ] ✅ Start Command: `cd bot-telegram && python src/bot_com_ia.py`

**Estrutura mínima necessária no servidor:**
```
/app/
├── bot-telegram/
│   └── src/
│       ├── bot_com_ia.py
│       ├── handlers/
│       └── services/
├── shared/
│   ├── config/
│   ├── database/
│   └── utils/
└── requirements.txt
```

---

## 🎯 Próximas Ações

1. **Acesse:** https://www.pella.app/signup
2. **Crie um novo servidor** (Free tier)
3. **Faça upload** ou conecte repositório Git com:
   - `bot-telegram/`
   - `shared/`
   - `requirements.txt`
4. **Configure** variáveis de ambiente
5. **Deploy!** 🚀

