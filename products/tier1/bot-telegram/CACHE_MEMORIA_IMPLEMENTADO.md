# ✅ Sistema de Cache e Monitoramento de Memória - Implementado

## 🎯 Objetivo

Implementar sistema de cache em memória e monitoramento de uso de memória para melhorar performance e evitar vazamentos.

---

## ✅ Implementações Realizadas

### 1. **CacheService** (`src/services/cache_service.py`)

#### **Características:**
- ✅ **Thread-safe** - Usa `threading.RLock()` para acesso seguro
- ✅ **TTL configurável** - Tempo de vida por tipo de dado
- ✅ **Limite de memória** - Máximo de 100 MB configurável
- ✅ **Limpeza automática** - Remove entradas expiradas a cada 5 minutos
- ✅ **Evicção inteligente** - Remove entradas menos usadas quando memória cheia
- ✅ **Estatísticas completas** - Hits, misses, taxa de acerto, uso de memória

#### **TTL por Tipo:**
```python
'processo': 3600 segundos (1 hora)      # Processos não mudam muito
'magistrado': 86400 segundos (24 horas) # Perfis são estáveis
'jurisprudencia': 1800 segundos (30 min) # Pode ter atualizações
'default': 3600 segundos (1 hora)
```

#### **Limite de Memória:**
- Máximo: **100 MB** (configurável)
- Quando cheio: Remove entradas expiradas primeiro
- Se ainda cheio: Remove entradas menos usadas (evicção)

---

### 2. **Integração com CNJService**

#### **Fluxo de Cache:**
```
1. Consulta processo
   ↓
2. Verifica cache PRIMEIRO ✅
   ↓ Se encontrou → Retorna imediatamente
   ↓ Se não encontrou → Continua
3. Verifica Kermartin
   ↓ Se encontrou → Armazena no cache e retorna
4. Consulta API CNJ
   ↓ Se encontrou → Armazena no cache (TTL menor) e retorna
```

#### **Benefícios:**
- ✅ **Performance**: Consultas repetidas são instantâneas
- ✅ **Redução de requisições**: Menos chamadas à API CNJ
- ✅ **Menos carga no Kermartin**: Consultas em memória primeiro
- ✅ **Melhor experiência**: Respostas mais rápidas

---

### 3. **Comando `/cache`**

Novo comando para ver estatísticas de cache e memória:

```
/cache
```

**Mostra:**
- Entradas no cache
- Hits e misses
- Taxa de acerto (%)
- Evicções
- Uso de memória (MB)
- Memória do processo (RSS, VMS) - se psutil disponível

---

### 4. **Monitoramento de Memória**

#### **Com `psutil` (recomendado):**
- ✅ RSS (Resident Set Size) - Memória física usada
- ✅ VMS (Virtual Memory Size) - Memória virtual total
- ✅ Uso do cache em MB
- ✅ Número de entradas

#### **Sem `psutil`:**
- ✅ Informações básicas do cache
- ✅ Aviso para instalar psutil

---

## 📊 Resultados dos Testes

### **Teste Executado:**
```bash
python3 test_cache_memory.py
```

### **Resultados:**
- ✅ Cache armazena e recupera corretamente
- ✅ Cache miss funciona
- ✅ TTL e expiração funcionam
- ✅ Integração com CNJ Service funciona
- ✅ Estatísticas funcionam
- ✅ Monitoramento de memória funciona

### **Estatísticas Observadas:**
- Taxa de acerto inicial: **40%** (esperado com poucos dados)
- Memória usada: **0.0 MB** (cache pequeno)
- RSS: **61.79 MB** (processo leve)
- VMS: **167.27 MB** (memória virtual)

---

## 🔧 Configuração

### **Instalar Dependências:**
```bash
pip install psutil>=5.9.0
```

Ou usando requirements.txt:
```bash
pip install -r src/requirements.txt
```

### **Ajustar Limite de Memória:**

Editar `cache_service.py`:
```python
MAX_MEMORY_MB = 100  # Alterar conforme necessário
```

### **Ajustar TTL:**

Editar `cache_service.py`:
```python
DEFAULT_TTL = {
    'processo': 3600,      # Alterar conforme necessário
    'magistrado': 86400,
    'jurisprudencia': 1800,
    'default': 3600
}
```

---

## 📈 Melhorias de Performance Esperadas

### **Antes (sem cache):**
- Cada consulta faz requisição completa
- Tempo médio: ~500-2000ms por consulta
- Requisições repetidas são lentas

### **Depois (com cache):**
- Consultas repetidas são instantâneas (< 10ms)
- Redução de ~80-90% em requisições para processos já consultados
- Melhor experiência do usuário

---

## 🛡️ Proteções Implementadas

1. **Limite de Memória**
   - Máximo de 100 MB
   - Evicção automática quando cheio

2. **Thread-Safe**
   - Uso de locks para acesso seguro
   - Suporta múltiplas requisições simultâneas

3. **Limpeza Automática**
   - Remove entradas expiradas a cada 5 minutos
   - Previne crescimento infinito do cache

4. **Graceful Degradation**
   - Funciona mesmo sem psutil
   - Cache continua funcionando se monitoramento falhar

---

## 📝 Uso

### **Para Desenvolvedores:**

```python
from services.cache_service import cache_service

# Armazenar
cache_service.set("chave", dados, cache_type='processo')

# Recuperar
dados = cache_service.get("chave", cache_type='processo')

# Estatísticas
stats = cache_service.get_stats()
memory = cache_service.get_memory_info()
```

### **Para Usuários:**

```
/cache - Ver estatísticas de cache e memória
```

---

## 🔍 Monitoramento

### **Métricas Importantes:**

1. **Taxa de Acerto (Hit Rate)**
   - Ideal: > 60%
   - Se < 40%: Cache pode estar muito pequeno ou TTL muito curto

2. **Uso de Memória**
   - Ideal: < 80% do limite
   - Se > 90%: Considerar aumentar limite ou reduzir TTL

3. **Evicções**
   - Se muito alto: Cache está muito pequeno para o uso
   - Considerar aumentar limite de memória

---

## ✅ Checklist de Implementação

- [x] CacheService criado
- [x] Integração com CNJService
- [x] Comando /cache implementado
- [x] Monitoramento de memória
- [x] Testes realizados
- [x] Documentação criada
- [x] psutil adicionado ao requirements.txt

---

## 🚀 Próximos Passos (Opcional)

1. **Cache Distribuído**
   - Implementar Redis para cache compartilhado entre instâncias
   - Melhor para múltiplos bots

2. **Cache Persistente**
   - Salvar cache em disco para sobreviver reinicializações
   - Útil para processos consultados frequentemente

3. **Métricas Avançadas**
   - Exportar métricas para Prometheus/Grafana
   - Alertas quando memória alta

---

**Implementado em:** 2025-10-31  
**Status:** ✅ **PRONTO PARA PRODUÇÃO**

