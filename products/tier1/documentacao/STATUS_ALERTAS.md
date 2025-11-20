# 📊 Status da Implementação de Alertas

## ✅ O Que Já Está Implementado

### 1. **Interface do Comando `/alerta`**
- ✅ Comando funcional que exibe menu com botões
- ✅ Opções disponíveis:
  - 📧 Via Email
  - 📱 Via Telegram
  - ⏰ Intervalos: 7, 3, 1 dia(s)
  - ✏️ Personalizado
- ✅ Callbacks respondem corretamente aos cliques

### 2. **Modelos de Banco de Dados**
- ✅ Tabela `alertas` - Para alertas gerais
- ✅ Tabela `notificacoes` - Para histórico de notificações enviadas
- ✅ Tabela `prazos` - Com campos `alertas_enviados` e `ultima_notificacao`

### 3. **Estrutura Básica**
- ✅ Handlers de comandos registrados
- ✅ Sistema de callbacks funcionando
- ✅ Logging das ações do usuário

---

## ❌ O Que Falta Implementar

### 1. **Persistência de Preferências** 🔴 CRÍTICO
**Status:** ⚠️ Apenas logs, não salva no banco

**Problema:**
```python
# TODO: Salvar preferência no banco
logger.info(f"Usuário {user_id} configurou alertas via {canal}")
```

**Precisa:**
- Criar tabela `preferencias_alertas` ou adicionar campos ao modelo `User`
- Salvar canal preferido (email/telegram)
- Salvar intervalo de dias para alertas
- Salvar outras configurações (frequência, prioridade mínima)

### 2. **Serviço de Alertas** 🔴 CRÍTICO
**Status:** ❌ Não existe

**Precisa criar:**
- `services/alertas_service.py` com funções:
  - `criar_alerta()` - Criar alerta no banco
  - `enviar_alerta()` - Enviar notificação
  - `listar_alertas_pendentes()` - Buscar alertas para enviar
  - `marcar_enviado()` - Atualizar status

### 3. **Sistema de Agendamento** 🟡 IMPORTANTE
**Status:** ❌ Não implementado no bot

**Precisa:**
- Integração com `automacao-prazos/src/scheduler.py` (já existe)
- Ou criar scheduler próprio no bot
- Verificar prazos vencendo e enviar alertas

### 4. **Envio de Notificações** 🟡 IMPORTANTE
**Status:** ❌ Apenas mock

**Precisa:**
- Enviar mensagem via Telegram (bot já está disponível)
- Enviar email (requer configuração SMTP)
- Registrar no histórico (`notificacoes`)

### 5. **Funcionalidade "Personalizado"** 🟢 BAIXA PRIORIDADE
**Status:** ⚠️ Botão existe mas não faz nada

**Precisa:**
- Permitir usuário digitar intervalo customizado
- Validar entrada
- Salvar preferência

---

## 📋 Esquema Atual vs Esperado

### Atual (Simplificado)
```
Usuário → /alerta → Botões → Callback → Log → Fim
```

### Esperado (Completo)
```
Usuário → /alerta → Botões → Callback → Salvar Preferências
                                              ↓
Scheduler → Verifica Prazos → Cria Alertas → Envia Notificações → Registra
```

---

## 🗄️ Estrutura de Dados Necessária

### Preferências de Alerta (Nova ou adicionar a User)
```python
{
    "user_id": int,
    "canal_preferido": "telegram" | "email" | "ambos",
    "intervalo_dias": int,  # 1, 3, 7 ou customizado
    "horario_envio": "time",  # ex: "09:00"
    "prioridade_minima": "baixa" | "media" | "alta",
    "ativo": boolean
}
```

---

## 🔧 Arquivos Envolvidos

### Já Existem
- ✅ `bot-telegram/src/handlers/commands.py` (cmd_alerta, button_callback)
- ✅ `shared/database/models.py` (Alerta, Notificacao, Prazo)
- ✅ `bot-telegram/src/services/database_service.py` (base)

### Precisam Ser Criados/Atualizados
- ❌ `bot-telegram/src/services/alertas_service.py` **NOVO**
- ❌ Atualizar `button_callback` para salvar preferências
- ❌ Integrar scheduler ou criar sistema de verificação periódica
- ❌ `bot-telegram/src/services/notifier_service.py` **NOVO** (opcional)

---

## 🎯 Próximos Passos Sugeridos

### Prioridade 1 (Essencial)
1. Criar serviço de alertas básico
2. Implementar salvamento de preferências
3. Criar função de envio de alertas via Telegram

### Prioridade 2 (Importante)
4. Integrar verificação de prazos
5. Sistema de agendamento/verificação periódica
6. Histórico de notificações enviadas

### Prioridade 3 (Melhorias)
7. Envio por email
8. Personalização avançada
9. Dashboard de alertas

---

**Status Geral:** ⚠️ **PARCIALMENTE IMPLEMENTADO** (Interface pronta, funcionalidade básica faltando)

