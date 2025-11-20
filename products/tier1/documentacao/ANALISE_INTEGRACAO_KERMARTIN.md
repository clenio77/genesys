# 🔗 Análise de Integração com Kermartin

## 📊 Visão Geral do Kermartin

O **Kermartin** é um sistema Django completo com:

### ✅ **Recursos Já Implementados**

1. **Banco de Dados Estruturado:**
   - SQLite (Django) com modelos de processos
   - Tabelas: `ai_engine_ragknowledgebase`, `tribunals_tribunal`, `notifications_processo`
   - Base RAG com ChromaDB para buscas semânticas

2. **Coleta de Dados:**
   - ✅ **Playwright** já implementado (`captacao_playwright_robusto.py`)
   - ✅ **Scrapy** para crawling de tribunais
   - ✅ **Firecrawl** para extração web
   - ✅ **API DataJud** (CNJ) integrada
   - ✅ Scripts de coleta do TJMG e outros tribunais

3. **Base de Conhecimento:**
   - JSON estruturado com processos
   - Perfis de magistrados, promotores, jurados
   - Jurisprudência por tema
   - Dados coletados do Triângulo Mineiro (MG)

4. **Infraestrutura:**
   - Django Web App
   - API REST
   - Sistema de notificações
   - Monitoramento de processos

---

## 🎯 Oportunidades de Integração

### **1. Compartilhar Base de Dados de Processos** ✅ RECOMENDADO

**Estrutura Existente:**
- Base JSON: `knowledge_base/processos/`
- Dados coletados: Triângulo Mineiro, Uberlândia
- Formato estruturado com metadados completos

**Como Usar:**
- Genesys pode consultar os arquivos JSON diretamente
- Ou usar a API Django do Kermartin (se exposta)
- Criar serviço compartilhado de consulta

**Benefícios:**
- ✅ Dados já coletados e estruturados
- ✅ Histórico de processos reais
- ✅ Perfis de magistrados/promotores
- ✅ Economiza tempo de coleta

---

### **2. Usar Playwright do Kermartin** ✅ VIÁVEL

**Código Existente:**
```python
# scripts/captacao_playwright_robusto.py
- Já tem browser automation
- Extração de dados estruturada
- Tratamento de erros
- Logging completo
```

**Adaptação para Genesys:**
- Reutilizar classe `CaptadorRobusto`
- Adaptar para consulta de processos (não apenas captação de clientes)
- Extrair movimentações de tribunais

**Tribunais que podem ser extraídos:**
- TJMG (já tem scraping)
- Outros TJs (padrão similar)
- e-SAJ/eProc (com Playwright funciona melhor que Scrapy)

---

### **3. Compartilhar Infraestrutura de Coleta** ✅ OTIMIZAÇÃO

**O que Compartilhar:**
- Scripts de coleta (Playwright/Scrapy)
- Configurações de rate limiting
- Cache de consultas
- Logs e monitoramento

**Arquitetura Sugerida:**
```
Kermartin (coleta principal)
    ↓
Base de Dados Compartilhada
    ↓
Genesys (consulta/uso)
```

---

## 🔧 Estratégias de Extração com Playwright

### **Opção 1: Extração Direta de Tribunais** ⭐ RECOMENDADA

**Playwright é IDEAL para:**
- ✅ Sites com JavaScript (React/Vue)
- ✅ Formulários complexos
- ✅ Navegação dinâmica
- ✅ Respeitar robots.txt e rate limits

**Exemplo - Consultar Processo no TJMG:**
```python
from playwright.async_api import async_playwright

async def consultar_processo_tjmg(numero_processo: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Acessar consulta pública
        await page.goto('https://www8.tjmg.jus.br/consultas/consulta.do')
        
        # Preencher número do processo
        await page.fill('#numeroProcesso', numero_processo)
        await page.click('#btnConsultar')
        
        # Aguardar resultados
        await page.wait_for_selector('.resultado-processo')
        
        # Extrair dados
        dados = await page.evaluate("""
            () => {
                return {
                    numero: document.querySelector('.numero').innerText,
                    partes: Array.from(document.querySelectorAll('.parte')).map(p => p.innerText),
                    movimentacoes: Array.from(document.querySelectorAll('.movimentacao')).map(m => ({
                        data: m.querySelector('.data').innerText,
                        tipo: m.querySelector('.tipo').innerText,
                        descricao: m.querySelector('.descricao').innerText
                    }))
                }
            }
        """)
        
        await browser.close()
        return dados
```

---

### **Opção 2: Usar Infraestrutura Existente do Kermartin**

**Adaptar scripts existentes:**
- `scripts/coletar_processos_reais_tjmg.py` → Usar como base
- `kermartin/integrations/datajud_api.py` → API CNJ já funciona
- `kermartin/integrations/scrapy_crawler.py` → Adicionar Playwright onde Scrapy falha

---

## 📋 Plano de Integração

### **FASE 1: Acesso aos Dados do Kermartin** 🔴 PRIORIDADE

**Objetivo:** Genesys pode consultar processos já coletados

**Implementação:**
1. Criar serviço `kermartin_service.py` em Genesys
2. Ler arquivos JSON da base de conhecimento
3. Criar endpoint ou função para buscar processos por:
   - Número CNJ
   - Tribunal
   - Magistrado
   - Tipo de crime

**Arquivos a Acessar:**
```
/home/clenio/Documentos/Meusagentes/kermartin/
├── knowledge_base/
│   ├── magistrados/*.json
│   ├── promotores/*.json
│   └── processos/ (se existir)
├── data/triangulo_mineiro/
│   ├── processos/ (JSONs de processos)
│   └── relatorios/
└── db.sqlite3 (banco Django)
```

