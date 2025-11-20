# 🤖 Configuração do Bot de Telegram - Guia Completo

## 📋 Passo a Passo

### 1. Criar o Bot no Telegram

#### Passo 1: Abrir BotFather
1. Abra o Telegram
2. Procure por **@BotFather** na busca
3. Inicie uma conversa

#### Passo 2: Criar Novo Bot
```
/newbot
```

BotFather irá perguntar o nome do bot:
```
Nome do Bot: Genesys Legal Assistant
```

Depois irá pedir o username:
```
Username do Bot: genesys_legal_bot
```

**⚠️ IMPORTANTE:** O username deve terminar com `_bot` e ser único!

#### Passo 3: Obter o Token
BotFather irá responder com algo como:
```
Done! Congratulations on your new bot. 

Use this token to access the HTTP API:
123456789:ABCdefGHIjklMNOpqrsTUVwxyz

For a description of the Bot API, see this page:
https://core.telegram.org/bots/api
```

**✅ Copie esse token!** Você precisará dele no próximo passo.

---

### 2. Configurar o Token no Projeto

#### Opção 1: Arquivo `.env` (Recomendado)
```bash
# Editar arquivo de configuração
cd tier1
nano .env

# Adicionar:
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

#### Opção 2: Variável de Ambiente
```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
```

---

### 3. Configurações Adicionais do Bot

#### 3.1 Descrever o Bot
No chat com BotFather:
```
/setdescription
```
Selecione seu bot e envie a descrição:
```
Assistente jurídico inteligente da Genesys Tecnologia. 
Busque jurisprudência, consulte prazos processuais e receba alertas automáticos.
```

#### 3.2 Adicionar Foto de Perfil
```
/setuserpic
```
Selecione seu bot e envie uma foto (quando solicitado).

#### 3.3 Comandos do Bot
```
/setcommands
```
Selecione seu bot e envie:
```
start - Iniciar o bot
help - Ver ajuda
buscar - Buscar jurisprudência
prazos - Ver prazos pendentes
alerta - Configurar alertas
processo - Consultar processo
config - Configurações
perfil - Meu perfil
```

---

### 4. Testar o Bot

#### Iniciar o Servidor
```bash
# Na pasta tier1
python bot-telegram/src/bot.py
```

Você deverá ver:
```
Iniciando Bot de Telegram Jurídico...
Bot iniciado com sucesso!
```

#### Conversar com o Bot
1. Abra o Telegram
2. Procure por **@seu_bot_username** (exemplo: @genesys_legal_bot)
3. Clique em **Iniciar** ou envie `/start`
4. Digite `/help` para ver os comandos disponíveis

---

### 5. Permissões e Segurança

#### 5.1 Webhook (Para Produção)

Quando estiver em produção, configure um webhook:

```bash
# Enviar comando via curl
curl -X POST "https://api.telegram.org/bot<SEU_TOKEN>/setWebhook" \
  -d "url=https://seu-dominio.com/webhook"
```

#### 5.2 Permissões do Bot

Algumas funcionalidades podem requerer permissões especiais. 
Você pode configurá-las com BotFather:

```
/setjoingroups - Para bot usar em grupos
/setprivacy - Para privacidade de comandos
```

---

### 6. Debugging

#### Ver Logs
```bash
# Logs do bot
tail -f tier1/logs/bot_telegram.log
```

#### Verificar Status do Bot
```bash
# Ver informações do bot
curl "https://api.telegram.org/bot<SEU_TOKEN>/getMe"
```

#### Deletar Webhook (Se necessário)
```bash
curl -X POST "https://api.telegram.org/bot<SEU_TOKEN>/deleteWebhook"
```

---

### 7. Comandos Avançados

#### Configurar Bot Description (Texto sob o nome do bot)
```
/setdescription
```

#### Adicionar Menu de Início
```
/setmenu
```

#### Configurar Bot Short Description
```
/setshortdescription
```

---

## 🔐 Segurança

### ❌ NUNCA:
- Compartilhe o token do bot publicamente
- Faça commit do token no Git
- Use o token em client-side

### ✅ SEMPRE:
- Armazene o token no arquivo `.env`
- Adicione `.env` ao `.gitignore`
- Use variáveis de ambiente em produção
- Rotacione o token se exposto

---

## 📊 Monitoramento

### Stats do Bot
BotFather pode mostrar estatísticas:
```
/mybots
```
Selecione seu bot e escolha "Statistics"

### Visualizar Dados do Bot
```bash
# Via API
curl "https://api.telegram.org/bot<SEU_TOKEN>/getMe" | python -m json.tool
```

---

## 🐛 Troubleshooting

### Problema: "Unauthorized"
- Verifique se o token está correto
- Regenere o token no BotFather se necessário

### Problema: Bot não responde
- Verifique se o servidor está rodando
- Veja os logs em `tier1/logs/bot_telegram.log`
- Verifique conexão com internet

### Problema: Webhook não funciona
- Certifique-se que a URL tem HTTPS
- Verifique se o certificado SSL é válido
- Teste a URL com curl

---

## 📞 Suporte

Se tiver problemas:
1. Consulte os logs: `tail -f tier1/logs/bot_telegram.log`
2. Verifique a documentação: https://core.telegram.org/bots/api
3. Contate: contato@genesys-tecnologia.com.br

---

## ✅ Checklist Final

- [ ] Bot criado no BotFather
- [ ] Token copiado e configurado no `.env`
- [ ] Comandos configurados
- [ ] Descrição adicionada
- [ ] Bot testado com `/start`
- [ ] Webhook configurado (produção)
- [ ] Logs funcionando
- [ ] Segurança verificada

---

## 🚀 Próximos Passos

Depois de configurar o bot:
1. Teste todos os comandos
2. Configure integrações com LLM
3. Adicione base de jurisprudência
4. Configure notificações

**Pronto! Seu bot está configurado! 🎉**

