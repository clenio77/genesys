# 🎯 Onde Usar as Funções de Extração

## 📊 Resumo Rápido

| Sistema | Função Principal | Usa Extração? | Tipo de Uso |
|---------|------------------|---------------|-------------|
| **Kermartin** | 🏭 **COLETA** de dados | ✅ **SIM** | Massiva, automática |
| **Genesys Bot** | 📱 **CONSULTA** de dados | ⚠️ Limitado | Pontual, sob demanda |

---

## 🏭 KERMARTIN - Sistema de Coleta

### **📍 Onde Está:**
```
/home/clenio/Documentos/Meusagentes/kermartin/
```

### **🎯 Função:**
- **COLETA** processos em massa dos tribunais
- Extrai dados de forma **automática** (cron job diário)
- Salva no banco de dados e base RAG
- Atualiza base de conhecimento continuamente

### **✅ Onde Usar Extrações:**

#### **1. Scripts de Coleta:**
```
kermartin/scripts/
├── scraping_tjmg_multiplas_fontes.py      ← USAR AQUI
├── captacao_playwright_robusto.py          ← USAR AQUI
└── coleta_processos/
    ├── coletor_datajud_cnj.py              (já usa API)
    ├── coletor_diarios_playwright.py       ← USAR AQUI
    └── scraping_tjmg_multiplas_fontes.py   ← USAR AQUI
```

#### **2. Como Integrar:**

**Substituir ou Complementar Playwright:**
```python
# kermartin/scripts/scraping_tjmg_multiplas_fontes.py

# ATUAL (Playwright standalone):
from playwright.sync_api import sync_playwright

# NOVO (com Browser MCP se disponível):
# Usar mcp_cursor-ide-browser para testes/debug
# Manter Playwright para produção
```

**Benefícios no Kermartin:**
- ✅ Testar extrações visualmente (Browser MCP)
- ✅ Debugging mais fácil
- ✅ Mapear estrutura de páginas (Firecrawl)
- ✅ Validar seletores antes de codificar

---

## 📱 GENESYS - Bot Telegram

### **📍 Onde Está:**
```
/home/clenio/Documentos/Meusagentes/genesys/products/tier1/bot-telegram/
```

### **🎯 Função:**
- **CONSULTA** processos quando usuário pede
- Responde mensagens do Telegram
- Acessa dados **já coletados** pelo Kermartin
- Faz consultas **pontuais** via API quando necessário

### **⚠️ Onde Usar Extrações (Limitado):**

#### **1. Fluxo Atual do Bot:**

```
Usuário pede processo
    ↓
1. API CNJ (primeira tentativa) ✅
    ↓ (se falhar)
2. Kermartin (dados já coletados) ✅
    ↓ (se não encontrar)
3. Playwright (último recurso) ⚠️
```

#### **2. Arquivos com Extração:**

```
bot-telegram/src/services/
├── cnj_service.py              (API HTTP - não precisa extração)
├── kermartin_service.py        (Lê dados já coletados)
└── playwright_extractor.py     ← Extração pontual (fallback)
```

#### **3. Quando Usar no Genesys:**

**❌ NÃO usar para coleta massiva:**
- Isso é função do Kermartin
- Bot só consulta dados já coletados

**✅ Usar apenas para:**
- **Fallback último recurso** (playwright_extractor.py)
- Quando API CNJ falhar E Kermartin não tiver o processo
- Consulta pontual de processo específico

**Exemplo:**
```python
# bot-telegram/src/services/cnj_service.py

# 1. Tenta API CNJ
if response.status_code == 404:
    # 2. Tenta Kermartin (dados já coletados)
    processo = kermartin_service.buscar_processo_por_numero(numero)
    
    if not processo:
        # 3. ÚLTIMO RECURSO: Extração direta
        from services.playwright_extractor import tribunal_extractor
        async with tribunal_extractor:
            processo = await tribunal_extractor.extrair_processo_tjmg(numero)
```

---

## 🔄 Divisão de Responsabilidades

### **Kermartin (Coletor):**
```
┌─────────────────────────────────────┐
│  KERMARTIN - Sistema de Coleta     │
├─────────────────────────────────────┤
│ ✅ Playwright para scraping        │
│ ✅ API DataJud CNJ                  │
│ ✅ API Escavador                    │
│ ✅ Firecrawl MCP (mapear sites)     │
│ ✅ Browser MCP (testes/debug)       │
│                                     │
│ Objetivo: COLETAR em massa          │
│ Frequência: Diária (cron)           │
│ Quantidade: 50+ processos/dia       │
└─────────────────────────────────────┘
```

### **Genesys Bot (Consultor):**
```
┌─────────────────────────────────────┐
│  GENESYS - Bot de Consulta          │
├─────────────────────────────────────┤
│ ✅ API CNJ (primeira opção)         │
│ ✅ Kermartin Service (dados locais) │
│ ⚠️ Playwright (fallback raro)        │
│                                     │
│ Objetivo: CONSULTAR sob demanda     │
│ Frequência: Quando usuário pede     │
│ Quantidade: 1 processo por vez      │
└─────────────────────────────────────┘
```

---

## 💡 Recomendações

### **1. Para Kermartin:**
**✅ USAR funções de navegador MCP para:**
- Testar novos sites de tribunais
- Validar seletores antes de codificar
- Debugging visual de extrações
- Mapear estrutura de formulários (Firecrawl)

**✅ MANTER Playwright para:**
- Coleta automática em produção
- Roda em background (headless)
- Não depende de extensão do Cursor

---

### **2. Para Genesys:**
**⚠️ USAR limitadamente:**
- Apenas como último recurso (playwright_extractor.py)
- Quando processo não está na base Kermartin
- Consulta pontual e específica

**✅ PRIORIZAR:**
- API CNJ (mais rápido, oficial)
- Kermartin Service (dados já coletados)

---

## 🎯 Resposta Direta

### **Onde usar as funções de extração:**

**🏭 KERMARTIN** ← **PRINCIPAL**
- É onde acontece a coleta massiva
- Já tem Playwright implementado
- Funções MCP podem **complementar** para testes/debug
- Firecrawl útil para **mapear** novos sites

**📱 GENESYS** ← **Limitado**
- Apenas como último recurso (fallback)
- Quando processo não está na base
- Consulta pontual, não coleta massiva

---

## 📝 Conclusão

**As extrações devem ser usadas principalmente no KERMARTIN**, que é o sistema responsável por coletar dados.

No Genesys, a extração é apenas um **fallback raro** quando:
1. API CNJ não encontra
2. Kermartin não tem o processo
3. Precisa buscar diretamente no tribunal

**Arquitetura ideal:**
```
Kermartin (coleta) → Banco de Dados → Genesys (consulta)
                         ↑
                  Extrações aqui!
```

