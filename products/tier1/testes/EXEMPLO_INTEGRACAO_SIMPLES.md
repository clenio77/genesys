# 🚀 Exemplo Prático - Integração MCP no Kermartin (Simples)

## 📝 Passo a Passo Rápido

### **Opção 1: Usar Firecrawl para Mapear (Mais Fácil)**

```python
# kermartin/scripts/mapear_eproc_com_firecrawl.py

"""
Script simples para mapear estrutura do eproc usando Firecrawl MCP
"""

# NOTA: Este script deve ser executado NO CURSOR
# As funções MCP (Firecrawl) só funcionam dentro do Cursor

def mapear_eproc():
    """
    Usa Firecrawl para mapear estrutura do formulário eproc
    
    Execute no Cursor pedindo:
    "Use Firecrawl para mapear o formulário do eproc TJMG"
    """
    
    url = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
    
    # No Cursor, pedir:
    # "Faça scraping desta URL e me mostre os campos do formulário"
    
    # Resultado esperado:
    campos_encontrados = {
        'txtNumProcesso': 'Número do processo',
        'txtStrOAB': 'OAB',
        'txtStrParte': 'Nome da parte',
        'sbmNovo': 'Botão Consultar'
    }
    
    return campos_encontrados
```

**Como usar:**
1. No Cursor, pedir: "Use Firecrawl para mapear o formulário do eproc TJMG"
2. Copiar campos identificados
3. Usar no código Playwright existente

---

### **Opção 2: Adicionar Flag para Teste com MCP**

```python
# kermartin/scripts/scraping_tjmg_multiplas_fontes.py

# Adicionar no início da classe:

class ScraperTJMGMultiFonte:
    def __init__(self, config: ConfigBusca = None, usar_mcp: bool = False):
        self.config = config or ConfigBusca()
        self.resultados = []
        self.usar_mcp = usar_mcp  # Flag para usar MCP
        
        # URLs dos sistemas
        self.urls = {
            'eproc': 'https://eproc-consulta-publica-1g.tjmg.jus.br/...',
            # ... outros
        }
    
    def buscar_eproc(self, nome_parte: str = None) -> List[Dict]:
        """Busca processos no eproc"""
        
        # Se flag MCP ativada E estiver no Cursor
        if self.usar_mcp:
            logger.info("🧪 Modo MCP ativado - use Cursor para testar")
            # Retornar instruções para usar no Cursor
            return []
        
        # Usar Playwright padrão (produção)
        from playwright.sync_api import sync_playwright
        # ... código existente ...
```

**Uso:**
```python
# Para testar com MCP (no Cursor):
scraper = ScraperTJMGMultiFonte(usar_mcp=True)

# Para produção (normal):
scraper = ScraperTJMGMultiFonte(usar_mcp=False)
```

---

### **Opção 3: Script Separado para Mapeamento**

```python
# kermartin/scripts/mapear_sites_tribunais.py

"""
Script para mapear sites de tribunais usando Firecrawl
Executar no Cursor pedindo para mapear cada URL
"""

SITES_PARA_MAPEAR = {
    'TJMG_eproc': 'https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica',
    'TJMG_pje': 'https://pje.tjmg.jus.br/pje/ConsultaPublica/listView.seam',
    # Adicionar outros...
}

def gerar_relatorio_mapeamento():
    """
    Gera relatório com estrutura de cada site
    
    Para executar:
    1. No Cursor, pedir para mapear cada URL com Firecrawl
    2. Extrair IDs dos campos
    3. Gerar este relatório automaticamente
    """
    
    relatorio = {}
    
    for nome, url in SITES_PARA_MAPEAR.items():
        # No Cursor:
        # "Use Firecrawl para mapear {url} e me dê os IDs dos campos"
        
        relatorio[nome] = {
            'url': url,
            'campos': [],  # Preenchido pelo Cursor
            'botoes': [],
            'formulario': {}
        }
    
    return relatorio

# Salvar em arquivo JSON
import json
relatorio = gerar_relatorio_mapeamento()
with open('mapeamento_tribunais.json', 'w') as f:
    json.dump(relatorio, f, indent=2)
```

---

## 🎯 Abordagem Recomendada (Mais Prática)

### **Estratégia: Usar MCP no Cursor, Código no Kermartin**

**Passo 1: Mapear com Firecrawl (no Cursor)**
```
No Cursor, pedir:
"Use Firecrawl para mapear o formulário do eproc TJMG 
e me mostre todos os IDs dos campos e botões"
```

**Passo 2: Copiar IDs para código Playwright**
```python
# kermartin/scripts/scraping_tjmg_multiplas_fontes.py

# Usar os IDs mapeados pelo Firecrawl:
SELECTORES_EPROC = {
    'numero_processo': '#txtNumProcesso',  # ← do Firecrawl
    'oab': '#txtStrOAB',                   # ← do Firecrawl
    'botao_buscar': '#sbmNovo',            # ← do Firecrawl
}

# No código Playwright existente, usar esses seletores:
page.fill(SELECTORES_EPROC['numero_processo'], numero)
page.click(SELECTORES_EPROC['botao_buscar'])
```

**Passo 3: Testar com Playwright**
```bash
python scraping_tjmg_multiplas_fontes.py
```

---

## 💡 Fluxo Completo Recomendado

```
┌─────────────────────────────────────────┐
│  1. MAPEAR (no Cursor com Firecrawl)   │
│     ↓                                    │
│     Identificar IDs dos campos          │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  2. CODIFICAR (no Kermartin)           │
│     ↓                                    │
│     Usar IDs no código Playwright       │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  3. TESTAR (Playwright)                │
│     ↓                                    │
│     Validar extração funciona           │
└─────────────────────────────────────────┘
            ↓
┌─────────────────────────────────────────┐
│  4. PRODUÇÃO (Cron job)                │
│     ↓                                    │
│     Usar Playwright (já funciona)      │
└─────────────────────────────────────────┘
```

---

## 📋 Checklist de Integração

### **Para Cada Novo Tribunal/Site:**

- [ ] 1. Mapear estrutura com Firecrawl (no Cursor)
- [ ] 2. Identificar IDs dos campos
- [ ] 3. Adicionar seletores no código Playwright
- [ ] 4. Testar extração
- [ ] 5. Adicionar ao cron job (produção)

---

## 🎯 Resumo Simples

**Integração MCP no Kermartin =**

1. **Mapear** sites com Firecrawl (no Cursor) ✅
2. **Copiar** IDs para código Playwright ✅
3. **Manter** Playwright para produção ✅

**NÃO precisa:**
- Criar classes complexas
- Modificar muito código existente
- Substituir Playwright por MCP

**Apenas usar MCP para:**
- Descobrir estrutura de sites novos
- Validar seletores antes de codificar
- Debugging visual (quando disponível)

---

**Abordagem mais prática e menos invasiva!** ✅

