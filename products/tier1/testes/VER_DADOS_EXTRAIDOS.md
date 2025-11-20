# 📊 Visualizando Dados Extraídos da API CNJ

## 🔍 Script de Debug

Para ver exatamente o que a API retorna (dados reais ou erros), use:

```bash
python3 debug_api_cnj.py "NUMERO_DO_PROCESSO"
```

Este script mostra:
- ✅ URL da requisição
- ✅ Payload enviado
- ✅ Headers da requisição
- ✅ Status code da resposta
- ✅ Resposta completa da API (JSON bruto)
- ✅ Análise da estrutura retornada

---

## 📄 Estrutura dos Dados Extraídos

Quando um processo é encontrado na API CNJ, os dados são estruturados no seguinte formato:

### **Arquivo JSON Gerado: `processo_{numero}.json`**

```json
{
  "numero_processo": "0878961-59.2013.8.13.0702",
  "fonte": "API CNJ DataJud",
  "data_extracao": "2025-10-31T20:10:36.628171",
  "dados_principais": {
    "numero": "0878961-59.2013.8.13.0702",
    "classe": "Ação Penal",
    "assunto": "Crimes contra a Administração Pública",
    "tribunal": "Tribunal de Justiça de Minas Gerais",
    "vara": "1ª Vara Criminal",
    "status": "Em andamento",
    "data_autuacao": "2013-05-15",
    "segredo_justica": false
  },
  "movimentacoes": [
    {
      "data": "2013-05-15",
      "descricao": "Distribuição do processo",
      "tipo": "Distribuição",
      "orgao": "1ª Vara Criminal"
    },
    {
      "data": "2013-06-20",
      "descricao": "Sentença proferida - Condenação",
      "tipo": "Sentença",
      "orgao": "1ª Vara Criminal"
    },
    {
      "data": "2013-07-10",
      "descricao": "Recurso de apelação interposto",
      "tipo": "Recurso",
      "orgao": "Tribunal de Justiça"
    }
  ],
  "movimentacoes_classificadas": {
    "sentencas": [
      {
        "data": "2013-06-20",
        "descricao": "Sentença proferida - Condenação",
        "tipo": "Sentença",
        "orgao": "1ª Vara Criminal"
      }
    ],
    "julgados": [
      {
        "data": "2013-07-10",
        "descricao": "Recurso de apelação interposto",
        "tipo": "Recurso",
        "orgao": "Tribunal de Justiça"
      }
    ],
    "denuncias": [],
    "peticoes": [],
    "despachos": [],
    "certidoes": []
  },
  "partes": [
    {
      "nome": "João da Silva",
      "tipo": "Autor",
      "documento": "123.456.789-00",
      "polo": "Ativo"
    },
    {
      "nome": "Maria Santos",
      "tipo": "Réu",
      "documento": "987.654.321-00",
      "polo": "Passivo"
    }
  ],
  "estatisticas": {
    "total_movimentacoes": 3,
    "total_partes": 2,
    "total_sentencas": 1,
    "total_julgados": 1,
    "total_denuncias": 0
  }
}
```

---

## 🔬 Resposta Bruta da API CNJ

A API CNJ retorna dados no formato Elasticsearch (`_search`). Estrutura típica:

```json
{
  "hits": {
    "total": {
      "value": 1
    },
    "hits": [
      {
        "_source": {
          "numeroProcesso": "0878961-59.2013.8.13.0702",
          "classe": {
            "nome": "Ação Penal",
            "codigo": "101"
          },
          "assunto": [
            {
              "nome": "Crimes contra a Administração Pública",
              "codigo": "12345"
            }
          ],
          "tribunal": {
            "nome": "Tribunal de Justiça de Minas Gerais",
            "codigo": "13"
          },
          "vara": "1ª Vara Criminal",
          "orgaoJulgador": "1ª Vara Criminal",
          "status": "Em andamento",
          "dataAbertura": "2013-05-15",
          "dataAutuacao": "2013-05-15",
          "segredoJustica": false,
          "movimentacoes": [
            {
              "data": "2013-05-15",
              "dataHora": "2013-05-15T10:30:00",
              "descricao": "Distribuição do processo",
              "tipo": "Distribuição",
              "orgao": "1ª Vara Criminal"
            }
          ],
          "partes": [
            {
              "nome": "João da Silva",
              "tipo": "Autor",
              "cpfCnpj": "12345678900",
              "documento": "123.456.789-00",
              "polo": "Ativo",
              "tipoParticipacao": "Autor"
            }
          ]
        }
      }
    ]
  }
}
```

---

## 📁 Arquivos Gerados

### **1. Arquivo Individual do Processo**
```
extracao_cnj/processo_0878961_59_2013_8_13_0702.json
```
- Dados completos do processo formatados
- Estrutura padronizada e fácil de usar
- Inclui classificação automática de movimentações

### **2. Arquivo de Resumo**
```
extracao_cnj/resumo_extracao_20251031_201026.json
```
- Estatísticas da execução
- Lista de processos processados
- Lista de erros encontrados
- Resultados completos

---

## 🔍 Como Ver os Dados

### **1. Ver último resumo gerado:**
```bash
cat extracao_cnj/resumo_extracao_*.json | jq .
```

### **2. Ver processo específico:**
```bash
cat extracao_cnj/processo_*.json | jq .
```

### **3. Ver dados reais da API (debug):**
```bash
python3 debug_api_cnj.py "NUMERO_PROCESSO"
```

### **4. Ver exemplo completo:**
```bash
cat extracao_cnj/exemplo_processo_sucesso.json | jq .
```

---

## ⚠️ Nota sobre Dados Simulados

Os arquivos de exemplo (`exemplo_processo_sucesso.json`) contêm dados **simulados** para demonstrar a estrutura esperada.

**Dados reais** só são gerados quando:
- ✅ O processo existe na API CNJ
- ✅ A API retorna dados válidos
- ✅ O script processa com sucesso

Para ver dados reais, execute o script com processos que existem na API CNJ.

---

## 🎯 Próximos Passos

1. **Testar com processos conhecidos** que existem na API
2. **Verificar formato do alias** correto para cada tribunal
3. **Ajustar código** conforme necessário baseado nas respostas reais
4. **Documentar** formatos específicos de cada tribunal

---

**Última atualização:** 2025-10-31

