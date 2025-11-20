# 🔗 Guia de Integração - Funções MCP no Kermartin

## 📋 Visão Geral

Este guia mostra como integrar as funções de navegador MCP (Cursor Browser e Firecrawl) nos scripts de coleta do Kermartin.

**Objetivo:** Complementar ou substituir Playwright para testes, debugging e mapeamento de sites.

---

## 🎯 Estratégia de Integração

### **Abordagem Híbrida:**

```
┌─────────────────────────────────────────┐
│  MÉTODO DE EXTRAÇÃO                     │
├─────────────────────────────────────────┤
│                                         │
│  1. Browser MCP (Cursor)               │
│     ↓ Para testes/debug visuais        │
│                                         │
│  2. Firecrawl MCP                      │
│     ↓ Para mapear estrutura            │
│                                         │
│  3. Playwright Standalone              │
│     ↓ Para produção (cron jobs)        │
│                                         │
└─────────────────────────────────────────┘
```

**Regra de Ouro:**
- **Desenvolvimento/Teste:** Browser MCP ou Firecrawl
- **Produção:** Playwright (já configurado)

---

## 📂 Onde Integrar

### **Scripts Principais do Kermartin:**

```
kermartin/scripts/
├── scraping_tjmg_multiplas_fontes.py      ← Integrar aqui
├── captacao_playwright_robusto.py        ← Integrar aqui
└── coleta_processos/
    ├── coletor_diarios_playwright.py      ← Integrar aqui
    └── scraping_tjmg_multiplas_fontes.py ← Integrar aqui
```

---

## 🔧 Integração 1: Browser MCP (Cursor)

### **Uso: Testes e Debugging Visual**

#### **1. Criar Classe Wrapper:**

```python
# kermartin/scripts/utils/browser_mcp_helper.py

"""
Helper para usar Browser MCP do Cursor em testes
"""
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class BrowserMCPHelper:
    """Wrapper para funções MCP de navegador"""
    
    def __init__(self):
        self.mcp_available = self._check_mcp_available()
    
    def _check_mcp_available(self) -> bool:
        """Verifica se MCP está disponível"""
        try:
            # Tentar importar/invocar MCP
            # Isso depende de como o MCP está configurado
            return False  # Por padrão, desabilitado
        except:
            return False
    
    def navigate(self, url: str) -> bool:
        """Navega para URL usando MCP"""
        if not self.mcp_available:
            logger.warning("Browser MCP não disponível")
            return False
        
        try:
            # Chamar mcp_cursor-ide-browser_browser_navigate
            # Implementação depende de como MCP está configurado
            logger.info(f"🌐 Navegando para: {url}")
            return True
        except Exception as e:
            logger.error(f"Erro ao navegar: {e}")
            return False
    
    def snapshot(self) -> Optional[Dict]:
        """Captura snapshot da página"""
        if not self.mcp_available:
            return None
        
        try:
            # Chamar mcp_cursor-ide-browser_browser_snapshot
            logger.debug("📸 Capturando snapshot")
            return {}
        except Exception as e:
            logger.error(f"Erro ao capturar snapshot: {e}")
            return None
    
    def fill_form(self, field_id: str, value: str) -> bool:
        """Preenche campo do formulário"""
        # Implementação similar
        pass
    
    def click(self, element_id: str) -> bool:
        """Clica em elemento"""
        # Implementação similar
        pass
```

---

#### **2. Modificar Script de Scraping:**

```python
# kermartin/scripts/scraping_tjmg_multiplas_fontes.py

from utils.browser_mcp_helper import BrowserMCPHelper

class ScraperTJMGMultiFonte:
    def __init__(self, config: ConfigBusca = None):
        self.config = config or ConfigBusca()
        self.resultados = []
        
        # Adicionar helper MCP
        self.mcp_helper = BrowserMCPHelper()
        self.use_mcp = self.mcp_helper.mcp_available  # Auto-detecta
        
        logger.info(f"🔧 Browser MCP: {'✅ Disponível' if self.use_mcp else '❌ Não disponível'}")
    
    def buscar_eproc_com_mcp(self, numero_processo: str) -> List[Dict]:
        """
        Busca no eproc usando Browser MCP (para testes) ou Playwright (produção)
        """
        if self.use_mcp:
            # Usar MCP para teste visual
            return self._buscar_eproc_mcp(numero_processo)
        else:
            # Usar Playwright padrão
            return self.buscar_eproc()
    
    def _buscar_eproc_mcp(self, numero_processo: str) -> List[Dict]:
        """Busca usando Browser MCP (teste/debug)"""
        logger.info("🧪 Usando Browser MCP para teste...")
        
        url = self.urls['eproc']
        
        # 1. Navegar
        if not self.mcp_helper.navigate(url):
            logger.warning("Falhou navegação MCP, usando Playwright")
            return self.buscar_eproc()
        
        # 2. Capturar snapshot para ver estrutura
        snapshot = self.mcp_helper.snapshot()
        if snapshot:
            logger.debug("✅ Página carregada")
        
        # 3. Preencher formulário
        self.mcp_helper.fill_form('txtNumProcesso', numero_processo)
        
        # 4. Clicar em buscar
        self.mcp_helper.click('sbmNovo')
        
        # 5. Aguardar resultados
        # ... aguardar e extrair
        
        # NOTA: Por enquanto, retornar vazio (MCP precisa estar ativo)
        # Em produção, usar Playwright
        logger.warning("MCP retornou vazio, usando Playwright como fallback")
        return self.buscar_eproc()
```

