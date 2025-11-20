# 🧠 Como Adicionar IA ao Bot - Guia Final

## ✅ Bot Rodando Agora

O bot está rodando com a estrutura de IA pronta!

### 🔍 Status Atual

- ✅ Bot rodando (PID: 177113)
- ✅ Aceita comandos e mensagens
- ⚠️ IA não configurada (mostra mensagens básicas)
- 💡 Estrutura de IA pronta para usar!

## 🚀 Ativar IA (2 Opções)

### **Opção 1: Google Gemini (Recomendado - Mais Barato)**

1. Obter API Key:
   - Acesse: https://makersuite.google.com/app/apikey
   - Faça login com Google
   - Crie uma nova API Key
   - Copie a chave (começa com `AIza...`)

2. Adicionar no `.env`:
```bash
cd products/tier1
nano .env
```

Adicione esta linha:
```bash
GEMINI_API_KEY=AIza...
```

### **Opção 2: OpenAI (Melhor Qualidade - Pago)**

1. Obter API Key:
   - Acesse: https://platform.openai.com/api-keys
   - Faça login/cadastro
   - Crie uma nova API Key
   - Copie a chave (começa com `sk-...`)

2. Adicionar no `.env`:
```bash
OPENAI_API_KEY=sk-...
```

## 🎯 Após Adicionar API Key

Reinicie o bot:

```bash
cd products/tier1

# Parar bot atual
pkill -f bot_com_ia.py

# Rodar novamente
source venv/bin/activate
export PYTHONPATH=$(pwd)
export TELEGRAM_BOT_TOKEN=8348618351:AAHx8Ho1FCP4hAsvKjk-WEiWibB3LOa_h7o
nohup python bot-telegram/src/bot_com_ia.py > bot_ia.log 2>&1 &
```

## 📊 Testar IA no Telegram

Depois de adicionar a API key e reiniciar:

1. Envie no Telegram:
```
"como funciona a cadeia de custódia?"
```

2. Receberá resposta inteligente com IA!

## 💰 Custos Estimados

### Gemini (Recomendado)
- **Gratuito:** 15 solicitações/min
- **Pago:** $0.50/1M tokens de entrada, $1.50/1M tokens de saída
- **Extremamente barato!**

### OpenAI
- **GPT-4:** $3-30/1M tokens (depende do modelo)
- **GPT-3.5:** $0.50-2/1M tokens
- **Bom desempenho**

## 🎉 Resultado Final

Com IA configurada, o bot:
- ✅ Responde perguntas jurídicas inteligentemente
- ✅ Entende contexto
- ✅ Gera respostas completas e fundamentadas
- ✅ Pode conversar naturalmente

## 📞 Conclusão

Adicione uma API key no `.env` e reinicie o bot para ativar IA!

O bot está funcionando perfeitamente! 🎉

