# 📊 Relatório de Debug - Extração eproc TJMG

## 🔍 Problema Identificado

**Processo testado:** `0878961-59.2013.8.13.0702`  
**Data teste:** 31/10/2025  
**Resultado:** ❌ Nenhum dado extraído

### **Estatísticas da Extração:**
- ❌ Movimentações: 0
- ❌ Sentenças: 0  
- ❌ Julgados: 0
- ❌ Denúncias: 0
- ❌ Partes: 0
- ⚠️ Documentos: 1 (link genérico do menu)

---

## 🔍 Link Encontrado

### **URL:**
```
https://eproc-consulta-publica-1g.tjmg.jus.br/externo_controlador.php?acao=consulta_autenticidade_documentos
```

### **Análise:**
- ❌ **Tipo:** Link genérico do menu lateral
- ❌ **Não é específico do processo**
- ❌ **Requer autenticação/contexto de sessão**
- ❌ **Não funciona como link direto** (retorna 404 quando acessado diretamente)

---

## ⚠️ Possíveis Causas

### **1. Página Não Carregou Resultado**
- Sistema pode ter retornado erro
- JavaScript não executou completamente
- Timeout insuficiente

### **2. Processo Muito Antigo (2013)**
- Processo de **2013** pode não estar mais disponível
- Sistema pode ter arquivado
- Migrado para outro sistema

### **3. Estrutura da Página Diferente**
- Seletores CSS não correspondem à estrutura real
- Sistema usa JavaScript dinâmico
- Conteúdo carregado via AJAX

### **4. Precisa Clicar em Elemento**
- Pode aparecer lista de processos
- Precisa clicar no processo específico para ver detalhes
- Resultado não aparece automaticamente

### **5. Sistema Anti-Bot**
- Pode estar bloqueando acesso automatizado
- Requer headers específicos
- Requer comportamento mais humano

---

## 🛠️ Scripts Criados para Debug

### **1. debug_extracao_eproc.py**
**Função:** Análise detalhada com navegador visível

**Uso:**
```bash
python3 debug_extracao_eproc.py 0878961-59.2013.8.13.0702
```

**Gera:**
- ✅ Screenshot completo
- ✅ HTML completo da página
- ✅ JSON com análise detalhada
- ✅ Lista de tabelas encontradas
- ✅ Todos os links encontrados
- ✅ Textos visíveis na página

---

### **2. extrair_processo_completo_v2.py**
**Função:** Versão melhorada com múltiplas estratégias

**Melhorias:**
- ✅ Aguarda mais tempo
- ✅ Tenta múltiplas estratégias de seleção
- ✅ Captura HTML e screenshot automaticamente
- ✅ Análise detalhada da estrutura
- ✅ Debug completo habilitado

**Uso:**
```bash
python3 extrair_processo_completo_v2.py 0878961-59.2013.8.13.0702
```

---

### **3. analisar_link_documentos.py**
**Função:** Analisa especificamente o link de documentos

**Uso:**
```bash
python3 analisar_link_documentos.py 0878961-59.2013.8.13.0702
```

---

## 📋 Checklist de Debug

### **Execute e verifique:**

- [ ] **1. Executar debug_extracao_eproc.py**
  - Verificar screenshot: tem tabelas? Tem dados?
  - Verificar HTML: estrutura correta?
  
- [ ] **2. Verificar mensagens de erro**
  - Processo não encontrado?
  - Erro no sistema?
  - Timeout?
  
- [ ] **3. Verificar URL após busca**
  - URL mudou? (indica redirecionamento)
  - Ainda na página de busca?
  - Página de erro?
  
- [ ] **4. Verificar seletores**
  - Tabelas encontradas no HTML?
  - Classes CSS correspondem?
  - IDs existem na página?
  
- [ ] **5. Testar com processo mais recente**
  - Tentar processo de 2023-2024
  - Verificar se problema é do processo antigo

---

## 🎯 Próximos Passos Recomendados

### **Passo 1: Executar Debug Visual**
```bash
cd /home/clenio/Documentos/Meusagentes/genesys/products/tier1/testes
python3 debug_extracao_eproc.py 0878961-59.2013.8.13.0702
```

**O que observar:**
- O navegador abre e mostra o que?
- Aparece mensagem de erro?
- Tem lista de processos?
- Precisa clicar em algo?

### **Passo 2: Analisar Arquivos Gerados**
Após executar, verificar:
- `debug_screenshot_*.png` → Ver visualmente o que aparece
- `debug_html_*.html` → Ver estrutura HTML real
- `debug_analise_*.json` → Ver análise detalhada

### **Passo 3: Ajustar Seletores**
Baseado no HTML real capturado, ajustar:
- Seletores CSS
- Estratégias de espera
- Clicks necessários

---

## 💡 Alternativas

### **Opção 1: Processo Mais Recente**
Processo de 2013 pode não estar disponível. Testar com:
- Processo de 2023-2024
- Processo conhecido que existe

### **Opção 2: API DataJud CNJ**
Para processos mais antigos, usar API CNJ que pode ter histórico melhor.

### **Opção 3: Sistema PJe**
Se eproc não funcionar, tentar PJe:
```
https://pje.tjmg.jus.br/pje/ConsultaPublica/listView.seam
```

---

**Execute o debug e me mostre os arquivos gerados para ajustarmos!** 🔍

