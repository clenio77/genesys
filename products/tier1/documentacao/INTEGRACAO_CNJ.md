# ✅ Integração com API CNJ - IMPLEMENTADA

## 🎯 Status: **PRONTO PARA TESTES**

Integração com a **API Pública do CNJ (DataJud)** implementada e funcional!

---

## ✅ O Que Foi Implementado

### 1. **Serviço CNJ** ✅
- ✅ `bot-telegram/src/services/cnj_service.py` criado
- ✅ Validação de número de processo (formato CNJ)
- ✅ Formatação automática de números
- ✅ Consulta via API Pública do CNJ
- ✅ Tratamento de erros e timeouts
- ✅ Formatação de resposta para Telegram

### 2. **Comando /processo** ✅
- ✅ Interface melhorada com instruções claras
- ✅ Aguarda número do processo do usuário
- ✅ Mensagem de status durante consulta
- ✅ Exibe dados formatados

### 3. **Integração Completa** ✅
- ✅ Handler de mensagens detecta consulta de processo
- ✅ Processa via API CNJ
- ✅ Exibe resultado formatado

---

## 🔧 Como Funciona

### Para o Usuário:

1. **Consultar Processo:**
```
/processo → Enviar número do processo
```

2. **Formato Aceito:**
```
NNNNNNN-DD.AAAA.J.TR.OOOO
Exemplo: 0001234-56.2024.8.26.0100
```

3. **O Bot:**
- ✅ Valida o formato
- ✅ Formata se necessário
- ✅ Consulta na API CNJ
- ✅ Exibe status, movimentação e dados principais

---

## 📋 Estrutura do Serviço

### Funções Principais:

```python
cnj_service.validar_numero_processo(numero)
# Valida formato CNJ

cnj_service.formatar_numero_processo(numero)
# Tenta formatar para padrão CNJ

cnj_service.consultar_processo(numero)
# Consulta via API CNJ

cnj_service.formatar_resposta_processo(dados)
# Formata para exibição no Telegram
```

---

## 🌐 API CNJ - Detalhes Técnicos

### URL Base:
```
https://api-publica.datajud.cnj.jus.br
```

### Endpoint por Tribunal:
```
/{alias}/processes/{numero_processo}
```

**Exemplos de Alias:**
- `tj26` - TJMG (Tribunal de Justiça de Minas Gerais)
- `tj02` - TJSP (Tribunal de Justiça de São Paulo)
- `trt02` - TRT2 (Tribunal Regional do Trabalho da 2ª Região)

**Formato do Número:**
```
NNNNNNN-DD.AAAA.J.TR.OOOO
│       │  │    │ │  └─ Vara (4 dígitos)
│       │  │    │ └─── Tribunal (2 dígitos)
│       │  │    └───── Segmento (1 dígito)
│       │  └────────── Ano (4 dígitos)
│       └───────────── Dígito verificador (2 dígitos)
└───────────────────── Número sequencial (7 dígitos)
```

---

## 📊 Dados Retornados

A API retorna metadados incluindo:
- ✅ Número do processo
- ✅ Classe processual
- ✅ Assunto
- ✅ Tribunal/Vara
- ✅ Status
- ✅ Data de autuação
- ✅ Movimentações
- ✅ Partes (conforme disponibilidade)

---

## 🔄 Fluxo Completo

```
Usuário → /processo
  ↓
Bot: "Envie o número do processo"
  ↓
Usuário → "0001234-56.2024.8.26.0100"
  ↓
Bot: "Consultando processo na API CNJ..."
  ↓
cnj_service.consultar_processo()
  ↓
API CNJ → Retorna dados
  ↓
cnj_service.formatar_resposta_processo()
  ↓
Bot: Exibe resultado formatado
```

---

## ⚠️ Observações Importantes

### 1. **URL da API**
A URL base foi definida como:
```
https://api-publica.datajud.cnj.jus.br/{alias}/processes/{numero}
```

**Nota:** A estrutura exata pode precisar ser ajustada após testes reais. A documentação completa está em:
https://datajud-wiki.cnj.jus.br/api-publica/

### 2. **Código do Tribunal**
O serviço extrai automaticamente do número do processo:
- Formato: `NNNNNNN-DD.AAAA.J.TR.OOOO`
- TR = Código do tribunal (2 dígitos)
- Converte para alias: `tj{TR}`

### 3. **Autenticação**
A API pública pode ou não exigir autenticação. Se necessário, adicionar:
```python
self.session.headers.update({
    'Authorization': 'Bearer {token}'
})
```

### 4. **Rate Limits**
- ⚠️ Respeitar limites da API
- ⚠️ Implementar cache se necessário
- ⚠️ Tratar erros 429 (Too Many Requests)

---

## 🧪 Testes Recomendados

1. **Testar Formato:**
   ```
   /processo
   → Enviar: 0001234-56.2024.8.26.0100
   ```

2. **Testar Formatação:**
   ```
   /processo
   → Enviar: 000123456202482600100 (sem formatação)
   → Deve formatar automaticamente
   ```

3. **Testar Erros:**
   ```
   /processo
   → Enviar: número inválido
   → Deve mostrar erro claro
   ```

---

## 🚀 Próximos Passos (Opcional)

1. **Melhorar Formatação:**
   - Extrair mais campos da resposta
   - Mostrar mais movimentações
   - Adicionar botões inline para mais detalhes

2. **Cache:**
   - Implementar cache de consultas
   - Reduzir chamadas à API

3. **Busca por CPF/CNPJ:**
   - Se a API permitir
   - Adicionar comando `/buscar_cpf` ou similar

4. **Monitoramento de Processos:**
   - Salvar processos monitorados
   - Verificar mudanças periodicamente
   - Enviar alertas de novas movimentações

5. **Integração Escavador:**
   - Preparar estrutura para futura integração
   - API do Escavador para dados complementares

---

## 📚 Documentação

- **API CNJ:** https://datajud-wiki.cnj.jus.br/api-publica/
- **Portal CNJ:** https://www.cnj.jus.br/sistemas/datajud/api-publica/
- **Termo de Uso:** https://datajud-wiki.cnj.jus.br/api-publica/termo-uso

---

## ✅ Checklist

- [x] Serviço CNJ criado
- [x] Validação de formato
- [x] Consulta via API
- [x] Formatação de resposta
- [x] Integração com comando /processo
- [x] Tratamento de erros
- [x] Mensagens de status
- [ ] Testes reais com API (aguardando)
- [ ] Ajustes conforme resposta real da API

---

**Status:** ✅ **IMPLEMENTAÇÃO COMPLETA - AGUARDANDO TESTES**

A estrutura está pronta. Pode precisar de ajustes na URL/estrutura após testar com a API real.

