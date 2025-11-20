# 🔐 Variáveis de Ambiente para Pella

## 📋 Variáveis OBRIGATÓRIAS

Configure estas no painel do Pella:

### 1. Token do Telegram (OBRIGATÓRIO)
```
Chave: TELEGRAM_BOT_TOKEN
Valor: 8348618351:AAHx8Ho1F...
```
**Onde obter:** @BotFather no Telegram → `/newbot`

---

### 2. Provedor de IA (OBRIGATÓRIO - Escolha UM)

**Opção A: Google Gemini (Recomendado - Mais barato)**
```
Chave: GEMINI_API_KEY
Valor: AIzaSyBh0qoud2D...
```

**Opção B: OpenAI**
```
Chave: OPENAI_API_KEY
Valor: sk-proj-...
```

---

## 🟡 Variáveis RECOMENDADAS

### 3. Banco de Dados

**Para SQLite (Mais simples - Recomendado para começar):**
```
Chave: DATABASE_URL
Valor: sqlite:///./bot.db
```

**OU para PostgreSQL (se já tiver configurado):**
```
Chave: DATABASE_URL
Valor: postgresql://usuario:senha@host:5432/database
```

---

### 4. Logs
```
Chave: LOG_LEVEL
Valor: INFO
```

---

## ⚪ Variáveis OPCIONAIS

### 5. Segurança
```
Chave: SECRET_KEY
Valor: uma-chave-secreta-aleatoria-para-seguranca
```
*Pode deixar em branco - tem valor padrão*

---

### 6. Redis (Opcional - não necessário para bot básico)
```
Chave: REDIS_URL
Valor: redis://localhost:6379/0
```
*Pode deixar em branco se não usar Redis*

---

## 📝 Resumo Rápido para Copiar e Colar

### Configuração Mínima (SQLite):
```
TELEGRAM_BOT_TOKEN=8348618351:AAHx8Ho1F...
GEMINI_API_KEY=AIzaSyBh0qoud2D...
DATABASE_URL=sqlite:///./bot.db
LOG_LEVEL=INFO
```

---

### Configuração Completa:
```
TELEGRAM_BOT_TOKEN=8348618351:AAHx8Ho1F...
GEMINI_API_KEY=AIzaSyBh0qoud2D...
DATABASE_URL=sqlite:///./bot.db
LOG_LEVEL=INFO
SECRET_KEY=uma-chave-secreta-aleatoria
```

---

## ✅ Como Adicionar no Pella

1. Vá em **Configurações** (Settings)
2. Seção **"VARIÁVEIS DE AMBIENTE"** (Environment Variables)
3. Para cada variável:
   - **Chave:** Digite o nome (ex: `TELEGRAM_BOT_TOKEN`)
   - **Valor:** Digite o valor (ex: seu token)
   - Clique em **"Salvar"** (Save)

---

## 🔍 Verificar Valores (Local)

Se você quiser verificar os valores do seu `.env` local:

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
cat .env | grep -E "TELEGRAM_BOT_TOKEN|GEMINI_API_KEY|OPENAI_API_KEY|DATABASE_URL"
```

---

## ⚠️ Importante

- ✅ **NUNCA** compartilhe seus tokens/chaves publicamente
- ✅ Use valores **reais** (não deixe "your_token_here")
- ✅ Para SQLite no Pella, use: `sqlite:///./bot.db`
- ✅ Após adicionar variáveis, **clique em "Salvar"**
- ✅ Reinicie o servidor após alterar variáveis

---

**Última atualização:** 2025-10-30

