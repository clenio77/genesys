# 📊 Análise dos Dados Extraídos pelo Firecrawl

## 🔍 Dados Capturados da Página do eproc TJMG

---

## 📋 Estrutura do Formulário Identificada

### **Campos de Entrada Encontrados:**

#### **1. Número do Processo**
- **ID:** `txtNumProcesso`
- **Tipo:** Text input
- **Máscara:** `#######-##.####.#.##.####` (formato CNJ)
- **Maxlength:** 25 caracteres
- **Label:** "Nº Processo"
- **Obrigatório:** Sim (infraLabelObrigatorio)

#### **2. Chave do Processo**
- **ID:** `txtNumChave`
- **Tipo:** Text input
- **Máscara:** `############` (12 dígitos)
- **Maxlength:** 12
- **Label:** "Chave do processo"
- **Obrigatório:** Sim

#### **3. Chave do Documento**
- **ID:** `txtNumChaveDocumento`
- **Tipo:** Text input
- **Máscara:** `############` (12 dígitos)
- **Maxlength:** 12
- **Label:** "Chave Documento"
- **Obrigatório:** Sim

#### **4. Nome da Parte**
- **ID:** `txtStrParte`
- **Tipo:** Text input
- **Label:** "Nome da Parte"
- **Observação:** "(somente pessoa física ou jurídica)"
- **Obrigatório:** Sim

#### **5. Pesquisa Fonética**
- **ID:** `chkFonetica`
- **Tipo:** Checkbox
- **Default:** Checked (S)
- **Label:** "Pesquisa fonética"

#### **6. OAB**
- **ID:** `txtStrOAB`
- **Tipo:** Text input
- **Label:** "OAB"
- **Obrigatório:** Sim

#### **7. Tipo de Pessoa**
- **Radio buttons:**
  - `rdoPessoaFisica` - CPF
  - `rdoPessoaJuridica` - CNPJ

#### **8. CPF/CNPJ**
- **ID:** `txtCpfCnpj`
- **Tipo:** Text input
- **Máscara:** Dinâmica (CPF ou CNPJ)
- **Maxlength:** 14
- **Label:** "CPF:" ou "CNPJ:"
- **Observação:** "(somente números)"

### **Botões de Ação:**

#### **Consultar**
- **ID:** `sbmNovo`
- **Tipo:** Submit button
- **Accesskey:** "C"
- **Texto:** "Consultar"
- **Ação:** `OnSubmitForm()`

#### **Voltar**
- **ID:** `btnVoltar`
- **Tipo:** Button
- **Accesskey:** "V"
- **Ação:** `location.href='externo_controlador.php?acao=principal'`

---

## 📄 Conteúdo HTML Extraído

### **Tags Principais Identificadas:**

```html
<form id="frmProcessoLista" 
      method="post" 
      onsubmit="return OnSubmitForm();" 
      action="externo_controlador.php?acao=processo_consulta_publica&amp;acao_origem=&amp;acao_retorno=processo_consulta_publica">

  <!-- Campo Número do Processo -->
  <input type="text" 
         id="txtNumProcesso" 
         name="txtNumProcesso" 
         class="infraText" 
         onkeypress="return infraMascara(this,event,'#######-##.####.#.##.####');" 
         value="" 
         maxlength="25">

  <!-- Campo OAB -->
  <input type="text" 
         id="txtStrOAB" 
         name="txtStrOAB" 
         class="infraText" 
         value="" 
         maxlength="">

  <!-- Botão Consultar -->
  <button type="submit" 
          id="sbmNovo" 
          value="Consultar" 
          class="infraButton">
    <span class="infraTeclaAtalho">C</span>onsultar
  </button>
</form>
```

---

## 🔍 Dados Estruturados Extraídos

### **1. Informações da Página:**
- **Título:** ":: eproc - Consulta Processual - Busca de Processo ::"
- **Charset:** ISO-8859-1
- **Status Code:** 200 (OK)
- **Content Type:** text/html; charset=iso-8859-1
- **Robots:** noindex

### **2. Estrutura de Navegação:**
O site tem um menu lateral com:
- Acessibilidade
- Entrar no Sistema
- Cadastre-se AQUI!
- Consulta Autenticidade
- Consulta Guia de Custas
- Audiências
- **Consulta Pública de Processos** ← Página atual
- Consulta de Documento por Chave
- Fale Conosco
- Fórum de Conciliação
- Legislação
- Sessões de Julgamento
- Tutoriais

### **3. JavaScript Identificado:**
- `OnSubmitForm()` - Validação do formulário
- `infraMascara()` - Máscara de entrada para números
- `trocarCpfCnpj()` - Alterna entre CPF e CNPJ
- `mascaraCpfCnpj()` - Aplica máscara de CPF/CNPJ
- `inicializar()` - Inicialização da página

### **4. CSS Identificado:**
Múltiplos arquivos CSS carregados:
- `bundle-bs4.css`
- `bundle-bs4-contrast.css`
- `bundle-global.css`
- `bundle-infra.css`
- `bundle-infra-contrast.css`
- `infra-barra-progresso.css`
- `infra-impressao-global.css`
- `infra-ajax.css`
- `infra-calendario.css`
- `infra-mapa.css`

---

## 📊 Métricas de Extração

### **O que foi capturado:**
- ✅ HTML completo (10.000+ linhas)
- ✅ Estrutura do formulário
- ✅ IDs de todos os campos
- ✅ Tipos de input
- ✅ Validações (máscaras, maxlength)
- ✅ JavaScript de validação
- ✅ Estrutura de navegação
- ✅ Metadados da página

### **O que NÃO foi capturado:**
- ❌ Dados de processo (precisa preencher formulário)
- ❌ Resultados de busca (precisa interagir)
- ❌ Dados dinâmicos carregados via JavaScript
- ❌ Cookies ou sessões

---

## 🎯 Informações Úteis para Automação

### **Para Preencher Formulário (Playwright/Browser):**

```python
# Número do processo
page.fill('#txtNumProcesso', '0878961-59.2013.8.13.0702')

# Ou por OAB
page.fill('#txtStrOAB', 'MG12345')

# Ou por nome da parte
page.fill('#txtStrParte', 'João Silva')

# Clicar em consultar
page.click('#sbmNovo')
```

### **Campos Prioritários para Teste:**
1. **Número do Processo** (`txtNumProcesso`) - Mais direto
2. **OAB** (`txtStrOAB`) - Para buscar processos do advogado
3. **Nome da Parte** (`txtStrParte`) - Para busca por pessoa

---

## 💡 Conclusão

**O que o Firecrawl extraiu:**
- ✅ Estrutura completa do formulário
- ✅ IDs e seletores para automação
- ✅ Regras de validação (máscaras)
- ✅ Ação do formulário (URL de destino)

**O que ainda precisa ser feito:**
- Preencher formulário (não automático com Firecrawl)
- Submeter formulário (não automático)
- Extrair resultados (precisa interação)

**Recomendação:**
- Firecrawl: Excelente para **mapear** a estrutura
- Playwright/Browser MCP: Necessário para **interagir** e extrair dados reais

