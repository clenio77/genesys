# 🤖 Como Rodar o Bot - Guia Rápido

## ✅ Tudo Configurado!

Seu bot está pronto para rodar! Siga um destes métodos:

## 🚀 Método 1: Script Simples (Recomendado)

```bash
cd products/tier1
./rodar_bot_simples.sh
```

## 🚀 Método 2: Manual

Abra um terminal e execute:

```bash
# 1. Ir para o diretório
cd products/tier1

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Configurar PYTHONPATH
export PYTHONPATH=$(pwd)

# 4. Carregar token
export TELEGRAM_BOT_TOKEN=8348618351:AAHx8Ho1FCP4hAsvKjk-WEiWibB3LOa_h7o

# 5. Rodar bot
python bot-telegram/src/bot.py
```

## 📱 Testar no Telegram

1. Abra o Telegram
2. Busque pelo seu bot
3. Envie `/start`
4. Veja a mensagem de boas-vindas!

## 🧪 Comandos para Testar

```
/start    - Iniciar o bot
/help     - Ver ajuda
/prazos   - Ver prazos
/alerta   - Configurar alertas
/config   - Configurações
/perfil   - Ver perfil
```

## ⚙️ Adicionar IA (Opcional)

Edite o arquivo `.env` e adicione uma API key:

```bash
# Escolha UMA opção:
OPENAI_API_KEY=sk-...     # Pago
GEMINI_API_KEY=AIza...    # Mais barato
```

## 🛑 Parar o Bot

Pressione `Ctrl+C` no terminal onde está rodando.

## 📊 Status Atual

- ✅ Token configurado
- ✅ Código completo
- ✅ IA integrada
- ✅ Funcionalidades prontas
- ⚠️ IA não configurada (opcional)

## 💡 Dica

Para rodar em background e sair do terminal:

```bash
nohup ./rodar_bot_simples.sh > bot.log 2>&1 &
```

Para ver os logs:

```bash
tail -f bot.log
```

## 📞 Precisa de Ajuda?

- Veja `BOT_FUNCIONANDO.md` para status completo
- Veja `CONFIGURACAO_BOT.md` para configurações avançadas
- Veja `INICIAR_BOT.md` para guia detalhado

