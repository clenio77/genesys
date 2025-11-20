# 🚀 Guia - Extração de Processos via API CNJ em Fila

## 📋 Descrição

Script para extrair dados completos de processos judiciais usando a **API Pública do CNJ (DataJud)**. Processa múltiplos processos em fila, extraindo:

✅ **Dados principais** (classe, assunto, tribunal, vara, status)  
✅ **Movimentações** (todas, classificadas)  
✅ **Sentenças** identificadas  
✅ **Julgados** identificados  
✅ **Denúncias** identificadas  
✅ **Partes** (autor, réu, etc.)  
✅ **Estatísticas** completas

---

## 🎯 Uso

⚠️ **Nota:** API pública, sem necessidade de configuração de chaves!

### **Opção 1: Processo Individual**

```bash
python3 extrair_processos_cnj_fila.py "0878961-59.2013.8.13.0702"
```

### **Opção 2: Múltiplos Processos**

```bash
python3 extrair_processos_cnj_fila.py "proc1" "proc2" "proc3"
```

### **Opção 3: Arquivo com Lista**

Crie um arquivo `processos.txt`:
```
0878961-59.2013.8.13.0702
0001234-56.2024.8.26.0100
0005678-90.2023.8.26.0100
```

Execute:
```bash
python3 extrair_processos_cnj_fila.py processos.txt
```

---

## 📊 O Que É Extraído

### **1. Dados Principais**
- Número do processo
- Classe processual
- Assunto
- Tribunal
- Vara/Órgão julgador
- Status
- Data de autuação
- Segredo de justiça

### **2. Movimentações (Todas)**
- Data
- Descrição completa
- Tipo
- Órgão julgador

### **3. Movimentações Classificadas**
- ✅ **Sentenças** - Identificadas automaticamente
- ✅ **Julgados** - Recursos, acórdãos, apelações
- ✅ **Denúncias** - Denúncias criminais
- ✅ **Petições** - Requerimentos, manifestações
- ✅ **Despachos** - Determinações, provimentos
- ✅ **Certidões** - Intimações, certidões

### **4. Partes**
- Nome/Razão social
- Tipo (autor, réu, assistente, etc.)
- Documento (CPF/CNPJ)
- Polo processual

### **5. Estatísticas**
- Total de movimentações
- Total de partes
- Total de sentenças
- Total de julgados
- Total de denúncias

---

## 📁 Arquivos Gerados

### **Pasta: `extracao_cnj/`**

Para cada processo processado:
- `processo_{numero_formatado}.json` - Dados completos do processo

Ao final:
- `resumo_extracao_{timestamp}.json` - Resumo da execução completa

---

## 🔧 Configuração

### **Delay Entre Requisições**

No código, ajuste o delay (em segundos):
```python
extrator = CNJExtractor(delay_segundos=1.0)  # 1 segundo entre requisições
```

**Recomendações:**
- ⚠️ **1 segundo** - Conservador, respeita rate limits
- ⚠️ **0.5 segundos** - Mais rápido, pode ter limites
- ❌ **< 0.5 segundos** - Pode causar bloqueio (429)

### **Timeout**

Timeout padrão: **15 segundos** por requisição

---

## 📄 Formato dos Dados

### **Estrutura JSON:**

```json
{
  "numero_processo": "0878961-59.2013.8.13.0702",
  "fonte": "API CNJ DataJud",
  "data_extracao": "2025-10-31T...",
  "dados_principais": {
    "numero": "...",
    "classe": "...",
    "assunto": "...",
    "tribunal": "...",
    "vara": "...",
    "status": "...",
    "data_autuacao": "..."
  },
  "movimentacoes": [
    {
      "data": "...",
      "descricao": "...",
      "tipo": "...",
      "orgao": "..."
    }
  ],
  "movimentacoes_classificadas": {
    "sentencas": [...],
    "julgados": [...],
    "denuncias": [...],
    "peticoes": [...],
    "despachos": [...],
    "certidoes": [...]
  },
  "partes": [
    {
      "nome": "...",
      "tipo": "...",
      "documento": "...",
      "polo": "..."
    }
  ],
  "estatisticas": {
    "total_movimentacoes": 10,
    "total_partes": 3,
    "total_sentencas": 1,
    "total_julgados": 2,
    "total_denuncias": 0
  }
}
```

---

## ⚠️ Limitações da API CNJ

### **1. Dados Disponíveis**
- ✅ Metadados do processo
- ✅ Movimentações (quando disponíveis)
- ✅ Partes (quando disponíveis)
- ❌ **Documentos completos** (PDFs, etc.) - **NÃO disponíveis via API**
- ❌ Conteúdo de petições - Apenas descrição
- ❌ Texto completo de sentenças - Apenas descrição

### **2. Processos Antigos**
- Processos muito antigos podem não estar na API
- API CNJ pode ter dados apenas de processos mais recentes
- Para processos antigos, usar eproc ou sistema do tribunal

### **3. Rate Limits**
- API pública pode ter limites de requisições
- Respeitar delay entre requisições
- Se receber erro 429, aumentar delay

### **4. Segredo de Justiça**
- Processos em segredo podem ter dados limitados
- Movimentações podem estar censuradas

---

## 🔍 Classificação Automática

O script identifica automaticamente:

### **Sentenças**
Palavras-chave: "sentença", "julgamento", "decisão", "sentenciar", "julgo"

### **Julgados**
Palavras-chave: "julgado", "acórdão", "recurso", "apelação", "agravo", "embargos"

### **Denúncias**
Palavras-chave: "denúncia", "imputação", "acusação"

### **Petições**
Palavras-chave: "petição", "requerimento", "manifestação"

### **Despachos**
Palavras-chave: "despacho", "determinação", "provimento"

