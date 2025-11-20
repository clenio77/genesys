"""
Seletores CSS para o formulário eproc TJMG
Mapeado usando Firecrawl MCP em Outubro 2025

URL: https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica
"""

# ============================================================================
# DICIONÁRIO DE SELETORES - PRONTO PARA COPIAR
# ============================================================================

SELECTORES_EPROC = {
    # ========== CAMPOS DE BUSCA ==========
    'numero_processo': '#txtNumProcesso',
    'chave_processo': '#txtNumChave',
    'chave_documento': '#txtNumChaveDocumento',
    'nome_parte': '#txtStrParte',
    'oab': '#txtStrOAB',
    'cpf_cnpj': '#txtCpfCnpj',
    
    # ========== CHECKBOXES E RADIOS ==========
    'pesquisa_fonetica': '#chkFonetica',
    'pessoa_fisica': '#rdoPessoaFisica',
    'pessoa_juridica': '#rdoPessoaJuridica',
    
    # ========== BOTÕES ==========
    'botao_consultar': '#sbmNovo',
    'botao_voltar': '#btnVoltar',
    
    # ========== FORMULÁRIO ==========
    'formulario': '#frmProcessoLista',
}

# ============================================================================
# URL BASE
# ============================================================================

URL_EPROC = "https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"

# ============================================================================
# EXEMPLOS DE USO COM PLAYWRIGHT
# ============================================================================

def exemplo_buscar_por_numero():
    """
    Exemplo: Buscar processo por número
    """
    from playwright.sync_api import sync_playwright
    
    numero_processo = "0878961-59.2013.8.13.0702"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navegar
        page.goto(URL_EPROC)
        
        # Preencher número do processo
        page.fill(SELECTORES_EPROC['numero_processo'], numero_processo)
        
        # Clicar em consultar
        page.click(SELECTORES_EPROC['botao_consultar'])
        
        # Aguardar resultados
        page.wait_for_selector('.resultado, .processo', timeout=15000)
        
        # Extrair dados aqui...
        
        browser.close()


def exemplo_buscar_por_oab():
    """
    Exemplo: Buscar processos por OAB
    """
    from playwright.sync_api import sync_playwright
    
    oab = "MG12345"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(URL_EPROC)
        
        # Preencher OAB
        page.fill(SELECTORES_EPROC['oab'], oab)
        
        # Consultar
        page.click(SELECTORES_EPROC['botao_consultar'])
        
        # Aguardar resultados
        page.wait_for_selector('.resultado', timeout=15000)
        
        # Extrair lista de processos aqui...
        
        browser.close()


def exemplo_buscar_por_nome(nome: str, usar_fonetica: bool = True):
    """
    Exemplo: Buscar processos por nome da parte
    """
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(URL_EPROC)
        
        # Preencher nome
        page.fill(SELECTORES_EPROC['nome_parte'], nome)
        
        # Configurar pesquisa fonética
        if not usar_fonetica:
            page.uncheck(SELECTORES_EPROC['pesquisa_fonetica'])
        
        # Consultar
        page.click(SELECTORES_EPROC['botao_consultar'])
        
        # Aguardar resultados
        page.wait_for_selector('.resultado', timeout=15000)
        
        browser.close()


# ============================================================================
# USO DIRETO NO CÓDIGO DO KERMARTIN
# ============================================================================

# Copiar este dicionário para seu script:
"""
SELECTORES_EPROC = {
    'numero_processo': '#txtNumProcesso',
    'oab': '#txtStrOAB',
    'nome_parte': '#txtStrParte',
    'botao_consultar': '#sbmNovo',
}
"""

