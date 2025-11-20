# ✅ Correção: Erro 401 na API CNJ

## 🔧 Problema Identificado

A API CNJ está retornando **status 401 (não autorizado)** para consultas, e o código não estava tentando buscar no Kermartin nesse caso.

**Logs mostravam:**
```
Erro ao consultar processo. Status: 401
```

**Problema:**
- Código só tentava Kermartin no caso 404
- Erros de status (401, 403, 500, etc.) não tentavam fallback
- Playwright não instalado (dependência opcional)

---

## ✅ Correção Implementada

Agora **TODOS** os erros de status da API tentam buscar no Kermartin:

- ✅ 401 (não autorizado) → Tenta Kermartin
- ✅ 403 (proibido) → Tenta Kermartin  
- ✅ 404 (não encontrado) → Tenta Kermartin
- ✅ 500 (erro servidor) → Tenta Kermartin
- ✅ Timeout → Tenta Kermartin
- ✅ Erro de conexão → Tenta Kermartin

---

## 📊 Fluxo Atualizado

```
1. Tenta API CNJ
   ↓ (status 401/403/404/500/etc)
2. Tenta Kermartin automaticamente
   ↓ (se encontrar)
3. Retorna dados do Kermartin formatados
   ↓ (se não encontrar)
4. Mensagem de erro informativa
```

---

## 🧪 Teste

Processo `0878961-59.2013.8.13.0702` agora deve funcionar:

```
/processo
> 0878961-59.2013.8.13.0702
```

**Resultado esperado:**
- API CNJ retorna 401
- Busca automaticamente no Kermartin
- Encontra o processo
- Mostra dados formatados

---

## ⚠️ Sobre a API CNJ

O erro 401 pode indicar:
- API requer autenticação (precisa de API key)
- API mudou formato de acesso
- Rate limiting ativado

Mas agora isso não é problema! O bot sempre tenta o Kermartin como fallback.

---

**Status:** ✅ **CORREÇÃO APLICADA - REINICIE O BOT**

