# 🧪 Teste de Extração - Passo a Passo

Guia para testar as funções de navegador MCP do Cursor na extração de dados de processos.

---

## 🎯 Objetivo do Teste

Testar se as funções de navegador do Cursor podem:
- ✅ Substituir ou complementar o Playwright atual
- ✅ Ser mais fáceis de usar e configurar
- ✅ Extrair dados de forma eficiente
- ✅ Lidar com sites complexos (JavaScript, formulários)

---

## 📋 Informações do Teste

**Tribunal:** TJMG  
**URL:** `https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica`  
**Processo de Teste:** `0878961-59.2013.8.13.0702`  
**Dados esperados:** número, vara, partes, movimentações, status

---

## 🔧 Etapas do Teste

### **Etapa 1: Navegar até o Site**

**Ação:** Abrir a página de consulta pública do eproc

```
URL: https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica
```

**Função MCP:**
```python
mcp_cursor-ide-browser_browser_navigate(
    url="https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica"
)
```

---

### **Etapa 2: Verificar Estrutura da Página**

**Ação:** Capturar snapshot para ver campos disponíveis

**Função MCP:**
```python
snapshot = mcp_cursor-ide-browser_browser_snapshot()
```

**O que procurar:**
- Campo de número do processo
- Botão de buscar/consultar
- Campos de filtro (OAB, nome, etc)

---

### **Etapa 3: Preencher Formulário**

**Ação:** Inserir número do processo no campo apropriado

**Processo de teste:** `0878961-59.2013.8.13.0702`

**Função MCP:**
```python
mcp_cursor-ide-browser_browser_type(
    element="Campo de número do processo",
    ref="[ref_do_campo]",  # Obter do snapshot
    text="0878961-59.2013.8.13.0702"
)
```

---

### **Etapa 4: Clicar em Buscar**

**Ação:** Clicar no botão de busca/consulta

**Função MCP:**
```python
mcp_cursor-ide-browser_browser_click(
    element="Botão de buscar",
    ref="[ref_do_botao]"  # Obter do snapshot
)
```

---

### **Etapa 5: Aguardar Resultados**

**Ação:** Aguardar carregamento da página de resultados

**Função MCP:**
```python
mcp_cursor-ide-browser_browser_wait_for(
    text="Resultado"  # Ou outro texto indicativo
)
```

---

### **Etapa 6: Capturar Resultados**

**Ação:** Tirar novo snapshot para ver dados do processo

**Função MCP:**
```python
snapshot_resultado = mcp_cursor-ide-browser_browser_snapshot()
```

**O que extrair:**
- Número do processo
- Vara/Turma
- Partes (autor, réu)
- Status
- Movimentações (se visíveis)
- Data de distribuição
- Magistrado

---

### **Etapa 7: Extrair Dados**

**Ação:** Analisar snapshot e extrair informações estruturadas

**Dados esperados:**
```json
{
    "numero_processo": "0878961-59.2013.8.13.0702",
    "vara": "3ª Vara Criminal",
    "comarca": "Uberlândia",
    "tribunal": "TJMG",
    "partes": {
        "autor": "...",
        "reu": "..."
    },
    "status": "...",
    "movimentacoes": [...]
}
```

---

## 📊 Métricas de Sucesso

### **✅ Critérios:**

1. **Navegação:** Consegue acessar o site? (Sim/Não)
2. **Tempo:** Quanto tempo levou? (< 10s ideal)
3. **Preenchimento:** Consegue preencher formulário? (Sim/Não)
4. **Busca:** Consegue acionar busca? (Sim/Não)
5. **Extração:** Quantos campos conseguiu extrair? (X/7)
6. **Precisão:** Dados estão corretos? (Sim/Não)

### **📈 Comparação:**

| Métrica | Playwright Atual | MCP Browser | Diferença |
|---------|-----------------|------------|-----------|
| Tempo setup | ~5s | ? | ? |
| Tempo execução | ~10-15s | ? | ? |
| Facilidade código | Média | ? | ? |
| Manutenção | Média | ? | ? |
| Campos extraídos | ? | ? | ? |

---

## 🎯 Executar Teste Agora

**No Cursor, você pode pedir:**

> "Use as funções de navegador para testar extração de dados do eproc do TJMG. Navegue até a URL, preencha o processo 0878961-59.2013.8.13.0702, busque e extraia os dados."

---

## 📝 Relatório do Teste

Após executar, documente:

1. ✅ Sucesso ou falha
2. ⏱️ Tempo de execução
3. 📊 Campos extraídos
4. 🔍 Dificuldades encontradas
5. 💡 Melhorias sugeridas
6. ✅ Comparação com Playwright

---

**Última atualização:** Outubro 2025

