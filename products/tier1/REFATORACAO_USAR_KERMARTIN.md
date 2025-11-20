# 🔄 Refatoração: Usar Apenas Kermartin como Fonte de Dados

## 🎯 Objetivo

Remover código de extração/scraping dos produtos Genesys e usar **apenas o Kermartin** como fonte de dados.

---

## 📋 Análise do Código Atual

### ⚠️ Código que Precisa ser Refatorado

#### 1. **`playwright_extractor.py`** ❌ REMOVER
**Localização:** `bot-telegram/src/services/playwright_extractor.py`

**Problema:** Faz extração direta de processos usando Playwright (scraping)

**Uso atual:**
```python
# handlers/messages.py linha 228-246
# Usado como último recurso quando processo não é encontrado
```

**Ação:** 
- ❌ **Remover completamente** este serviço
- ✅ **Substituir** por consulta ao Kermartin
- ✅ Se processo não existir no Kermartin, informar ao usuário que será coletado pelo Kermartin

#### 2. **`cnj_service.py`** ⚠️ REFATORAR
**Localização:** `bot-telegram/src/services/cnj_service.py`

**Problema:** Consulta API CNJ diretamente sem verificar Kermartin primeiro

**Uso atual:**
- Consulta API CNJ diretamente
- Não verifica se processo já existe no Kermartin

**Ação:**
- ✅ **Verificar Kermartin primeiro** antes de consultar API CNJ
- ✅ Usar API CNJ apenas como fallback quando processo não existe no Kermartin
- ✅ Documentar que é uma consulta (não extração)

#### 3. **`handlers/messages.py`** ⚠️ REFATORAR
**Localização:** `bot-telegram/src/handlers/messages.py`

**Problema:** Usa Playwright como último recurso (linha 228-246)

**Ação:**
- ✅ Remover uso do `playwright_extractor`
- ✅ Melhorar mensagem quando processo não encontrado
- ✅ Sugerir que processo será coletado pelo Kermartin

---

## 🔧 Plano de Refatoração

### **Fase 1: Remover Playwright Extractor**

#### Passo 1.1: Remover arquivo
```bash
rm products/tier1/bot-telegram/src/services/playwright_extractor.py
```

#### Passo 1.2: Atualizar `handlers/messages.py`
```python
# ANTES (linha 228-246):
# Processo não encontrado em nenhuma fonte, tentar Playwright como último recurso
try:
    from services.playwright_extractor import tribunal_extractor
    # ... código de extração ...

# DEPOIS:
# Processo não encontrado - informar que será coletado pelo Kermartin
resposta = (
    f"⚠️ Processo {numero_processo} não encontrado na base atual.\n\n"
    f"💡 Este processo será coletado pelo sistema Kermartin.\n"
    f"Você receberá uma notificação quando os dados estiverem disponíveis."
)
```

### **Fase 2: Refatorar CNJ Service**

#### Passo 2.1: Modificar `cnj_service.py` para verificar Kermartin primeiro

```python
# Adicionar método para verificar Kermartin primeiro
def consultar_processo(self, numero_processo: str) -> Optional[Dict]:
    """
    Consulta processo verificando primeiro no Kermartin,
    depois na API CNJ como fallback
    """
    # 1. Verificar no Kermartin primeiro
    from services.kermartin_service import kermartin_service
    
    processo_kermartin = kermartin_service.buscar_processo(numero_processo)
    if processo_kermartin:
        logger.info(f"Processo encontrado no Kermartin: {numero_processo}")
        return processo_kermartin
    
    # 2. Se não encontrou no Kermartin, consultar API CNJ
    logger.info(f"Processo não encontrado no Kermartin, consultando API CNJ: {numero_processo}")
    processo_cnj = self._consultar_api_cnj(numero_processo)
    
    if processo_cnj:
        # Se encontrou na API CNJ, pode ser útil salvar no Kermartin
        # (mas isso deve ser feito pelo próprio Kermartin, não pelo Genesys)
        logger.info(f"Processo encontrado na API CNJ: {numero_processo}")
        return processo_cnj
    
    # 3. Não encontrado em nenhuma fonte
    return None
```

### **Fase 3: Melhorar Integração com Kermartin**

#### Passo 3.1: Expandir `kermartin_service.py`

Adicionar métodos úteis:
```python
def buscar_processo(self, numero_processo: str) -> Optional[Dict]:
    """Busca processo na base do Kermartin"""
    # Implementar busca em SQLite ou base RAG
    
def listar_processos_usuario(self, user_id: int) -> List[Dict]:
    """Lista processos monitorados por um usuário"""
    
def obter_movimentacoes_recentes(self, numero_processo: str, dias: int = 30) -> List[Dict]:
    """Obtém movimentações recentes de um processo"""
```

---

## ✅ Checklist de Refatoração

### **Bot Telegram**
- [ ] Remover `playwright_extractor.py`
- [ ] Atualizar `handlers/messages.py` para não usar Playwright
- [ ] Refatorar `cnj_service.py` para verificar Kermartin primeiro
- [ ] Melhorar mensagens quando processo não encontrado
- [ ] Adicionar sugestão de monitoramento no Kermartin

### **Automação de Prazos**
- [ ] Verificar se há código de extração
- [ ] Garantir que usa apenas dados do Kermartin
- [ ] Implementar sincronização com processos do Kermartin

### **Assistente Virtual**
- [ ] Verificar se há código de extração
- [ ] Garantir que usa apenas dados do Kermartin
- [ ] Melhorar contexto jurídico com dados do Kermartin

---

## 📝 Padrão de Código Recomendado

### ✅ Forma CORRETA (consultar Kermartin)

```python
from services.kermartin_service import kermartin_service

def consultar_processo(numero: str):
    # 1. Sempre verificar Kermartin primeiro
    processo = kermartin_service.buscar_processo(numero)
    if processo:
        return processo
    
    # 2. Se não encontrou, pode consultar API pública (consulta, não extração)
    # Mas apenas se for necessário para funcionalidade do produto
    processo_api = consultar_api_publica(numero)
    if processo_api:
        # Informar que dados serão coletados pelo Kermartin
        return processo_api
    
    # 3. Não encontrado - informar usuário
    return None
```

### ❌ Forma INCORRETA (não fazer)

```python
# ❌ NÃO fazer scraping direto
from playwright.sync_api import sync_playwright

def extrair_processo(numero: str):
    # Isso não deve existir nos produtos Genesys
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # ... scraping ...
```

---

## 🎯 Benefícios da Refatoração

1. **Separação de Responsabilidades**
   - Kermartin: Coleta
   - Genesys: Consulta e Automação

2. **Manutenibilidade**
   - Código mais simples
   - Menos dependências
   - Menos pontos de falha

3. **Performance**
   - Dados já coletados são mais rápidos
   - Cache natural do Kermartin
   - Menos requisições externas

4. **Confiabilidade**
   - Dados validados pelo Kermartin
   - Menos erros de scraping
   - Base de dados consolidada

---

## 📞 Próximos Passos

1. **Revisar código atual** e identificar todos os pontos de extração
2. **Criar issues** para cada refatoração necessária
3. **Implementar mudanças** seguindo o padrão recomendado
4. **Testar** todas as funcionalidades após refatoração
5. **Documentar** novas integrações com Kermartin

---

**Última atualização:** 2025-10-31

