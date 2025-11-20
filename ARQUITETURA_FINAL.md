# 🏗️ Arquitetura Final - Genesys Tecnologia

## 📊 Visão Geral

Arquitetura **escalável**, **modular** e **fácil de manter** com produtos separados.

## 🌐 Estrutura Completa

```
genesys/
│
├── site/                          # Site institucional (Next.js)
│   ├── Apresenta a empresa
│   ├── Mostra produtos
│   └── CTA para contato
│
├── products/                      # Produtos separados
│   ├── tier1/
│   │   ├── bot-telegram/         # Bot Telegram Jurídico
│   │   ├── automacao-prazos/     # Automação de Prazos
│   │   └── assistente-virtual/   # Assistente 24/7
│   └── shared/                    # Código compartilhado
│
└── docs/                          # Documentação geral
    ├── README.md
    └── arquitetura/
```

---

## 🌟 PRODUTOS

### 1. Site Institucional
**Tecnologia:** Next.js 14 + TypeScript + Tailwind CSS

**URL:** `https://genesys.com.br`

**Responsabilidades:**
- ✅ Apresentar a empresa
- ✅ Mostrar produtos e serviços
- ✅ Captar leads
- ✅ Contato e informações

**Conteúdo:**
- Hero com value proposition
- Produtos da Genesys (Bot, Prazos, Assistente)
- Portfólio (ex: Kermartin IA)
- Equipe
- Depoimentos
- Contato

**NÃO contém:**
- ❌ Lógica de negócio dos produtos
- ❌ Banco de dados complexo
- ❌ Processamento pesado

---

### 2. Bot de Telegram Jurídico
**Tecnologia:** Python + FastAPI + Telegram Bot API

**URL:** `https://bot.genesys.com.br`

**Responsabilidades:**
- ✅ Chat com IA para consultas jurídicas
- ✅ Busca de jurisprudência
- ✅ Alertas de prazos
- ✅ Processamento de linguagem natural

**Deployment:**
```bash
cd products/tier1
docker-compose up -d bot-telegram postgres redis
```

**Banco de Dados:**
- PostgreSQL separado
- Schema próprio

**Recursos:**
- 8 comandos (`/start`, `/help`, `/buscar`, etc)
- Integração com LLM
- Histórico de conversas

---

### 3. Automação de Prazos
**Tecnologia:** Python + FastAPI + APScheduler

**URL:** `https://prazos.genesys.com.br`

**Responsabilidades:**
- ✅ Monitorar prazos processuais
- ✅ Enviar alertas (7, 3, 1 dia antes)
- ✅ Dashboard de prazos
- ✅ API REST para integrações

**Deployment:**
```bash
cd products/tier1
docker-compose up -d automacao-prazos postgres redis
```

**Características:**
- Agendamento automático (APScheduler)
- Notificações multi-canal (Email, Telegram, WhatsApp)
- Dashboard web próprio
- API REST completa

---

### 4. Assistente Virtual 24/7
**Tecnologia:** Python + FastAPI + WebSocket

**URL:** `https://assistente.genesys.com.br`

**Integração no site:**
```typescript
// Widget embutido no site
<AssistenteVirtual 
  apiUrl="https://assistente.genesys.com.br"
  channel="web"
/>
```

**Responsabilidades:**
- ✅ Chat inteligente 24/7
- ✅ Qualificação de leads
- ✅ FAQ com IA
- ✅ Conversação natural

**Deployment:**
```bash
cd products/tier1
docker-compose up -d assistente-virtual postgres redis
```

**Características:**
- WebSocket para chat em tempo real
- API REST alternativa
- Extração automática de informações
- Score de leads

---

## 🗄️ BANCO DE DADOS

### Estratégia: Separado

```
bot-telegram          →   bot_db (PostgreSQL)
automacao-prazos      →   prazos_db (PostgreSQL)
assistente-virtual    →   assistente_db (PostgreSQL)
```

**Vantagens:**
- ✅ Isolamento total
- ✅ Escala independente
- ✅ Backup separado
- ✅ Sem conflitos de schema

---

## 🚀 DEPLOYMENT

### Opção 1: Domínios Separados (Recomendado)

