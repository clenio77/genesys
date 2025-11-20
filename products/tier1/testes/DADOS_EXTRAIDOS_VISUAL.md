# 👁️ Dados Extraídos - Visualização Detalhada

## 📄 O Que o Firecrawl Conseguiu Extrair da Página

---

## 🔍 1. ESTRUTURA DO FORMULÁRIO

### **Campos de Busca Disponíveis:**

```
┌─────────────────────────────────────────────────────────┐
│  CONSULTA PROCESSUAL - BUSCA DE PROCESSO               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📋 Nº Processo: [____________________]                │
│      Formato: #######-##.####.#.##.####                │
│      Exemplo: 0878961-59.2013.8.13.0702               │
│                                                         │
│  🔑 Chave do processo: [____________]                  │
│      OU                                                 │
│  📄 Chave Documento: [____________]                    │
│                                                         │
│  👤 Nome da Parte: [____________________]              │
│      (somente pessoa física ou jurídica)               │
│      ☑ Pesquisa fonética                               │
│                                                         │
│  ⚖️ OAB: [____________________]                        │
│                                                         │
│  🆔 Tipo: ○ Pessoa Física  ○ Pessoa Jurídica         │
│      CPF/CNPJ: [____________________]                  │
│      (somente números)                                  │
│                                                         │
│  [Consultar]  [Voltar]                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 2. DETALHES TÉCNICOS DOS CAMPOS

### **Campo 1: Número do Processo**
```html
<input type="text" 
       id="txtNumProcesso" 
       name="txtNumProcesso"
       maxlength="25"
       onkeypress="infraMascara(this,event,'#######-##.####.#.##.####')">
```
- **Tipo:** Texto formatado
- **Formato CNJ:** `NNNNNNN-DD.AAAA.J.TR.OOOO`
- **Máscara:** Aplicada automaticamente ao digitar
- **Obrigatório:** Não (mas necessário para busca)

---

### **Campo 2: OAB**
```html
<input type="text" 
       id="txtStrOAB" 
       name="txtStrOAB"
       maxlength="">
```
- **Tipo:** Texto livre
- **Uso:** Buscar processos de um advogado específico
- **Exemplo:** `MG12345`

---

### **Campo 3: Nome da Parte**
```html
<input type="text" 
       id="txtStrParte" 
       name="txtStrParte"
       maxlength="">
```
- **Tipo:** Texto livre
- **Uso:** Buscar por nome de autor/réu
- **Fonética:** Checkbox disponível (☑ ativo por padrão)

---

### **Campo 4: CPF/CNPJ**
```html
<input type="text" 
       id="txtCpfCnpj" 
       name="txtCpfCnpj"
       maxlength="14"
       onkeypress="mascaraCpfCnpj(this,event)">
```
- **Tipo:** Números apenas
- **Máscara:** Alterna entre CPF (11 dígitos) e CNPJ (14 dígitos)
- **Controlado por:** Radio buttons `rdoPessoaFisica` / `rdoPessoaJuridica`

---

## 🎯 3. AÇÃO DO FORMULÁRIO

### **Quando clica em "Consultar":**

```python
# URL de destino:
action = "externo_controlador.php?acao=processo_consulta_publica"

# Método:
method = "POST"

# Validação:
onsubmit = "return OnSubmitForm()"
```

**O que acontece:**
1. Validação JavaScript (`OnSubmitForm()`)
2. Submissão POST para `externo_controlador.php`
3. Redirecionamento para página de resultados
4. Exibição de dados do processo encontrado

---

## 📊 4. DADOS QUE PODERIAM SER EXTRAÍDOS (Após Preencher)

**Se conseguíssemos preencher o formulário, os resultados conteriam:**

### **Estrutura Esperada de Resultado:**

```json
{
  "numero_processo": "0878961-59.2013.8.13.0702",
  "vara": "3ª Vara Criminal",
  "comarca": "Uberlândia",
  "tribunal": "TJMG",
  "partes": {
    "autor": "Ministério Público",
    "reu": "Nome do Réu"
  },
  "status": "Julgado",
  "classe": "Processo Penal",
  "assunto": "Homicídio",
  "data_distribuicao": "2013-XX-XX",
  "magistrado": "Dimas Borges de Paula",
  "movimentacoes": [
    {
      "data": "2013-XX-XX",
      "tipo": "Distribuição",
      "descricao": "..."
    }
  ]
}
```

---

## 🔧 5. INFORMAÇÕES PARA AUTOMAÇÃO

### **Seletores CSS Encontrados:**

```python
# Número do processo
"#txtNumProcesso"

# OAB
"#txtStrOAB"

# Nome da parte
"#txtStrParte"

# CPF/CNPJ
"#txtCpfCnpj"

# Botão consultar
"#sbmNovo"

# Formulário completo
"#frmProcessoLista"
```

### **Código de Exemplo (Playwright):**

```python
from playwright.async_api import async_playwright

async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    
    # Navegar
    await page.goto('https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica')
    
    # Preencher número do processo
    await page.fill('#txtNumProcesso', '0878961-59.2013.8.13.0702')
    
    # Clicar em consultar
    await page.click('#sbmNovo')
    
    # Aguardar resultados
    await page.wait_for_selector('.resultado, .processo', timeout=10000)
    
    # Extrair dados
    dados = await page.evaluate('''() => {
        // Extrair dados da página de resultados
        return {
            numero: document.querySelector('.numero-processo')?.textContent,
            vara: document.querySelector('.vara')?.textContent,
            // ... outros campos
        }
    }''')
    
    print(dados)
```

---

## 📈 6. COMPARAÇÃO: O QUE FOI EXTRAÍDO vs O QUE É POSSÍVEL

| Tipo de Dado | Firecrawl | Playwright | Browser MCP |
|--------------|-----------|------------|-------------|
| **HTML da página** | ✅ Completo | ✅ Completo | ✅ Completo |
| **Estrutura formulário** | ✅ Identificou | ✅ Identificou | ✅ Identificou |
| **IDs dos campos** | ✅ Todos | ✅ Todos | ✅ Todos |
| **Preencher formulário** | ❌ Não pode | ✅ Sim | ✅ Sim |
| **Submeter formulário** | ❌ Não pode | ✅ Sim | ✅ Sim |
| **Extrair resultados** | ❌ Não pode | ✅ Sim | ✅ Sim |
| **Interação JavaScript** | ⚠️ Limitada | ✅ Completa | ✅ Completa |

---

## 💡 7. CONCLUSÃO DO TESTE

### **O que o Firecrawl extraiu:**
✅ **Estrutura completa** do formulário  
✅ **Todos os IDs** dos campos  
✅ **Máscaras e validações** JavaScript  
✅ **Ação do formulário** (URL destino)  
✅ **Metadados** da página  

### **O que o Firecrawl NÃO conseguiu:**
❌ **Preencher** o formulário  
❌ **Clicar** no botão de busca  
❌ **Extrair resultados** do processo  
❌ **Interagir** com JavaScript dinâmico  

### **Para extrair dados reais:**
🔧 **Necessário:** Playwright ou Browser MCP (com interação)  
📋 **Firecrawl serve para:** Mapear estrutura e planejar automação  

---

**Status:** Firecrawl mapeou a página perfeitamente, mas precisa de ferramenta com interação para extrair dados reais do processo.

