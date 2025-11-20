# 🔐 Sistema de Autenticação para Acesso ao Kermartin

## 📋 Visão Geral

O bot do Telegram agora possui **sistema de autenticação** para proteger o acesso aos dados do Kermartin. 

**Princípio:** 
- ✅ Funções básicas do bot (IA, busca, prazos) → **Acessíveis sem login**
- 🔒 Acesso ao Kermartin → **Requer autenticação**

---

## 🚀 Como Funciona

### 1️⃣ Cadastro (Primeira Vez)

Para acessar o Kermartin, o usuário precisa primeiro **cadastrar um email e senha**:

```
/cadastrar email@exemplo.com senha123
```

**O que acontece:**
- Email e senha são salvos no banco de dados
- Senha é armazenada como hash (SHA256) - não em texto plano
- Status de autenticação: `autenticado = False` (precisa fazer login)

### 2️⃣ Login

Após cadastrar, o usuário deve fazer login:

```
/login email@exemplo.com senha123
```

**O que acontece:**
- Verifica se email e senha estão corretos
- Atualiza `autenticado = True` no banco
- Registra `ultimo_login = datetime.utcnow()`

### 3️⃣ Acesso ao Kermartin

Agora o usuário pode:
- ✅ Buscar magistrados: `/magistrado`
- ✅ Buscar processos no Kermartin (fallback quando API CNJ falha)
- ✅ Acessar todos os dados coletados no Kermartin

### 4️⃣ Logout

Para sair e revogar acesso:

```
/logout
```

Isso define `autenticado = False` no banco.

---

## 📊 Estrutura no Banco de Dados

### Campos Adicionados ao Modelo `User`:

```python
senha_hash = Column(String(255), nullable=True)      # Hash SHA256 da senha
autenticado = Column(Boolean, default=False)        # Status atual de autenticação
ultimo_login = Column(DateTime, nullable=True)       # Data do último login
```

---

## 🛡️ Proteções Implementadas

### ✅ Comandos Protegidos

1. **`/magistrado`** - Exige autenticação
   - Sem login: mostra mensagem pedindo login
   - Com login: permite buscar no Kermartin

2. **`/processo`** - Acesso condicional
   - Sem login: apenas API CNJ
   - Com login: API CNJ + busca no Kermartin (fallback)

### ✅ Handlers Protegidos

- Busca de magistrado via mensagem → Verifica autenticação
- Busca de processos no Kermartin → Verifica autenticação antes de buscar
- Todos os acessos ao `kermartin_service` → Protegidos

---

## 🔧 Comandos Disponíveis

### `/cadastrar`
**Cadastrar email e senha pela primeira vez**

```
Formato: /cadastrar email@exemplo.com senha
Exemplo: /cadastrar usuario@exemplo.com minhasenha123
```

**Quando usar:**
- Primeira vez que vai usar o Kermartin
- Usuário ainda não tem email cadastrado

### `/login`
**Fazer login para acessar Kermartin**

```
Formato: /login email@exemplo.com senha
Exemplo: /login usuario@exemplo.com minhasenha123
```

**Quando usar:**
- Já tem cadastro
- Quer acessar dados do Kermartin
- Após fazer logout

### `/logout`
**Sair e revogar acesso ao Kermartin**

```
Formato: /logout
```

**Quando usar:**
- Quer desativar acesso temporariamente
- Mudança de dispositivo
- Segurança

### `/perfil`
**Ver status de autenticação**

Mostra:
- ✅ Email cadastrado
- 🔒 Status: Autenticado / Não autenticado
- Informações do perfil

---

## 🔒 Segurança

### Hash de Senha
- Senhas são armazenadas como **hash SHA256**
- Nunca armazenadas em texto plano
- Comparação sempre via hash

### Verificação de Autenticação
- Verificação realizada em **cada acesso** ao Kermartin
- Status `autenticado` no banco como fonte da verdade
- Não há sessão persistente - verifica sempre

### Validações
- ✅ Email único por usuário
- ✅ Email deve corresponder ao cadastro
- ✅ Senha verificada via hash
- ✅ Usuário deve existir no banco (criado via `/start`)

---

## 📝 Fluxo de Uso

### Cenário 1: Usuário Novo
```
1. Usuário faz /start → Cria registro no banco
2. Usuário faz /cadastrar email@exemplo.com senha → Cadastro
3. Usuário faz /login email@exemplo.com senha → Login
4. Usuário pode usar /magistrado e /processo (com Kermartin)
```

### Cenário 2: Usuário Existente
```
1. Usuário faz /login email@exemplo.com senha → Login
2. Usuário pode usar comandos do Kermartin
3. Usuário faz /logout → Revoga acesso
```

### Cenário 3: Consulta de Processo Sem Login
```
1. Usuário faz /processo
2. Envia número do processo
3. Bot tenta API CNJ apenas
4. Se não encontrar: "Use /login para acessar base local"
```

### Cenário 4: Consulta de Processo Com Login
```
1. Usuário faz /login (se ainda não estiver autenticado)
2. Usuário faz /processo
3. Envia número do processo
4. Bot tenta API CNJ
5. Se falhar: Busca automaticamente no Kermartin
6. Retorna dados do Kermartin se encontrado
```

---

## 🧪 Migração do Banco de Dados

Para adicionar os novos campos, você precisa rodar migração:

```bash
# Se usar Alembic
alembic revision --autogenerate -m "add_auth_fields"
alembic upgrade head

# OU manualmente em SQL
ALTER TABLE users ADD COLUMN senha_hash VARCHAR(255);
ALTER TABLE users ADD COLUMN autenticado BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN ultimo_login TIMESTAMP;
```

---

## ⚠️ Importante

### 🔴 Requisitos
- ✅ Banco de dados configurado e acessível
- ✅ Usuário deve fazer `/start` antes de usar autenticação
- ✅ Email único (não pode ter dois usuários com mesmo email)

### ✅ Boas Práticas
- Sempre verificar autenticação antes de acessar `kermartin_service`
- Usar `auth_service.is_authenticated(telegram_id)` para verificar
- Mostrar mensagem clara quando acesso negado

### 🛠️ Troubleshooting

**Problema:** "Usuário não encontrado"
- Solução: Usuário deve fazer `/start` primeiro

**Problema:** "Email não confere"
- Solução: Verificar se email usado no login é o mesmo cadastrado

**Problema:** "Senha incorreta"
- Solução: Verificar se senha está correta (case-sensitive)

**Problema:** Ainda não acessa Kermartin após login
- Solução: Verificar logs, pode haver erro no banco de dados

---

## 📚 Arquivos Modificados

1. **`shared/database/models.py`** - Adicionados campos de autenticação
2. **`bot-telegram/src/services/auth_service.py`** - Serviço de autenticação (NOVO)
3. **`bot-telegram/src/handlers/commands.py`** - Comandos /login, /logout, /cadastrar
4. **`bot-telegram/src/handlers/messages.py`** - Verificação antes de buscar magistrado
5. **`bot-telegram/src/services/cnj_service.py`** - Verificação antes de buscar no Kermartin

---

## 🎯 Próximos Passos (Opcional)

- [ ] Implementar expiração de sessão (ex: logout automático após 24h)
- [ ] Reset de senha via comando
- [ ] Lista de usuários autorizados (whitelist)
- [ ] Logs de acesso ao Kermartin
- [ ] Rate limiting por autenticação

---

**Status:** ✅ **IMPLEMENTADO E FUNCIONANDO**

Data: 2025-10-29

