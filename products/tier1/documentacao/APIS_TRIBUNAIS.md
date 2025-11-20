# 📡 APIs de Tribunais - Pesquisa e Análise

## 🎯 APIs Públicas Disponíveis

### 1. **API Pública do CNJ (DataJud)** ⭐ RECOMENDADA

**URL:** https://www.cnj.jus.br/sistemas/datajud/api-publica/

**Status:** ✅ **OFICIAL E GRATUITA**

**O que oferece:**
- ✅ Acesso público aos metadados de processos judiciais
- ✅ Dados de **todo o Brasil**
- ✅ Base Nacional de Dados do Poder Judiciário (DataJud)
- ✅ Gratuita e oficial do CNJ

**Características:**
- 🔓 **Acesso:** Público (precisa de cadastro/credenciais?)
- 📊 **Dados:** Metadados de processos (não conteúdo completo)
- 🔄 **Atualização:** Não em tempo real (há delays)
- 📚 **Documentação:** Disponível no site do CNJ

**Limitações conhecidas:**
- ⚠️ Dados podem não estar em tempo real
- ⚠️ Metadados apenas (não movimentações detalhadas)
- ⚠️ Pode exigir cadastro/autenticação

**Documentação:**
- Wiki: https://datajud-wiki.cnj.jus.br/api-publica/

**Exemplo de uso:**
```python
# Consulta por número CNJ
GET /api/publica/processos/{numero_cnj}
```

---

### 2. **APIs de Tribunais Individuais**

Alguns tribunais têm APIs próprias, mas são **limitadas e fragmentadas**:

#### STF (Supremo Tribunal Federal)
- ❌ Não há API pública conhecida
- ⚠️ Apenas consultas web

#### STJ (Superior Tribunal de Justiça)
- ❌ Não há API pública conhecida
- ⚠️ Portal de consulta web disponível

#### Tribunais Estaduais (TJ)
- ⚠️ Cada tribunal tem seu sistema (e-SAJ, eProc)
- ⚠️ **Não há padronização**
- ⚠️ Maioria não oferece API pública

---

## 💼 APIs Privadas/Pagas

### 1. **Judit.io**

**URL:** https://judit.io/

**Status:** 💰 **PAGA**

**O que oferece:**
- ✅ Consulta processual em tempo real
- ✅ Acesso direto a tribunais
- ✅ API documentada (Swagger)
- ✅ Consulta por CPF, CNPJ, OAB, número CNJ
- ✅ Andamentos e partes em tempo real

**Preços:**
- 💰 Modelo pago (precisa consultar)
- 📊 Pay-per-use ou planos

**Vantagens:**
- ✅ Tempo real
- ✅ Dados completos
- ✅ Múltiplos tribunais

**Desvantagens:**
- ❌ Paga
- ❌ Terceiro (não oficial)

---

### 2. **Jusbrasil API**

**Status:** ⚠️ **NÃO É API PÚBLICA**

- ❌ Não oferece API pública
- ✅ Tem portal de consulta web
- ✅ Notificações de atualizações (via web)

---

## 🔍 Alternativas: Web Scraping

### Por que considerar:
- ✅ Gratuito
- ✅ Acesso a dados públicos
- ⚠️ Mais complexo de implementar
- ⚠️ Fragil (quebras quando site muda)
- ⚠️ Pode violar termos de uso

### Ferramentas possíveis:
- **Selenium** - Automação de navegador
- **BeautifulSoup** - Parsing HTML
- **Requests** - HTTP requests

### Riscos:
- ⚠️ Captcha e anti-bot
- ⚠️ Rate limiting
- ⚠️ Mudanças frequentes nos sites
- ⚠️ Termos de uso podem proibir

---

## 📊 Comparação Rápida

| Solução | Tipo | Custo | Tempo Real | Dados | Estabilidade |
|---------|------|-------|------------|-------|--------------|
| **API CNJ** | Pública | Grátis | ❌ Delay | Metadados | ✅ Estável |
| **Judit.io** | Privada | Paga | ✅ Sim | Completo | ✅ Estável |
| **Web Scraping** | Alternativa | Grátis | ⚠️ Variável | Completo | ❌ Frágil |
| **e-SAJ/eProc** | Direto | Grátis | ✅ Sim | Completo | ⚠️ Fragmentado |

---

## 🎯 Recomendação para o Projeto

### **FASE 1: API CNJ (Gratuita)**
**Para:** Consulta básica de processos

**Implementar:**
```python
# Consulta metadados via API CNJ
- Número do processo
- Tribunal
- Status básico
- Data de entrada
```

**Limitações aceitas:**
- Não terá movimentações detalhadas
- Dados podem ter delay
- Apenas metadados

### **FASE 2: Web Scraping (Se necessário)**
**Para:** Movimentações detalhadas e tempo real

**Implementar:**
- Scraping de e-SAJ/eProc por tribunal
- Consulta periódica
- Cache de resultados

**Desvantagens:**
- Complexo
- Manutenção constante
- Pode quebrar

### **FASE 3: API Paga (Se escalar)**
**Para:** Produção confiável

**Considerar:**
- Judit.io ou similar
- Garantia de uptime
- Suporte

---

## 🔧 Exemplo de Integração com API CNJ

```python
import requests

class CNJAPI:
    BASE_URL = "https://api.cnj.jus.br/processos"
    
    def consultar_processo(self, numero_cnj: str):
        """
        Consulta processo pela API CNJ
        
        Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
        Exemplo: 0001234-56.2024.8.26.0100
        """
        url = f"{self.BASE_URL}/{numero_cnj}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao consultar processo: {e}")
            return None
```

---

## 📚 Links Úteis

### Oficiais
- [API Pública CNJ](https://www.cnj.jus.br/sistemas/datajud/api-publica/)
- [Wiki DataJud](https://datajud-wiki.cnj.jus.br/api-publica/)
- [Portal CNJ](https://www.cnj.jus.br/)

### Privadas
- [Judit.io API](https://judit.io/api)
- [Jusbrasil Consulta](https://www.jusbrasil.com.br/consulta-processual/)

---

## ⚠️ Considerações Legais

### Web Scraping:
- ✅ Dados públicos são legais de acessar
- ⚠️ Verificar termos de uso de cada site
- ⚠️ Respeitar rate limits
- ⚠️ Não sobrecarregar servidores

### APIs Públicas:
- ✅ Uso permitido conforme documentação
- ✅ Seguir limites de rate
- ✅ Respeitar termos de uso

---

## 🚀 Próximos Passos

1. **Testar API CNJ:**
   - Verificar documentação completa
   - Testar endpoints disponíveis
   - Verificar necessidade de autenticação

2. **Avaliar necessidades:**
   - Precisamos de tempo real?
   - Precisamos de movimentações detalhadas?
   - Qual o volume de consultas?

3. **Decidir abordagem:**
   - API CNJ (gratuita) para começar
   - Web scraping (se necessário)
   - API paga (se escalar)

---

**Status da Pesquisa:** ✅ **API PÚBLICA OFICIAL ENCONTRADA**

**Recomendação:** Começar com **API CNJ (DataJud)** - gratuita e oficial, mesmo com limitações.