---

### **FASE 2: Extração com Playwright** 🟡 IMPORTANTE

**Objetivo:** Extrair processos diretamente dos tribunais

**Implementação:**
1. Reutilizar código Playwright do Kermartin
2. Adaptar para consulta de processos (não captação)
3. Criar scripts para tribunais principais:
   - TJMG (já tem estrutura)
   - TJSP
   - TRF (se necessário)

**Vantagens do Playwright:**
- ✅ Funciona com sites modernos (React/Vue)
- ✅ Pode lidar com CAPTCHA (com extensões)
- ✅ Melhor que Scrapy para JS pesado
- ✅ Mais estável que Selenium

---

### **FASE 3: Sincronização** 🟢 FUTURO

**Objetivo:** Compartilhar dados entre sistemas

**Opções:**
1. **API REST Compartilhada:**
   - Kermartin expõe endpoints
   - Genesys consome via HTTP

2. **Banco Compartilhado:**
   - PostgreSQL compartilhado
   - Ambos acessam mesma base

3. **Serviço Compartilhado:**
   - Módulo Python compartilhado
   - Ambos importam e usam

---

## 🗂️ Estrutura de Dados Encontrada

### **Base de Conhecimento (JSON)**

**Localização:** `knowledge_base/`

**Tipos de Dados:**
- **Magistrados:** Perfis completos, estatísticas, histórico
- **Promotores:** Perfis, casos, especializações
- **Jurados:** Dados de júris (quando aplicável)
- **Jurisprudência:** Por tema (homicídio, danos morais, etc.)

**Exemplo de Estrutura:**
```json
{
  "magistrado_id": "MAG_TRI_UBE_1ª",
  "comarca": "Uberlândia",
  "vara": "1ª Vara Criminal",
  "nome_publico": "...",
  "estatisticas": {
    "processos_julgados": 150,
    "taxa_condenacao": 0.75,
    "pena_media_homicidio": "12 anos"
  }
}
```

### **Banco SQLite Django**

**Tabelas Relevantes:**
- `ai_engine_ragknowledgebase` - Base RAG
- `tribunals_tribunal` - Tribunais cadastrados
- `tribunals_consultaprocesso` - Histórico de consultas
- `notifications_processo` - Processos monitorados
- `monitoring_processo_monitorado` - Monitoramento ativo

---

## 🚀 Recomendações Imediatas

### **1. Criar Serviço de Acesso ao Kermartin**

```python
# products/tier1/bot-telegram/src/services/kermartin_service.py

class KermartinService:
    """Serviço para acessar dados do Kermartin"""
    
    BASE_PATH = "/home/clenio/Documentos/Meusagentes/kermartin"
    
    def buscar_processo_kermartin(self, numero_cnj: str):
        """Busca processo na base do Kermartin"""
        # Ler JSONs ou consultar SQLite
        pass
    
    def buscar_magistrado(self, nome: str):
        """Busca perfil de magistrado"""
        # Ler knowledge_base/magistrados/
        pass
```

### **2. Criar Extrator Playwright para Tribunais**

```python
# products/tier1/bot-telegram/src/services/playwright_extractor.py

from playwright.async_api import async_playwright

class TribunalExtractor:
    """Extrai processos diretamente dos tribunais"""
    
    async def extrair_tjmg(self, numero_processo: str):
        """Extrai processo do TJMG"""
        # Usar código similar ao Kermartin
        pass
```

---

## 📊 Comparação de Métodos

| Método | Kermartin | Genesys | Recomendação |
|--------|-----------|---------|--------------|
| **API CNJ** | ✅ Implementado | ✅ Implementado | Usar ambos |
| **Playwright** | ✅ Para captação | ❌ Não tem | **Criar no Genesys** |
| **Scrapy** | ✅ Para tribunais | ❌ Não tem | Reutilizar se necessário |
| **Firecrawl** | ✅ Via MCP | ✅ Via MCP | Compatível |
| **Base JSON** | ✅ Grande volume | ❌ Não tem | **Acessar Kermartin** |

---

## 🎯 Próximos Passos

### **Prioridade 1 (Agora):**
1. ✅ Criar serviço para acessar dados JSON do Kermartin
2. ✅ Integrar busca de processos na base existente
3. ✅ Usar perfis de magistrados/promotores

### **Prioridade 2 (Próximo):**
4. ✅ Criar extrator Playwright para tribunais
5. ✅ Implementar consulta direta no TJMG
6. ✅ Sincronizar dados coletados

### **Prioridade 3 (Futuro):**
7. ✅ API REST compartilhada
8. ✅ Banco de dados unificado
9. ✅ Sistema de cache compartilhado

---

## 💡 Exemplo de Uso

### **Buscar Processo no Genesys:**

```python
# Bot recebe: /processo 0001234-56.2024.8.26.0100

# 1. Tenta API CNJ (já implementado)
dados = cnj_service.consultar_processo(numero)

# 2. Se não encontrar, busca no Kermartin
if not dados:
    dados = kermartin_service.buscar_processo_kermartin(numero)

# 3. Se ainda não encontrar, extrai com Playwright
if not dados:
    dados = playwright_extractor.extrair_tjmg(numero)

# 4. Retorna resultado ao usuário
bot.reply(formatar_resposta(dados))
```

---

**Status:** ✅ **ANÁLISE COMPLETA - PRONTO PARA IMPLEMENTAÇÃO**

O Kermartin tem uma base rica de dados e infraestrutura que podemos aproveitar!

