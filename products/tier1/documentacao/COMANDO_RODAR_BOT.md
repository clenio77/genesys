# 🚀 Como Rodar o Bot

## Opção 1: Script Automático (Recomendado)

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
./ativar_bot_ia.sh
```

Este script:
- ✅ Ativa o venv automaticamente
- ✅ Configura PYTHONPATH
- ✅ Carrega variáveis do .env
- ✅ Roda o bot

**Para rodar em background:**
```bash
./ativar_bot_ia.sh > bot_ativa.log 2>&1 &
```

---

## Opção 2: Comando Manual Completo

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
source venv/bin/activate
export PYTHONPATH=$(pwd)
export TELEGRAM_BOT_TOKEN=8348618351:AAHx8Ho1FCP4hAsvKjk-WEiWibB3LOa_h7o
export GEMINI_API_KEY=AIzaSyBh0qoud2DOMabd-Ki_U5gt_nbTksXgNsA
python bot-telegram/src/bot_com_ia.py
```

**Para rodar em background:**
```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
source venv/bin/activate
export PYTHONPATH=$(pwd)
export TELEGRAM_BOT_TOKEN=8348618351:AAHx8Ho1FCP4hAsvKjk-WEiWibB3LOa_h7o
export GEMINI_API_KEY=AIzaSyBh0qoud2DOMabd-Ki_U5gt_nbTksXgNsA
python bot-telegram/src/bot_com_ia.py > bot_cnj_integrado.log 2>&1 &
```

---

## Opção 3: Usando .env

Se você tiver um arquivo `.env` configurado:

```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1
source venv/bin/activate
source .env
export PYTHONPATH=$(pwd)
python bot-telegram/src/bot_com_ia.py
```

---

## 📊 Verificar se Está Rodando

```bash
# Ver processos do bot
ps aux | grep bot_com_ia.py | grep -v grep

# Ver logs
tail -f /home/clenio/Documentos/Meusagentes/genesys/products/tier1/bot_cnj_integrado.log
```

---

## 🛑 Parar o Bot

```bash
# Encontrar processo
ps aux | grep bot_com_ia.py | grep -v grep

# Matar processo (substitua PID pelo número do processo)
kill <PID>
```

Ou:

```bash
pkill -f bot_com_ia.py
```

---

## ✅ Verificar Funcionamento

Após iniciar, teste no Telegram:
1. Envie `/start` ao bot
2. Verifique se responde
3. Teste `/help` para ver todos os comandos
4. Teste `/magistrado` para buscar um magistrado

