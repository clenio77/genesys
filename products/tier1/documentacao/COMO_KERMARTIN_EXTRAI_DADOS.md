# 🔍 Como o Kermartin Extrai Dados de Processos

Documentação completa sobre os métodos e locais de configuração de extração de dados.

---

## 📊 Visão Geral

O Kermartin usa **múltiplas estratégias** para coletar dados de processos:

1. **API DataJud CNJ** (oficial, grátis)
2. **Scraping com Playwright** (TJMG, TJSP, TRF)
3. **Escavador API** (pago, R$ 0,05/processo)
4. **Firecrawl MCP** (para sites complexos)

---

## 🗂️ Onde Está Configurado

### **1. Scripts Principais de Extração**

#### **📍 Pasta:** `/home/clenio/Documentos/Meusagentes/kermartin/scripts/`

**Arquivos principais:**

1. **`scraping_tjmg_multiplas_fontes.py`** ⭐
   - Tenta múltiplas fontes: PJe, eproc, sistema antigo
   - URLs configuradas para TJMG
   - Usa Playwright para navegação

2. **`captacao_playwright_robusto.py`**
   - Extração robusta com Playwright
   - Fallbacks e seletores genéricos
   - Para captação de clientes/advogados

3. **`scraping_portais_juridicos.py`**
   - Extração de portais jurídicos (Jusbrasil, etc)
   - Usa Playwright para sites JavaScript

---

### **2. Scripts de Coleta de Processos**

#### **📍 Pasta:** `/home/clenio/Documentos/Meusagentes/kermartin/scripts/coleta_processos/`

**Arquivos principais:**

1. **`coletor_datajud_cnj.py`**
   - Coleta via API oficial do CNJ (DataJud)
   - **URL Base:** `https://api-publica.datajud.cnj.jus.br/api/v1/`
   - Método: HTTP requests diretos

2. **`coletor_datajud_uberlandia_penal.py`**
   - Específico para processos penais de Uberlândia
   - Usa API DataJud CNJ

3. **`coletor_escavador_uberlandia_penal.py`**
   - Coleta via API do Escavador (pago)
   - **Custo:** R$ 0,05 por processo

4. **`coletor_diarios_playwright.py`**
   - Extrai dos diários oficiais
   - Usa Playwright para navegação

5. **`scraping_tjmg_multiplas_fontes.py`**
   - Scraping direto dos sites do TJMG
   - Múltiplas estratégias de fallback

---

## 🔧 Configurações de URLs e Endpoints

### **TJMG - Múltiplas Fontes**

**Arquivo:** `scripts/scraping_tjmg_multiplas_fontes.py`

```python
self.urls = {
    'pje': 'https://pje.tjmg.jus.br/pje/ConsultaPublica/listView.seam',
    'eproc': 'https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica',
    'sistema_antigo': 'https://www4.tjmg.jus.br/juridico/sf/index.jsp'
}
```

**Ordem de tentativa:**
1. **eproc** (mais simples, primeiro)
2. **PJe** (segundo)
3. **sistema_antigo** (backup)

---

### **API DataJud CNJ (Oficial)**

**Arquivo:** `scripts/coleta_processos/coletor_datajud_cnj.py`

**Configuração:**
- **URL Base:** `https://api-publica.datajud.cnj.jus.br/api/v1/`
- **Autenticação:** Não requer (pública)
- **Endpoints:**
  - `/processos` - Buscar processos
  - `/orgaos` - Listar órgãos
  - `/assuntos` - Listar assuntos

**Exemplo de uso:**
```python
import requests

url = "https://api-publica.datajud.cnj.jus.br/api/v1/processos"
params = {
    'numero': '0000123-45.2024.8.13.0024',
    'tribunal': 'TJMG'
}
response = requests.get(url, params=params)
```

---

### **API Escavador (Pago)**

**Arquivo:** `scripts/coleta_processos/coletor_escavador_uberlandia_penal.py`

**Configuração:**
- **URL Base:** `https://api.escavador.com/v1/`
- **Autenticação:** Token (requer API key)
- **Custo:** R$ 0,05 por processo consultado

**Configuração do token:**
```python
# Em CONFIG_ESCAVADOR_V2.md
ESCAVADOR_API_KEY = "seu_token_aqui"
```

---

### **Portais Jurídicos**

**Arquivo:** `scripts/scraping_portais_juridicos.py`

**Sites suportados:**
- Jusbrasil
- Outros portais jurídicos

**Método:** Playwright para sites JavaScript

---