---

## 🔧 Integração 2: Firecrawl MCP

### **Uso: Mapear Estrutura de Sites**

#### **1. Criar Helper Firecrawl:**

```python
# kermartin/scripts/utils/firecrawl_helper.py

"""
Helper para usar Firecrawl MCP no Kermartin
"""
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class FirecrawlHelper:
    """Wrapper para Firecrawl MCP"""
    
    def __init__(self):
        self.mcp_available = self._check_firecrawl_available()
    
    def _check_firecrawl_available(self) -> bool:
        """Verifica se Firecrawl MCP está disponível"""
        # Verificar se MCP Firecrawl está configurado
        # Por enquanto, assumir disponível (já testamos)
        return True
    
    def mapear_formulario(self, url: str) -> Optional[Dict]:
        """
        Mapeia estrutura de formulário usando Firecrawl
        
        Retorna:
        - IDs dos campos
        - Tipos de input
        - Botões e ações
        """
        logger.info(f"🗺️ Mapeando formulário: {url}")
        
        try:
            # Chamar Firecrawl para extrair HTML
            # result = mcp_firecrawl_firecrawl_scrape(url, formats=['html'])
            
            # Parse HTML para extrair estrutura
            estrutura = {
                'campos': [],
                'botoes': [],
                'formulario': {}
            }
            
            # Exemplo de extração (pseudo-código):
            # campos = parse_html_extract_fields(result['html'])
            # estrutura['campos'] = campos
            
            logger.info("✅ Formulário mapeado")
            return estrutura
            
        except Exception as e:
            logger.error(f"Erro ao mapear: {e}")
            return None
    
    def validar_seletores(self, url: str, seletores: List[str]) -> Dict[str, bool]:
        """
        Valida se seletores CSS funcionam na página
        
        Útil antes de codificar scraping
        """
        logger.info(f"🔍 Validando {len(seletores)} seletores...")
        
        # Extrair HTML com Firecrawl
        # html = mcp_firecrawl_firecrawl_scrape(url)['html']
        
        # Validar cada seletor
        resultados = {}
        for seletor in seletores:
            # resultado = validate_selector(html, seletor)
            resultados[seletor] = True  # Placeholder
        
        return resultados
```

---

#### **2. Usar no Script de Coleta:**

```python
# kermartin/scripts/scraping_tjmg_multiplas_fontes.py

from utils.firecrawl_helper import FirecrawlHelper

class ScraperTJMGMultiFonte:
    def __init__(self, config: ConfigBusca = None):
        # ... código existente ...
        
        # Adicionar Firecrawl helper
        self.firecrawl = FirecrawlHelper()
    
    def mapear_estrutura_eproc(self) -> Dict:
        """
        Mapeia estrutura do formulário eproc antes de codificar scraping
        """
        logger.info("🗺️ Mapeando estrutura do eproc...")
        
        url = self.urls['eproc']
        estrutura = self.firecrawl.mapear_formulario(url)
        
        if estrutura:
            logger.info("✅ Estrutura mapeada:")
            logger.info(f"   Campos: {len(estrutura.get('campos', []))}")
            logger.info(f"   Botões: {len(estrutura.get('botoes', []))}")
        
        return estrutura or {}
    
    def validar_seletores_antes_de_usar(self):
        """
        Valida seletores CSS antes de usar em produção
        """
        url = self.urls['eproc']
        
        seletores_para_testar = [
            '#txtNumProcesso',
            '#txtStrOAB',
            '#sbmNovo',
            '.resultado-processo',
            '.dados-processo'
        ]
        
        resultados = self.firecrawl.validar_seletores(url, seletores_para_testar)
        
        logger.info("📊 Resultados da validação:")
        for seletor, valido in resultados.items():
            status = "✅" if valido else "❌"
            logger.info(f"   {status} {seletor}")
```

---

## 🔧 Integração 3: Modo Híbrido (Recomendado)

### **Classe que Escolhe Automaticamente:**

