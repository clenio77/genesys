# 🚀 Quick Start - Tier 1

Guia rápido para começar a usar os serviços do TIER 1.

## ⚡ Setup Rápido (5 minutos)

### 1. Clone e Entre
```bash
cd tier1
```

### 2. Configure Variáveis
```bash
cp env.example .env
nano .env
```

**Mínimo necessário:**
- `DATABASE_URL` (já configurado por padrão)
- `TELEGRAM_BOT_TOKEN` (obtenha em @BotFather)
- `GEMINI_API_KEY` ou `OPENAI_API_KEY` (opcional por enquanto)

### 3. Inicie com Docker
```bash
docker-compose up -d
```

### 4. Veja os Logs
```bash
docker-compose logs -f
```

---

## 📱 Configurar Bot de Telegram

**Siga o guia completo:** [TELEGRAM_SETUP.md](docs/TELEGRAM_SETUP.md)

### Resumo rápido:
1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot`
3. Escolha nome e username do bot
4. Copie o **token** gerado
5. Cole no arquivo `.env`:
   ```bash
   TELEGRAM_BOT_TOKEN=seu_token_aqui
   ```

---

## 🧪 Executar Testes

```bash
# Executar todos os testes
./run_tests.sh

# Ou manualmente
pytest tests/ -v
```

---

## 🎯 Testar Serviços

### Bot de Telegram
1. Abra o Telegram
2. Procure por seu bot (ex: `@genesys_legal_bot`)
3. Envie `/start`
4. Teste comandos: `/help`, `/buscar`, `/prazos`

### API de Prazos
```bash
# Ver health
curl http://localhost:8001/health

# Criar prazo
curl -X POST http://localhost:8001/prazos/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "tipo": "contestação",
    "data_vencimento": "2024-12-31"
  }'
```

### Assistente Virtual
```bash
# Abrir WebSocket
# Conecte em: ws://localhost:8002/ws/1

# Ou usar API REST
curl -X POST http://localhost:8002/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "Olá!"
  }'
```

---

## 📊 Monitorar

### Ver todos os logs
```bash
docker-compose logs -f
```

### Logs específicos
```bash
docker-compose logs -f bot-telegram
docker-compose logs -f automacao-prazos
docker-compose logs -f assistente-virtual
```

### Status dos serviços
```bash
docker-compose ps
```

---

## 🛠️ Troubleshooting

### Bot não conecta
```bash
# Verificar token
grep TELEGRAM_BOT_TOKEN .env

# Ver logs
docker-compose logs bot-telegram
```

### Erro de banco de dados
```bash
# Reiniciar banco
docker-compose restart postgres

# Ver logs do banco
docker-compose logs postgres
```

### Porta já em uso
```bash
# Parar tudo
docker-compose down

# Ver portas ocupadas
sudo lsof -i :3000
sudo lsof -i :8001
sudo lsof -i :8002
```

---

## 📚 Documentação

- [README Principal](README.md) - Visão geral
- [Documentação Detalhada](docs/README_TIER1.md) - Arquitetura completa
- [Guia Telegram](docs/TELEGRAM_SETUP.md) - Setup do bot
- [API Documentation](docs/API.md) - Endpoints REST

---

## ✅ Checklist

Antes de usar em produção:

- [ ] Configurar `.env` com todos os tokens
- [ ] Testar Bot de Telegram
- [ ] Testar API de Prazos
- [ ] Testar Assistente Virtual
- [ ] Executar todos os testes
- [ ] Configurar backup do banco de dados
- [ ] Configurar SSL/HTTPS
- [ ] Configurar monitoramento

---

## 🚀 Próximos Passos

1. **Configurar LLM**: Adicione chaves de API no `.env`
2. **Base de Jurisprudência**: Importe dados de decisões
3. **Integrações**: WhatsApp, Email, etc.
4. **Deploy**: Configure CI/CD e deploy em produção

---

## 💡 Dicas

- Use `docker-compose up -d` para rodar em background
- Use `docker-compose logs -f` para acompanhar logs
- Teste cada serviço individualmente antes de usar tudo junto
- Sempre faça backup do banco antes de updates

**Boa sorte! 🎉**