## 🛠️ Como Funciona a Extração

### **1. Método Playwright (Scraping)**

**Arquivo:** `scripts/scraping_tjmg_multiplas_fontes.py`

**Fluxo:**
```
1. Inicia browser Playwright (headless)
2. Navega até URL do tribunal
3. Preenche formulário de busca (número do processo, OAB, etc)
4. Clica em "Buscar"
5. Espera carregamento da página
6. Extrai dados do HTML (tabelas, divs, etc)
7. Formata dados estruturados
8. Salva no banco de dados
```

**Código exemplo:**
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Navegar
    page.goto('https://eproc-consulta-publica-1g.tjmg.jus.br/...')
    
    # Preencher formulário
    page.fill('#numero_processo', '0000123-45.2024.8.13.0024')
    page.click('#botao_buscar')
    
    # Extrair dados
    dados = page.query_selector_all('.processo-item')
```

---

### **2. Método API (DataJud CNJ)**

**Arquivo:** `scripts/coleta_processos/coletor_datajud_cnj.py`

**Fluxo:**
```
1. Faz requisição HTTP GET para API DataJud
2. Passa parâmetros (número processo, tribunal, etc)
3. Recebe JSON com dados do processo
4. Valida e formata resposta
5. Salva no banco de dados Django
```

**Código exemplo:**
```python
import requests

def coletar_processo_cnj(numero_processo: str):
    url = "https://api-publica.datajud.cnj.jus.br/api/v1/processos"
    params = {'numero': numero_processo}
    
    response = requests.get(url, params=params)
    dados = response.json()
    
    return dados
