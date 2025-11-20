# 🗺️ Mapeamento Completo - eproc TJMG

**Data:** Outubro 2025  
**Fonte:** Firecrawl MCP  
**URL:** `https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica`

---

## 📋 Seletores CSS Identificados

### **✅ FORMULÁRIO PRINCIPAL**

**ID do formulário:** `frmProcessoLista`  
**Método:** POST  
**Ação:** `externo_controlador.php?acao=processo_consulta_publica`

---

## 🔍 CAMPOS DE ENTRADA

### **1. Número do Processo** ⭐ MAIS USADO
```python
# Seletor CSS
"#txtNumProcesso"

# Label
"Nº Processo:"

# Tipo
type="text"

# Máscara JavaScript
onkeypress="return infraMascara(this,event,'#######-##.####.#.##.####')"

# Maxlength
maxlength="25"

# Uso Playwright:
page.fill('#txtNumProcesso', '0878961-59.2013.8.13.0702')
```

---

### **2. Chave do Processo**
```python
# Seletor CSS
"#txtNumChave"

# Label
"Chave do processo:"

# Tipo
type="text"

# Máscara
onkeypress="return infraMascara(this,event,'############')"

# Maxlength
maxlength="12"

# Uso Playwright:
page.fill('#txtNumChave', '123456789012')
```

---

### **3. Chave do Documento**
```python
# Seletor CSS
"#txtNumChaveDocumento"

# Label
"Chave Documento:"

# Tipo
type="text"

# Máscara
onkeypress="return infraMascara(this,event,'############')"

# Maxlength
maxlength="12"

# Uso Playwright:
page.fill('#txtNumChaveDocumento', '123456789012')
```

---

### **4. Nome da Parte** ⭐ USADO
```python
# Seletor CSS
"#txtStrParte"

# Label
"Nome da Parte:"

# Tipo
type="text"

# Observação
"(somente pessoa física ou jurídica)"

# Uso Playwright:
page.fill('#txtStrParte', 'João Silva')
```

---

### **5. Pesquisa Fonética** (Checkbox)
```python
# Seletor CSS
"#chkFonetica"

# Tipo
type="checkbox"

# Valor padrão
checked="checked" (ativa por padrão)

# Hidden field (backup)
"#hdnFonetica" (value="N")

# Uso Playwright:
# Para desmarcar (se necessário):
page.uncheck('#chkFonetica')

# Para marcar:
page.check('#chkFonetica')
```

---

### **6. OAB** ⭐ MUITO USADO
```python
# Seletor CSS
"#txtStrOAB"

# Label
"OAB:"

# Tipo
type="text"

# Uso Playwright:
page.fill('#txtStrOAB', 'MG12345')
```

---

### **7. Tipo de Pessoa** (Radio Buttons)
```python
# Pessoa Física
"#rdoPessoaFisica"
value="CPF"
onclick="trocarCpfCnpj()"

# Pessoa Jurídica
"#rdoPessoaJuridica"
value="CNPJ"
onclick="trocarCpfCnpj()"

# Uso Playwright:
# Selecionar Pessoa Física:
page.check('#rdoPessoaFisica')

# Selecionar Pessoa Jurídica:
page.check('#rdoPessoaJuridica')
```

---

### **8. CPF/CNPJ**
```python
# Seletor CSS
"#txtCpfCnpj"

# Label
"CPF:" (ou "CNPJ:" - muda dinamicamente)

# Tipo
type="text"

# Máscara
onkeypress="mascaraCpfCnpj(this,event)"

# Maxlength
maxlength="14"

# Observação
"(somente números)"

# Uso Playwright:
page.fill('#txtCpfCnpj', '12345678901')
```

---

## 🔘 BOTÕES

### **1. Consultar** ⭐ PRINCIPAL
```python
# Seletor CSS
"#sbmNovo"

# Tipo
type="submit"

# Nome
name="sbmNovo"

# Valor
value="Consultar"

# Accesskey
accesskey="C"

# Classe
class="infraButton"

# Uso Playwright:
page.click('#sbmNovo')

# OU (por ser submit):
page.click('button[type="submit"]')
```

---

### **2. Voltar**
```python
# Seletor CSS
"#btnVoltar"

# Tipo
type="button"

# Valor
value="Voltar"

# Ação
onclick="location.href='externo_controlador.php?acao=principal'"

# Uso Playwright:
page.click('#btnVoltar')
```

---

## 📊 CAMPOS HIDDEN (Ocultos)

### **1. Tipo de Página**
```python
"#hdnInfraTipoPagina"
name="hdnInfraTipoPagina"
value="1"
```

### **2. Seleções**
```python
"#hdnInfraSelecoes"
name="hdnInfraSelecoes"
value="Infra"
```

### **3. Prefixo Cookie**
```python
"#hdnInfraPrefixoCookie"
value="TJMG_Eproc_"
```

### **4. URL Log Erro JavaScript**
```python
"#url_log_erro_javascript"
name="url_log_erro_javascript"
```

---

## 📝 DICIONÁRIO DE SELETORES (Pronto para Copiar)