```bash
# Site institucional
genesys.com.br       →  Vercel/Netlify

# Produtos
bot.genesys.com.br   →  Render/Fly.io (Python)
prazos.genesys.com.br →  Render/Fly.io (Python)
assistente.genesys.com.br →  Render/Fly.io (Python)

# Database
Supabase ou Neon   →  PostgreSQL (x3)
Redis Cloud       →  Redis
```

### Opção 2: Subdomínios Mesmo Servidor

```bash
# Todos em um servidor
genesys.com.br         # Nginx reverse proxy
├── /                 # Site Next.js
├── /api/bot          # Proxy para bot
├── /api/prazos       # Proxy para prazos
└── /api/assistente   # Proxy para assistente
```

---

## 📱 INTEGRAÇÃO NO SITE

### Como o site apresenta os produtos:

```typescript
// Página de Produtos
export default function ProductsPage() {
  return (
    <div>
      <h1>Nossos Produtos de IA Jurídica</h1>
      
      <ProductCard
        title="Bot de Telegram Jurídico"
        description="Consultas jurídicas 24/7 via Telegram"
        features={[
          "Busca de jurisprudência",
          "Análise de processos",
          "Alertas automáticos"
        ]}
        cta="Experimentar Grátis"
        href="https://t.me/genesys_legal_bot"
        icon={<FaTelegram />}
      />
      
      <ProductCard
        title="Automação de Prazos"
        description="Nunca perca um prazo novamente"
        features={[
          "Alertas 7, 3 e 1 dia antes",
          "Dashboard personalizado",
          "Integração com tribunais"
        ]}
        cta="Começar Agora"
        href="https://prazos.genesys.com.br/signup"
        icon={<FaCalendar />}
      />
      
      <ProductCard
        title="Assistente Virtual"
        description="Atendimento inteligente para seu site"
        features={[
          "Qualificação de leads",
          "FAQ automático",
          "Multi-idioma"
        ]}
        cta="Integrar Gratuitamente"
        href="#assistente"
        icon={<FaRobot />}
      />
    </div>
  )
}
```

---

## 🔐 SEGURANÇA

### Cada produto tem:
- ✅ Autenticação própria
- ✅ API keys separadas
- ✅ Rate limiting
- ✅ CORS configurado
- ✅ SSL obrigatório

### Tokens necessários:
```bash
# Bot de Telegram
TELEGRAM_BOT_TOKEN

# AI APIs
OPENAI_API_KEY ou GEMINI_API_KEY

# Integração WhatsApp
WHATSAPP_ACCESS_TOKEN
```

---

## 📊 MONITORAMENTO

### Por produto:
- ✅ Logs separados
- ✅ Métricas independentes
- ✅ Alertas específicos
- ✅ Uptime independente

### Ferramentas:
- Sentry (erros)
- Prometheus (métricas)
- Grafana (dashboards)
- Uptime Robot (disponibilidade)

---

## 💰 CUSTOS

### Por produto/mês:

| Produto | Infra | LLM | Total |
|---------|-------|-----|-------|
| Bot Telegram | R$ 500-800 | R$ 200-500 | R$ 700-1.3k |
| Prazos | R$ 600-1k | R$ 100-300 | R$ 700-1.3k |
| Assistente | R$ 700-1.2k | R$ 300-800 | R$ 1k-2k |
| **Total** | **R$ 1.8k-3k** | **R$ 600-1.6k** | **R$ 2.4k-4.6k** |

---

## ✅ VANTAGENS DESTA ARQUITETURA

1. **Escalabilidade**: Cada produto escala independente
2. **Manutenção**: Equipes separadas, deploys isolados
3. **Segurança**: Falha em um produto não afeta os outros
4. **Performance**: Cada produto otimizado para seu propósito
5. **Flexibilidade**: Pode trocar stack de cada produto
6. **Isolamento**: Bugs não se propagam
7. **Deploy independente**: Sem downtime geral

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Estrutura criada
2. ✅ Produtos implementados
3. ⏳ Configurar deploy em produção
4. ⏳ Obter domínios (bot.genesys.com.br, etc)
5. ⏳ Configurar SSL
6. ⏳ Configurar monitoramento
7. ⏳ Testar integração completa

---

**Arquitetura definida e implementada! 🎉**

