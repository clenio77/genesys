# 🚀 Deploy Rápido no Pella - Checklist

Guia resumido para fazer deploy do bot Telegram no Pella em poucos minutos.

## ✅ O Que Você Já Tem Pronto

- ✅ `requirements.txt` criado na raiz
- ✅ `.pellaignore` configurado
- ✅ Guia completo em `documentacao/DEPLOY_PELLA.md`

## 📦 O Que Você Precisa Fazer

### 1️⃣ Criar Conta no Pella
👉 Acesse: https://www.pella.app/signup

### 2️⃣ Preparar Arquivo ZIP para Upload

**IMPORTANTE:** O Pella requer upload em formato **.ZIP** (máximo 30MB)!

#### Opção Rápida - Script Automático:
```bash
# Na raiz do projeto tier1/
./scripts/preparar_zip_pella.sh
```

Isso criará `bot-pella-deploy.zip` pronto para upload.

#### Opção Manual - Criar ZIP:
Crie um arquivo ZIP com:
```
bot-pella-deploy.zip
├── bot-telegram/    ← Código do bot
├── shared/          ← Módulos compartilhados (OBRIGATÓRIO!)
└── requirements.txt ← Dependências Python
```

**⚠️ NÃO inclua:** `venv/`, `__pycache__/`, `.env`, `logs/`, etc.

### 3️⃣ No Pella Dashboard

#### Configurar Servidor:
1. Clique em **"New Server"**
2. Escolha **"Free"** tier
3. Runtime: **Python**
4. No campo **"Code Source"**, escolha **"File Upload"**
5. Faça upload do arquivo **`bot-pella-deploy.zip`**
   - Arraste o arquivo OU clique para selecionar
   - Tamanho máximo: 30MB

#### Build & Start:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `cd bot-telegram && python src/bot_com_ia.py`

#### Variáveis de Ambiente (Settings → Environment Variables):

**Obrigatórias:**
```bash
TELEGRAM_BOT_TOKEN=seu_token_aqui
GEMINI_API_KEY=sua_chave_aqui
# OU
OPENAI_API_KEY=sua_chave_aqui
```

**Opcionais:**
```bash
DATABASE_URL=sqlite:///./bot.db
LOG_LEVEL=INFO
```

### 4️⃣ Deploy!

Após configurar, o Pella fará:
1. ✅ Build automático
2. ✅ Instalação de dependências
3. ✅ Início do bot

### 5️⃣ Verificar

1. Veja os logs no dashboard
2. Teste o bot no Telegram: `/start`
3. Deve responder! 🎉

## 🐛 Problema: "No module named 'shared'"

**Solução:** Você esqueceu de enviar a pasta `shared/`!
- Adicione a pasta `shared/` no servidor
- Faça redeploy

## 📚 Documentação Completa

Veja `documentacao/DEPLOY_PELLA.md` para detalhes completos.

---

**Pronto para fazer deploy? Siga os passos acima! 🚀**