```python
# kermartin/scripts/seletores_eproc_tjmg.py

SELECTORES_EPROC = {
    # Campos de busca
    'numero_processo': '#txtNumProcesso',
    'chave_processo': '#txtNumChave',
    'chave_documento': '#txtNumChaveDocumento',
    'nome_parte': '#txtStrParte',
    'oab': '#txtStrOAB',
    'cpf_cnpj': '#txtCpfCnpj',
    
    # Checkboxes e radios
    'pesquisa_fonetica': '#chkFonetica',
    'pessoa_fisica': '#rdoPessoaFisica',
    'pessoa_juridica': '#rdoPessoaJuridica',
    
    # Botões
    'botao_consultar': '#sbmNovo',
    'botao_voltar': '#btnVoltar',
    
    # Formulário
    'formulario': '#frmProcessoLista',
}

# Uso:
from seletores_eproc_tjmg import SELECTORES_EPROC

page.fill(SELECTORES_EPROC['numero_processo'], numero)
page.click(SELECTORES_EPROC['botao_consultar'])
```

---

## 🎯 EXEMPLOS DE USO NO PLAYWRIGHT

### **Exemplo 1: Buscar por Número do Processo**

```python
from playwright.sync_api import sync_playwright

def buscar_processo_por_numero(numero_processo: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navegar
        page.goto('https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica')
        
        # Preencher número do processo
        page.fill('#txtNumProcesso', numero_processo)
        
        # Clicar em consultar
        page.click('#sbmNovo')
        
        # Aguardar resultados
        page.wait_for_selector('.resultado, .processo', timeout=15000)
        
        # Extrair dados
        # ... código de extração ...
        
        browser.close()
```

---

### **Exemplo 2: Buscar por OAB**

```python
def buscar_processos_por_oab(oab: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto('https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica')
        
        # Preencher OAB
        page.fill('#txtStrOAB', oab)
        
        # Clicar em consultar
        page.click('#sbmNovo')
        
        # Aguardar e extrair
        page.wait_for_selector('.resultado', timeout=15000)
        
        # ... extrair lista de processos ...
        
        browser.close()
```

---

### **Exemplo 3: Buscar por Nome da Parte**

```python
def buscar_processos_por_nome(nome: str, usar_fonetica: bool = True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto('https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica')
        
        # Preencher nome
        page.fill('#txtStrParte', nome)
        
        # Configurar pesquisa fonética
        if not usar_fonetica:
            page.uncheck('#chkFonetica')
        
        # Consultar
        page.click('#sbmNovo')
        
        # Aguardar e extrair
        page.wait_for_selector('.resultado', timeout=15000)
        
        browser.close()
```

---

## 🔍 VALIDAÇÕES E MÁSCARAS

### **JavaScript Identificado:**

1. **`infraMascara()`** - Aplica máscara de formato
   - Número processo: `#######-##.####.#.##.####`
   - Chave: `############`

2. **`trocarCpfCnpj()`** - Alterna entre CPF/CNPJ
   - Chamado ao clicar nos radio buttons

3. **`mascaraCpfCnpj()`** - Máscara dinâmica CPF/CNPJ

4. **`OnSubmitForm()`** - Validação antes de submeter

---

## 📊 RESUMO VISUAL

```
FORMULÁRIO EPROC TJMG
╔══════════════════════════════════════════╗
║  🔍 CAMPOS DE BUSCA:                     ║
║  • #txtNumProcesso      (Número)         ║
║  • #txtNumChave         (Chave)          ║
║  • #txtNumChaveDocumento (Chave Doc)    ║
║  • #txtStrParte         (Nome Parte)     ║
║  • #txtStrOAB           (OAB)           ║
║  • #txtCpfCnpj          (CPF/CNPJ)      ║
║                                          ║
║  ☑ #chkFonetica        (Fonética)        ║
║  ○ #rdoPessoaFisica    (Tipo)           ║
║  ○ #rdoPessoaJuridica  (Tipo)           ║
║                                          ║
║  [Consultar] [Voltar]                    ║
║  #sbmNovo    #btnVoltar                 ║
╚══════════════════════════════════════════╝
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### **Para usar no Kermartin:**

- [ ] Copiar dicionário `SELECTORES_EPROC` para script
- [ ] Substituir seletores antigos pelos novos
- [ ] Testar busca por número do processo
- [ ] Testar busca por OAB
- [ ] Testar busca por nome da parte
- [ ] Validar extração de resultados
- [ ] Adicionar ao cron job (produção)

---

## 📁 ONDE APLICAR NO KERMARTIN

### **Arquivo:** `kermartin/scripts/scraping_tjmg_multiplas_fontes.py`

**Substituir:**
```python
# Seletores antigos (se houver)
page.fill('input[name="numero"]', numero)

# Por:
page.fill('#txtNumProcesso', numero)
page.click('#sbmNovo')
```

---

## 🎉 RESULTADO

**✅ Mapeamento completo do formulário eproc TJMG**  
**✅ Todos os IDs identificados**  
**✅ Seletores prontos para usar no Playwright**  
**✅ Exemplos de código prontos**  

**Próximo passo:** Copiar seletores para o código do Kermartin! 🚀

---

**Última atualização:** Outubro 2025  
**Método:** Firecrawl MCP