### **Certidões**
Palavras-chave: "certidão", "intimação"

---

## 🎯 Exemplos de Uso

### **Exemplo 1: Processo Único**

```bash
python3 extrair_processos_cnj_fila.py "0878961-59.2013.8.13.0702"
```

### **Exemplo 2: Múltiplos Processos**

```bash
python3 extrair_processos_cnj_fila.py \
  "0878961-59.2013.8.13.0702" \
  "0001234-56.2024.8.26.0100" \
  "0005678-90.2023.8.26.0100"
```

### **Exemplo 3: Arquivo com Lista**

```bash
# Criar arquivo
cat > processos.txt << EOF
0878961-59.2013.8.13.0702
0001234-56.2024.8.26.0100
0005678-90.2023.8.26.0100
EOF

# Executar
python3 extrair_processos_cnj_fila.py processos.txt
```

---

## 📊 Saída do Script

Durante execução:
```
============================================================
🚀 PROCESSANDO 3 PROCESSO(S) EM FILA
============================================================

[1/3] 📄 Processando: 0878961-59.2013.8.13.0702
   ✅ Sucesso! Movimentações: 15
      • Sentenças: 1
      • Julgados: 2
      • Denúncias: 0
      💾 Salvo: processo_0878961_59_2013_8_13_0702.json
   ⏳ Aguardando 1.0s...

[2/3] 📄 Processando: 0001234-56.2024.8.26.0100
   ✅ Sucesso! Movimentações: 8
      • Sentenças: 0
      • Julgados: 1
      • Denúncias: 0
      💾 Salvo: processo_0001234_56_2024_8_26_0100.json
   ⏳ Aguardando 1.0s...

============================================================
📊 RESUMO DA EXECUÇÃO
============================================================
✅ Sucessos: 2/3
❌ Erros: 1/3
📄 Resumo salvo: resumo_extracao_20251031_143022.json
============================================================
```

---

## ❌ Tratamento de Erros

### **Erros Comuns:**

1. **Número inválido**
   - Formato incorreto
   - Script tenta formatar automaticamente
   - **Solução:** Verificar formato CNJ: `NNNNNNN-DD.AAAA.J.TR.OOOO`

2. **Processo não encontrado (404)**
   - Processo não existe na API
   - Processo muito antigo
   - Processo em segredo de justiça
   - **Solução:** 
     - Verificar se o processo existe no sistema do tribunal
     - Processos muito antigos podem não estar disponíveis na API
     - Tentar buscar no site oficial do tribunal

3. **Rate limit (429)**
   - Muitas requisições
   - Aumentar delay entre requisições
   - **Solução:** 
     ```python
     extrator = CNJExtractor(delay_segundos=2.0)  # Aumentar para 2 segundos
     ```

4. **Timeout**
   - API demorou muito para responder
   - Tentar novamente
   - **Solução:** Aguardar alguns minutos e tentar novamente

5. **Erro de conexão**
   - Problema de rede
   - API temporariamente indisponível
   - **Solução:** Verificar conexão com internet e status da API CNJ

### **Debug Avançado:**

Para ver detalhes completos dos erros, verifique o arquivo `resumo_extracao_*.json`:

```bash
# Ver último resumo gerado
cat extracao_cnj/resumo_extracao_*.json | tail -n 50
```

**Campos úteis no resumo:**
- `erros_detalhados`: Lista completa de erros com número do processo
- `status_code`: Código HTTP retornado pela API
- `resposta`: Resposta parcial da API (últimos 500 caracteres)

---

## 🧪 Testando e Validando

### **Testar Processo Único**

Antes de processar uma lista grande, teste com um processo conhecido:

```bash
# Processo de exemplo (TJMG)
python3 extrair_processos_cnj_fila.py "0878961-59.2013.8.13.0702"
```

### **Validar Formato antes de Processar**

O script valida automaticamente, mas você pode verificar manualmente:

```python
from extrair_processos_cnj_fila import CNJExtractor

extrator = CNJExtractor()
numero = "0878961-59.2013.8.13.0702"

# Validar formato
if extrator.validar_numero_processo(numero):
    print("✅ Formato válido!")
else:
    formatado = extrator.formatar_numero_processo(numero)
    if formatado:
        print(f"✅ Formatado: {formatado}")
    else:
        print("❌ Número inválido")
```

### **Verificar Processos Disponíveis na API**

Nem todos os processos estão disponíveis na API CNJ. Processos mais recentes têm maior probabilidade de estar disponíveis.

**Tribunais com melhor cobertura:**
- TJMG (código 13)
- TJSP (código 02)
- TJRJ (código 19)

**Processos com menor probabilidade:**
- Processos muito antigos (antes de 2010)
- Processos em segredo de justiça
- Processos de tribunais menores

---

## 🔄 Integração com Kermartin

Este script extrai dados da **API CNJ**. Para dados mais completos:

1. **API CNJ** → Dados básicos e metadados
2. **eProc/Tribunal** → Documentos completos (PDFs, petições)
3. **Kermartin** → Base local com dados coletados

**Fluxo recomendado:**
```
1. Extrair metadados via API CNJ (este script)
2. Para documentos completos, usar extração do eProc
3. Armazenar tudo no Kermartin
```

---

## 📚 Referências

- **API CNJ:** https://datajud-wiki.cnj.jus.br/api-publica/
- **Documentação DataJud:** https://www.cnj.jus.br/sistemas/datajud/api-publica/

---

## ✅ Vantagens da API CNJ

- ✅ **Gratuita** e pública
- ✅ **Padronizada** (todos os tribunais)
- ✅ **Rápida** (sem scraping)
- ✅ **Confiável** (dados oficiais)
- ✅ **Completa** (metadados e movimentações)

---

**Pronto para usar! 🚀**

