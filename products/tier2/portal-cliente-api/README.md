# Portal do Cliente - API

API RESTful para o Portal do Cliente, permitindo que clientes acompanhem seus processos judiciais em tempo real.

## 🚀 Funcionalidades

- **Autenticação por CPF**: Login simplificado para clientes
- **Listagem de Processos**: Visualização de todos os processos do cliente
- **Timeline Detalhada**: Histórico completo de movimentações processuais
- **Tradutor Jurídico**: Linguagem simplificada para o cliente final

## 🏗️ Tecnologias

- **FastAPI**: Framework web assíncrono
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados leve (produção deve usar PostgreSQL)
- **Pydantic**: Validação de dados

## 📦 Instalação

```bash
# Ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## ▶️ Executar

```bash
# Método 1: Script automatizado
./run.sh

# Método 2: Manual
uvicorn app.main:app --reload --port 8001
```

A API estará disponível em: `http://localhost:8001`

## 📚 Documentação da API

Acesse `http://localhost:8001/docs` para ver a documentação interativa (Swagger UI).

### Endpoints Principais

#### POST `/api/auth/login`
Autenticação do cliente via CPF.

**Request Body:**
```json
{
  "cpf": "123.456.789-00"
}
```

**Response:**
```json
{
  "token": "demo-token",
  "user": {
    "name": "Cliente Exemplo",
    "id": 1
  }
}
```

#### GET `/api/processos`
Lista todos os processos do cliente autenticado.

**Response:**
```json
[
  {
    "id": 1,
    "cnj": "5001234-12.2024.8.13.0024",
    "title": "Ação de Indenização - Danos Morais",
    "status": "Em Andamento",
    "last_update": "2025-11-20T00:00:00",
    "next_step": "Aguardando decisão do Juiz",
    "lawyer_name": "Dr. Carlos Silva",
    "timeline": [...]
  }
]
```

#### GET `/api/processos/{process_id}`
Detalhes de um processo específico.

## 🗄️ Estrutura do Banco de Dados

### Tabela `users`
- `id`: INT (PK)
- `cpf`: STRING (Unique)
- `name`: STRING
- `hashed_password`: STRING

### Tabela `processes`
- `id`: INT (PK)
- `cnj`: STRING (Unique)
- `title`: STRING
- `status`: STRING
- `last_update`: DATETIME
- `next_step`: STRING
- `lawyer_name`: STRING
- `client_id`: INT (FK → users.id)

### Tabela `timeline_events`
- `id`: INT (PK)
- `date`: DATETIME
- `title`: STRING
- `description`: STRING (tradução simplificada)
- `icon_type`: STRING (gavel, file, check, clock, user)
- `status`: STRING (current, completed)
- `process_id`: INT (FK → processes.id)

## 🔐 Dados de Teste

O sistema é populado automaticamente com dados de exemplo:

**CPF de Teste:** `123.456.789-00`

Este CPF tem acesso a 2 processos:
1. Ação de Indenização - Danos Morais
2. Reclamação Trabalhista

## 🔄 Integração com Frontend

O frontend Next.js em `/src/app/portal-cliente/page.tsx` consome esta API.

**Configuração CORS:** Permite requisições de `http://localhost:3000`

## 🚧 TODOs para Produção

- [ ] Implementar JWT real (atualmente usa token "demo")
- [ ] Hash de senhas com bcrypt
- [ ] Migrar de SQLite para PostgreSQL
- [ ] Implementar rate limiting
- [ ] Adicionar logs estruturados
- [ ] Implementar cache (Redis)
- [ ] Adicionar testes automatizados
- [ ] WebSocket para atualizações em tempo real
- [ ] Sincronização automática com PJe/e-SAJ

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação principal do projeto.