```python
# kermartin/scripts/utils/extrator_hibrido.py

"""
Extrator híbrido que usa MCP quando disponível, Playwright quando não
"""
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class ExtratorHibrido:
    """
    Escolhe automaticamente o melhor método de extração:
    - Browser MCP (se disponível e em modo debug)
    - Firecrawl (para mapeamento)
    - Playwright (produção)
    """
    
    def __init__(self, modo: str = "auto"):
        """
        Args:
            modo: "auto", "mcp", "playwright", "firecrawl"
        """
        self.modo = modo
        self.browser_mcp = BrowserMCPHelper()
        self.firecrawl = FirecrawlHelper()
        
        # Detectar melhor método
        if modo == "auto":
            if self.browser_mcp.mcp_available:
                self.metodo_principal = "mcp"
            else:
                self.metodo_principal = "playwright"
        else:
            self.metodo_principal = modo
        
        logger.info(f"🔧 Modo de extração: {self.metodo_principal}")
    
    def extrair_processo(self, numero_processo: str, tribunal: str = "TJMG") -> Optional[Dict]:
        """
        Extrai processo usando melhor método disponível
        """
        if self.metodo_principal == "mcp" and self.browser_mcp.mcp_available:
            logger.info("🧪 Usando Browser MCP...")
            return self._extrair_com_mcp(numero_processo, tribunal)
        
        elif self.metodo_principal == "firecrawl":
            logger.info("🗺️ Usando Firecrawl...")
            return self._mapear_com_firecrawl(numero_processo, tribunal)
        
        else:
            logger.info("🏭 Usando Playwright...")
            return self._extrair_com_playwright(numero_processo, tribunal)
    
    def _extrair_com_mcp(self, numero: str, tribunal: str) -> Optional[Dict]:
        """Extrai usando Browser MCP"""
        # Implementação com MCP
        pass
    
    def _mapear_com_firecrawl(self, numero: str, tribunal: str) -> Optional[Dict]:
        """Mapeia usando Firecrawl"""
        # Implementação com Firecrawl
        pass
    
    def _extrair_com_playwright(self, numero: str, tribunal: str) -> Optional[Dict]:
        """Extrai usando Playwright (fallback)"""
        # Código Playwright existente
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # ... lógica existente ...
            
            browser.close()
```

---

## 📝 Exemplo Prático Completo

### **Script Modificado: `scraping_tjmg_test_mcp.py`**

```python
#!/usr/bin/env python3
"""
Teste de integração MCP no scraper TJMG
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.extrator_hibrido import ExtratorHibrido
from utils.firecrawl_helper import FirecrawlHelper

def teste_mapeamento_eproc():
    """Teste 1: Mapear estrutura do eproc"""
    print("🧪 Teste 1: Mapear estrutura do eproc")
    
    firecrawl = FirecrawlHelper()
    url = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
    
    estrutura = firecrawl.mapear_formulario(url)
    
    if estrutura:
        print("✅ Estrutura mapeada:")
        print(f"   Campos encontrados: {len(estrutura.get('campos', []))}")
    else:
        print("❌ Falha ao mapear")


def teste_extracao_hibrida():
    """Teste 2: Extrair usando método híbrido"""
    print("\n🧪 Teste 2: Extração híbrida")
    
    extrator = ExtratorHibrido(modo="auto")
    
    numero_teste = "0878961-59.2013.8.13.0702"
    resultado = extrator.extrair_processo(numero_teste, "TJMG")
    
    if resultado:
        print("✅ Processo extraído:")
        print(f"   Número: {resultado.get('numero')}")
        print(f"   Vara: {resultado.get('vara')}")
    else:
        print("❌ Falha ao extrair")


if __name__ == "__main__":
    print("=" * 60)
    print("🔗 TESTE DE INTEGRAÇÃO MCP NO KERMARTIN")
    print("=" * 60)
    
    teste_mapeamento_eproc()
    teste_extracao_hibrida()
    
    print("\n" + "=" * 60)
    print("✅ Testes concluídos")
```

---

## 🚀 Passos para Implementar

### **1. Criar Estrutura de Helpers:**

```bash
cd /home/clenio/Documentos/Meusagentes/kermartin/scripts

# Criar pasta para helpers
mkdir -p utils

# Criar arquivos
touch utils/__init__.py
touch utils/browser_mcp_helper.py
touch utils/firecrawl_helper.py
touch utils/extrator_hibrido.py
```

### **2. Modificar Scripts Existentes:**

```bash
# Backup primeiro
cp scraping_tjmg_multiplas_fontes.py scraping_tjmg_multiplas_fontes.py.bak

# Modificar para usar helpers
# (código nos exemplos acima)
```

### **3. Testar Integração:**

```bash
# Executar teste
python scraping_tjmg_test_mcp.py
```

---

## ⚠️ Importante

### **Compatibilidade:**

- **Manter Playwright** como método principal em produção
- **MCP apenas para:** testes, debug, mapeamento
- **Fallback automático:** Se MCP falhar, usa Playwright

### **Modo de Uso:**

```python
# Desenvolvimento (com MCP ativo)
extrator = ExtratorHibrido(modo="mcp")

# Produção (sempre Playwright)
extrator = ExtratorHibrido(modo="playwright")

# Auto-detecta
extrator = ExtratorHibrido(modo="auto")
```

---

## 📊 Resumo

| Método | Quando Usar | Vantagem |
|--------|-------------|----------|
| **Browser MCP** | Testes visuais, debug | Vê o que está acontecendo |
| **Firecrawl** | Mapear estrutura | Rápido, fácil |
| **Playwright** | Produção, cron jobs | Confiável, independente |

**Estratégia:** Use MCP para desenvolver/testar, Playwright para produção!

---

**Última atualização:** Outubro 2025