```

---

### **3. Método Firecrawl (MCP)**

**Arquivo:** Vários scripts usam Firecrawl via MCP

**Fluxo:**
```
1. Chama função MCP Firecrawl
2. Firecrawl acessa a página (mesmo com JS)
3. Extrai conteúdo estruturado
4. Retorna dados em markdown/JSON
5. Processa e salva no banco
```

**Código exemplo:**
```python
# Via MCP Firecrawl (no Cursor/AI)
resultado = mcp_firecrawl_firecrawl_scrape(
    url="https://eproc.tjmg.jus.br/...",
    formats=["markdown"]
)
```

---

## 📍 Onde Cada Método é Usado

### **TJMG (Tribunal de Justiça de MG)**

**Scripts:**
- `scraping_tjmg_multiplas_fontes.py` - Playwright
- `coletor_datajud_uberlandia_penal.py` - API CNJ

**Estratégias:**
1. Tenta API DataJud (rápido, grátis)
2. Se falhar, tenta scraping Playwright
3. Tenta múltiplas fontes (eproc, PJe)

---

### **Outros Tribunais**

**TJSP:** Configurado mas não totalmente implementado

**TRF1:** URLs mapeadas, código pendente

**Localização:** `scripts/scraping_tjmg_multiplas_fontes.py` (linha 70+)

---

## ⚙️ Configurações Importantes

### **Playwright**

**Instalação:**
```bash
pip install playwright
playwright install chromium
```

**Configurações no código:**
```python
# scripts/captacao_playwright_robusto.py
browser = await playwright.chromium.launch(
    headless=True,  # Sem interface gráfica
    args=[
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-gpu'
    ]
)
```

---

### **API DataJud CNJ**

**Não requer configuração especial** - é pública!

**Limites:**
- Rate limiting (não documentado, mas respeitar)
- Alguns processos podem não estar disponíveis

---

### **API Escavador**

**Arquivo de configuração:** `scripts/coleta_processos/CONFIG_ESCAVADOR_V2.md`

**Variáveis necessárias:**
```python
ESCAVADOR_API_KEY = "seu_token"
ESCAVADOR_API_URL = "https://api.escavador.com/v1/"
```

**Custo:** R$ 0,05 por processo consultado

---

## 🔄 Fluxo Completo de Coleta

### **Coleta Automática Diária**

**Script:** `scripts/coleta_processos/coleta_automatica_diaria.py`

**Execução:**
- **Cron:** Todos os dias às 2:00 AM
- **Quantidade:** 50 processos/dia
- **Rotação:** 6 áreas penais diferentes

**Fluxo:**
```
1. Seleciona área do dia (júri, sexual, etc)
2. Tenta API DataJud primeiro
3. Se falhar, tenta Escavador
4. Se falhar, tenta scraping Playwright
5. Salva no RAG (ChromaDB)
6. Atualiza banco Django
7. Gera log e relatório
```

---

### **Coleta Manual**

**Scripts disponíveis:**
- `coleta_piloto_imediato.py` - Coleta rápida
- `coletar_processos_reais_tjmg.py` - TJMG específico
- `scraping_tjmg_multiplas_fontes.py` - Multi-fonte

---

## 📊 Dados Coletados

### **O que é extraído:**

1. **Dados do Processo:**
   - Número CNJ
   - Vara/Turma
   - Comarca
   - Data de distribuição
   - Status atual

2. **Partes:**
   - Autor/Réu
   - Advogados (com OAB)
   - Ministério Público

3. **Movimentações:**
   - Histórico de decisões
   - Sentenças
   - Prazos

4. **Magistrado/Promotor:**
   - Nome
   - Estatísticas
   - Histórico

---

## 🗄️ Onde os Dados São Armazenados

### **1. Banco SQLite Django**

**Localização:** `/home/clenio/Documentos/Meusagentes/kermartin/db.sqlite3`

**Tabelas principais:**
- `notifications_processo` - Processos coletados
- `tribunals_consultaprocesso` - Histórico de consultas
- `ai_engine_ragknowledgebase` - Base RAG

---

### **2. Base RAG (ChromaDB)**

**Localização:** `/home/clenio/Documentos/Meusagentes/kermartin/scripts/coleta_processos/chroma_db/`

**Formato:** ChromaDB (vetorização para busca semântica)

**Uso:** Busca inteligente por conteúdo, não só por número

---

### **3. Arquivos JSON**

**Localização:** `/home/clenio/Documentos/Meusagentes/kermartin/knowledge_base/`

**Estrutura:**
```
knowledge_base/
├── magistrados/*.json
├── promotores/*.json
└── processos/ (se existir)
```

---

## 🔍 Scripts Específicos por Função

### **Busca por OAB (Advogados)**

**Script:** `scripts/buscar_processos_por_oabs_leads.py`

**Método:** 
- Usa `scraping_tjmg_multiplas_fontes.py`
- Busca no eproc por número OAB
- Playwright para preencher formulário

---

### **Coleta de Diários Oficiais**

**Script:** `scripts/coleta_processos/coletor_diarios_playwright.py`

**Método:**
- Acessa diários oficiais via Playwright
- Extrai links de processos publicados
- Coleta dados de cada processo

---

### **Enriquecimento de Processos**

**Scripts:**
- `enriquecer_homicidios_uberlandia.py`
- `enriquecer_cnjs_uberlandia_penal.py`

**O que faz:**
- Pega processos já coletados
- Busca mais informações
- Atualiza dados existentes

---

## 🚀 Como Adicionar Novo Tribunal

### **1. Adicionar URL**

**Arquivo:** `scripts/scraping_tjmg_multiplas_fontes.py`

```python
self.urls = {
    'novo_tribunal': 'https://novo-tribunal.jus.br/consulta',
    # ... outros
}
```

---

### **2. Criar Método de Extração**

```python
def buscar_novo_tribunal(self, numero_processo: str) -> List[Dict]:
    """Busca no novo tribunal"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navegar
        page.goto(self.urls['novo_tribunal'])
        
        # Preencher e buscar
        # ...
        
        # Extrair dados
        # ...
        
        return processos
```

---

### **3. Adicionar ao Fluxo Principal**

**Arquivo:** `scripts/scraping_tjmg_multiplas_fontes.py` (método `buscar_todas_fontes`)

```python
# Estratégia 3: Novo Tribunal
try:
    processos = self.buscar_novo_tribunal()
    if processos:
        self.resultados.extend(processos)
        logger.info(f"✅ Novo Tribunal: {len(processos)} processos")
except Exception as e:
    logger.warning(f"❌ Novo Tribunal falhou: {e}")
```

---

## 📝 Resumo

### **Métodos de Extração:**
1. ✅ **Playwright** - Scraping de sites (TJMG, TJSP)
2. ✅ **API DataJud CNJ** - Oficial, grátis
3. ✅ **API Escavador** - Pago, R$ 0,05/processo
4. ✅ **Firecrawl MCP** - Para sites complexos

### **Onde está configurado:**
- `/kermartin/scripts/scraping_tjmg_multiplas_fontes.py` - Multi-fonte
- `/kermartin/scripts/coleta_processos/` - Coletores especializados
- URLs e endpoints nos próprios scripts

### **Execução:**
- **Automática:** Cron às 2:00 AM (50 processos/dia)
- **Manual:** Scripts específicos quando necessário

---

**Última atualização:** Outubro 2025

