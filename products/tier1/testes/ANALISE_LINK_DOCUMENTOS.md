# 📄 Análise do Link de Documentos Encontrado

## 🔍 Link Identificado

**URL:** `https://eproc-consulta-publica-1g.tjmg.jus.br/externo_controlador.php?acao=consulta_autenticidade_documentos`

**Texto:** "Documentos arrow_drop_down"

**Tipo:** Link do menu lateral (não específico do processo)

---

## ⚠️ Problema Identificado

### **O que aconteceu:**

1. A extração encontrou **0 movimentações, 0 partes, 0 dados principais**
2. Encontrou apenas **1 link genérico** (menu lateral)
3. O link é do **menu**, não do processo específico

### **Causa Provável:**

- ❌ A página **não carregou** o resultado do processo
- ❌ Ainda está na **página de busca** (não foi redirecionada)
- ❌ O processo **não foi encontrado** pelo sistema
- ❌ É necessário **mais tempo** para carregar
- ❌ Precisa **preencher formulário diferente** ou usar outra URL

---

## 🔍 Sobre o Link de Documentos

### **O que é:**

O link encontrado (`consulta_autenticidade_documentos`) é uma **página genérica** do menu lateral, não específica para o processo.

### **Como funcionaria corretamente:**

1. Fazer busca do processo
2. Na página de resultado, **clicar no processo** (se houver lista)
3. Isso abre página **específica do processo**
4. Na página específica, acessar seção de **documentos**
5. Ou usar link direto com **número do processo na URL**

### **Problema atual:**

O sistema eproc pode requerer:
- ✅ Sessão/autenticação (mesmo para consulta pública)
- ✅ Parâmetros específicos na URL
- ✅ Clique em elemento para ver detalhes do processo
- ✅ Tempo de carregamento maior

---

## 🛠️ Como Resolver

### **Opção 1: Debug Visual (Recomendado)**

Execute o script de debug para ver o que realmente aparece:

```bash
python3 debug_extracao_eproc.py
```

Isso vai:
- Abrir navegador
- Fazer busca
- Mostrar o que aparece na tela
- Salvar screenshot e HTML
- Analisar estrutura completa

### **Opção 2: Analisar Link de Documentos**

Se quiser ver o que tem no link de documentos:

```bash
python3 analisar_link_documentos.py
```

Isso vai:
- Fazer busca do processo
- Procurar todos os links relacionados
- Tentar acessar página de documentos
- Analisar estrutura

### **Opção 3: Versão Melhorada**

Execute a versão V2 com melhor debug:

```bash
python3 extrair_processo_completo_v2.py
```

---

## 📊 O Que Esperar se Funcionar Corretamente

### **Página de Resultado do Processo deve ter:**

✅ **Dados principais:**
- Número do processo (visível)
- Classe do processo
- Vara/Turma
- Status
- Comarca

✅ **Tabela de Partes:**
- Autor
- Réu
- Advogados
- Ministério Público

✅ **Tabela de Movimentações:**
- Data | Tipo | Descrição
- Sentenças
- Julgados
- Denúncias
- Outras movimentações

✅ **Links para Documentos:**
- Links específicos para PDFs
- Sentenças em PDF
- Denúncias em PDF
- Julgados em PDF
- Outros documentos

---

## 🎯 Próximos Passos

1. **Execute o debug:** `python3 debug_extracao_eproc.py`
2. **Analise o screenshot** gerado
3. **Verifique o HTML** salvo
4. **Identifique o problema** real (não carregou? Precisa clicar? Erro?)
5. **Ajuste os seletores** baseado no HTML real

---

## 💡 Suspeitas

### **Possíveis problemas:**

1. **Processo muito antigo (2013)** → Pode não estar mais disponível
2. **Página requer JavaScript pesado** → Precisa aguardar mais tempo
3. **Sistema anti-bot** → Bloqueando acesso automatizado
4. **URL diferente** → Pode precisar de parâmetros diferentes
5. **Precisa clicar** → Pode ter lista de processos e precisa clicar no específico

---

**Execute o debug para descobrir o problema real!** 🔍

