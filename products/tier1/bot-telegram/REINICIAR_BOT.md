# 🔄 REINICIAR BOT TELEGRAM - GUIA RÁPIDO

**Data:** 03/11/2025  
**Status:** ✅ Correções Aplicadas - Pronto para Reiniciar

---

## ⚠️ IMPORTANTE

**As correções foram aplicadas, mas o bot precisa ser REINICIADO para funcionar!**

O bot atual está rodando com o código antigo. Reinicie para aplicar as correções.

---

## 🛑 PARAR O BOT ATUAL

### Opção 1: Via Terminal (Recomendado)

```bash
# Encontrar o processo
ps aux | grep bot_com_ia.py

# Matar o processo (substituir PID pelo número encontrado)
kill <PID>

# Ou matar todos os processos Python do bot
pkill -f bot_com_ia.py
```

### Opção 2: Via Ctrl+C

Se o bot está rodando no terminal atual:
1. Pressione `Ctrl+C`
2. Aguarde o bot parar

### Opção 3: Verificar e Matar

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1

# Ver processos
ps aux | grep bot_com_ia

# Matar
kill $(ps aux | grep '[b]ot_com_ia.py' | awk '{print $2}')
```

---

## ✅ VERIFICAR CORREÇÕES ANTES DE REINICIAR

### 1. Verificar PostgreSQL

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1/bot-telegram
python3 test_db.py
```

**Resultado esperado:**
```
✅ Conexão estabelecida com sucesso!
```

### 2. Verificar .env

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
grep DATABASE_URL .env
```

**Deve mostrar:**
```
DATABASE_URL=postgresql://genesys:genesys123@localhost:5432/genesys_db
```

### 3. Verificar Código Corrigido

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1/bot-telegram
grep -A 5 "def sanitize_text" src/handlers/messages.py
```

**Deve mostrar:**
```python
def sanitize_text(text: str) -> str:
    # Remove caracteres de escape problemáticos primeiro
    import re
    text = re.sub(r'\\x(?![0-9a-fA-F]{2})', '', text)
```

---

## 🚀 REINICIAR O BOT

### Passo 1: Navegar para o Diretório

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1/bot-telegram
```

### Passo 2: Verificar Configuração

```bash
# Verificar se .env existe no diretório pai
cat ../.env | grep -E "(TELEGRAM|DATABASE|OPENAI|GEMINI)"
```

### Passo 3: Iniciar o Bot

```bash
# Opção A: Bot com IA (recomendado)
python src/bot_com_ia.py

# Opção B: Bot simples
python src/bot.py
```

### Passo 4: Verificar Logs

**Logs esperados (sem erros):**
```
✅ Bot iniciado com sucesso
✅ Conectado ao Telegram
✅ IA configurada (OpenAI ou Gemini)
✅ Banco de dados: OK (ou fallback ativo)
```

**Se aparecer erro de banco:**
```
⚠️ Banco de dados não disponível
💡 Bot continuará funcionando sem banco de dados
```
*(Isso é OK - o bot funciona em modo fallback)*

---

## 🧪 TESTAR O BOT

### 1. No Telegram

1. **Abra o Telegram**
2. **Busque seu bot** pelo nome
3. **Envie:** `/start`
4. **Envie:** `O que é jurisprudência?`

### 2. Verificar Logs

**Logs esperados (sem erros):**
```
✅ Usuário X enviou: o que jurisprudência?
✅ Processando com IA...
✅ Mensagem completa enviada (1 parte(s))
```

**NÃO deve aparecer:**
```
❌ Erro ao processar mensagem: incomplete escape \x
❌ password authentication failed
```

### 3. Testar Outras Mensagens

```
Teste 1: "Oi, como vai?"
Teste 2: "Explique prescrição trabalhista"
Teste 3: "Qual a diferença entre prazo e decadência?"
```

---

## 🔍 VERIFICAR SE FUNCIONOU

### ✅ Sinais de Sucesso

1. **Bot responde normalmente**
2. **Sem erros nos logs**
3. **Respostas da IA chegam corretamente**
4. **Sem erros de escape**
5. **Banco conectado (ou fallback ativo)**

### ❌ Se Ainda Houver Erros

**Erro de PostgreSQL:**
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Reiniciar PostgreSQL
sudo systemctl restart postgresql

# Testar conexão
python3 test_db.py
```

**Erro de escape:**
```bash
# Verificar se o código foi atualizado
grep "re.sub" src/handlers/messages.py

# Se não aparecer, o arquivo não foi salvo
# Reabrir e verificar
```

**Erro de IA:**
```bash
# Verificar API keys
cat ../.env | grep -E "(OPENAI|GEMINI)"

# Testar manualmente
python3 -c "from services.ia_service import ai_service; print(ai_service.provider)"
```

---

## 📊 STATUS ATUAL

```
┌─────────────────────────────────────────────┐
│  CORREÇÕES APLICADAS                       │
├─────────────────────────────────────────────┤
│  ✅ PostgreSQL: genesys/genesys123        │
│  ✅ sanitize_text: Melhorada               │
│  ✅ test_db.py: Criado                     │
│  ✅ .env: Atualizado                       │
├─────────────────────────────────────────────┤
│  ⏳ BOT PRECISA SER REINICIADO            │
└─────────────────────────────────────────────┘
```

---

## 🎯 COMANDOS RÁPIDOS

### Parar Bot

```bash
pkill -f bot_com_ia.py
```

### Iniciar Bot

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1/bot-telegram
python src/bot_com_ia.py
```

### Ver Logs em Tempo Real

```bash
tail -f logs/bot_telegram.log
```

### Testar Conexão Banco

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1/bot-telegram
python3 test_db.py
```

---

## 💡 DICAS

1. **Sempre pare o bot antes de reiniciar**
   - Evita processos duplicados
   - Garante que mudanças sejam aplicadas

2. **Use `test_db.py` antes de iniciar**
   - Verifica se PostgreSQL está OK
   - Economiza tempo de debug

3. **Monitore os logs**
   - Primeiros segundos são críticos
   - Erros aparecem logo no início

4. **Teste no Telegram rapidamente**
   - Envie uma mensagem simples
   - Verifique se não há erros

---

## 🚨 TROUBLESHOOTING

### Bot não para

```bash
# Forçar kill
kill -9 $(ps aux | grep '[b]ot_com_ia.py' | awk '{print $2}')
```

### Bot não inicia

```bash
# Verificar Python
python3 --version  # Deve ser 3.11+

# Verificar dependências
pip list | grep -E "(telegram|openai|sqlalchemy)"

# Verificar .env
ls -la ../.env
```

### Erros persistem

```bash
# Verificar se arquivo foi salvo
grep "re.sub" src/handlers/messages.py

# Se não aparecer, reabrir o arquivo
# As mudanças podem não ter sido salvas
```

---

## ✅ CHECKLIST

Antes de reiniciar:

- [ ] Bot parado completamente
- [ ] PostgreSQL rodando (`sudo systemctl status postgresql`)
- [ ] `.env` atualizado com senha correta
- [ ] `test_db.py` passou (conexão OK)
- [ ] Código corrigido salvo (`sanitize_text`)

Ao reiniciar:

- [ ] Bot inicia sem erros críticos
- [ ] Logs mostram "Bot iniciado"
- [ ] Responde no Telegram
- [ ] Sem erros de escape
- [ ] Sem erros de autenticação

---

**🔄 Agora é só reiniciar e testar!**

*Documento criado em 03/11/2025*

