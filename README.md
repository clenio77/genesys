# Genesys Tecnologia — Implantação e Operação do Kermartin IA

Site institucional e documentação comercial da **Genesys Tecnologia**: consultoria jurídico-tecnológica que **implanta, opera e governa** o **Kermartin IA** — plataforma de análise jurídica com inteligência artificial.

> **Genesys** = empresa / serviços / go-to-market  
> **Kermartin** = produto (plataforma SaaS, repositório em `../kermartin/`)

---

## Posicionamento

| Papel | Descrição |
|-------|-----------|
| **Kermartin IA** | Produto central — análise jurídica por blocos BMAD, módulos por área, RAG, perfis estratégicos |
| **Genesys** | Parceira de implantação, operação, automação, LGPD e integrações |

### Serviços principais
- **Implantação do Kermartin** — diagnóstico, módulos, bases, treinamento, governança (30–90 dias)
- **Operação e Suporte** — suporte contínuo, análises assistidas, evolução de fluxos

### Serviços complementares
- **Automação de Processos** — upload, triagem, peças assistidas, webhooks
- **Governança, Compliance e LGPD** — anonimização, políticas, RIPD, auditoria
- **Integração com Sistemas** — PJe, e-SAJ, CRM, ERP, WhatsApp ([/integracoes](/integracoes))

> Pesquisa jurisprudencial e gestão de conhecimento **não são serviços avulsos** — são capacidades nativas do Kermartin, configuradas na implantação.

---

## Stack do Site

- **Next.js 14** (App Router) + **TypeScript** + **Tailwind CSS**
- **Framer Motion** — animações
- **PWA** — manifest + service worker
- Deploy recomendado: **Vercel**

---

## Como Executar

```bash
cd genesys
npm install
npm run dev    # http://localhost:3000
npm run build  # produção
```

---

## Estrutura Principal

```
genesys/
├── src/
│   ├── app/
│   │   ├── page.tsx                 # Homepage
│   │   ├── produtos/                # Kermartin e ofertas
│   │   ├── servicos/                # Implantação, operação, complementares
│   │   ├── integracoes/             # Conectores e APIs
│   │   └── sobre/                   # Empresa e equipe
│   └── components/
│       ├── ProductCarousel.tsx      # Hero — Kermartin + casos de uso
│       ├── ServicesSection.tsx      # Serviços na homepage
│       ├── KermartinSection.tsx     # Destaque do produto
│       └── PricingSection.tsx       # Planos Kermartin
├── ANALISE_SERVICOS_KERMARTIN.md    # Estratégia Genesys × Kermartin
└── README.md
```

---

## Páginas-chave

| Rota | Conteúdo |
|------|----------|
| `/` | Homepage — Kermartin no centro, serviços Genesys |
| `/produtos/kermartin-ia` | Produto — módulos, blocos, planos |
| `/servicos` | Implantação + operação (principais) e automação/LGPD/integração (complementares) |
| `/integracoes` | Ecossistema de conectores |
| `/sobre` | História, equipe, missão |
| `/servicos/gestao-conhecimento` | Redirect conceitual → capacidade do Kermartin |

---

## Kermartin — Resumo do Produto

Plataforma jurídica com arquitetura **BMAD** (Business, Model, Application, Domain):

- **Stack:** Django + React + PostgreSQL/pgvector + Gemini
- **6+ blocos** de análise (tipificação, provas, estratégia, jurisprudência, recursos, perfis)
- **Módulos:** penal/júri (produção), civil, trânsito, tributário, administrativo, trabalhista (beta)
- **RAG:** bases privadas, busca semântica, guardrails de citação
- **Perfis estratégicos:** jurados, magistrados, promotores
- **Auditoria pública:** licitações, score de risco, dashboards
- **LGPD:** anonimização antes do LLM, validação de entrada

Documentação técnica completa: [`../kermartin/README.md`](../kermartin/README.md)

---

## Casos de Uso (derivados do Kermartin)

1. **Defesa penal / Tribunal do Júri** — análise por blocos, teses, perfis de plenário
2. **Civil e execução** — deep scan de prova, estratégia de execução
3. **Trânsito e tributário** — defesas administrativas, revisão fiscal
4. **Auditoria pública** — licitações, irregularidades, evidências
5. **Departamentos jurídicos** — base privada, pesquisa auditável, relatórios Markdown
6. **Operação assistida Genesys** — equipe não opera sozinha; entrega com revisão humana

---

## Documentação Complementar

- [ANALISE_SERVICOS_KERMARTIN.md](./ANALISE_SERVICOS_KERMARTIN.md) — modelo de negócio e matriz serviços × produto
- [PLANO_MELHORIAS.md](./PLANO_MELHORIAS.md) — roadmap de UX/design
- [ROADMAP_IMPLEMENTACAO.md](./ROADMAP_IMPLEMENTACAO.md) — cronograma de sprints

---

## Contato

- **WhatsApp:** +55 34 99826-4603
- **Site:** https://genesys-tecnologia.com.br
- **Produto:** Kermartin IA — https://kermartin.com

---

**Genesys Tecnologia** — Kermartin no centro, implantação na Genesys.
