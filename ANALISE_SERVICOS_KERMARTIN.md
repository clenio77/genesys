# Análise de Serviços — Genesys × Kermartin

**Data:** 12/07/2026  
**Versão:** 2.0  
**Status:** Posicionamento alinhado (site + docs)

---

## Visão Geral

A **Genesys Tecnologia** é a consultoria que **implanta, opera e governa** o **Kermartin IA**.  
O **Kermartin** é o produto (plataforma SaaS de análise jurídica com IA) — não confundir com a Genesys.

```
┌─────────────────────────────────────────────────────────┐
│  GENESYS (empresa)          KERMARTIN (produto)         │
│                                                          │
│  • Implantação      ──────►  • Plataforma BMAD           │
│  • Operação/Suporte        • Módulos por área          │
│  • Automação (compl.)      • RAG e base privada         │
│  • LGPD (compl.)           • Perfis estratégicos        │
│  • Integração (compl.)     • Auditoria pública          │
└─────────────────────────────────────────────────────────┘
```

---

## Serviços no Site (v2)

### Principais

| Serviço | Descrição | Relação com Kermartin |
|---------|-----------|----------------------|
| **Implantação** | Diagnóstico, módulos, bases, treinamento, governança | Onboarding da plataforma no fluxo do cliente |
| **Operação e Suporte** | Suporte contínuo, análises assistidas, revisão humana | Operação assistida sobre o Kermartin já implantado |

### Complementares

| Serviço | Descrição | Relação com Kermartin |
|---------|-----------|----------------------|
| **Automação** | Upload, triagem, peças, webhooks | Fluxos conectados ao Kermartin |
| **LGPD / Governança** | Anonimização, políticas, RIPD, auditoria | Camada de segurança na operação do Kermartin |
| **Integração** | PJe, CRM, ERP, WhatsApp | Kermartin no ecossistema existente |

---

## O que NÃO vendemos como serviço avulso

| Antigo posicionamento | Novo framing |
|----------------------|--------------|
| Pesquisa de Jurisprudência | Capacidade nativa do Kermartin (RAG + fontes) |
| Gestão de Conhecimento | Base privada configurada na implantação |
| Análise Jurídica standalone | Módulos do Kermartin + operação assistida Genesys |
| Auditoria Pública standalone | Módulo Kermartin + operação Genesys |

A página `/servicos/gestao-conhecimento` foi reframed como **capacidade do Kermartin**, com CTAs para produto e implantação.

---

## Matriz de Integração (atualizada)

| Oferta | Tipo | Integração Kermartin |
|--------|------|---------------------|
| Implantação | Serviço principal | 100% — é onboarding do produto |
| Operação/Suporte | Serviço principal | 100% — operação assistida |
| Automação | Complementar | 70% — fluxos conectados |
| LGPD | Complementar | 60% — governança da operação |
| Integração | Complementar | 80% — conectores ao produto |
| Pesquisa / KM | ~~Serviço~~ → **Produto** | 100% — feature do Kermartin |

---

## Casos de Uso do Kermartin (base para marketing Genesys)

1. **Penal / Júri** — 6+ blocos, perfis de jurados/magistrados/promotores
2. **Civil** — prova, execução, estratégia processual
3. **Trânsito** — defesa administrativa (CTB)
4. **Tributário** — revisão fiscal, lançamentos, recursos
5. **Auditoria pública** — licitações, score de risco, dashboards
6. **Base privada** — pesquisa semântica com citações auditáveis

**Público-alvo:** escritórios de advocacia, departamentos jurídicos corporativos, órgãos de controle, consultorias especializadas.

**Stack Kermartin:** Django, React, PostgreSQL/pgvector, Gemini, arquitetura BMAD.

---

## Modelo Comercial Recomendado

```
Cliente → Implantação Genesys (30–90 dias) → Operação contínua + plano Kermartin
          R$ 5.000+/mês (projeto)              Assinatura SaaS + suporte
```

**Bundles:** implantação + plano Professional/Enterprise + complementares (automação, LGPD, integração) sob proposta.

---

## Pendências / Próximos Passos

- [ ] Atualizar `/produtos/pesquisa-juridica` com redirect ou reframing (página legada ainda existe)
- [ ] Revisar depoimentos que citam "pesquisa jurídica" como serviço Genesys avulso
- [ ] Alinhar página `/pricing` standalone com PricingSection da homepage
- [ ] Validar números de marketing (500+ clientes, 50K casos) com dados reais

---

*Documento atualizado em 12/07/2026 — v2.0 alinhada ao reposicionamento Codex + revisão Cursor.*
