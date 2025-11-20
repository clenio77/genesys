# 🤖 Assistente Virtual e Automação de Prazos - TIER 1

**Data:** 2025-01-27  
**Status:** ⚠️ **IMPLEMENTAÇÃO PARCIAL** | 📋 **ARQUITETURA DEFINIDA**

---

## 📊 Visão Geral

O **TIER 1** da Genesys Tecnologia é composto por **3 produtos principais**:

1. **Bot Telegram Jurídico** ✅ (100% implementado)
2. **Automação de Prazos Processuais** ⚠️ (60% implementado)
3. **Assistente Virtual 24/7** ⚠️ (40% implementado)

---

## 🤖 ASSISTENTE VIRTUAL 24/7

### 📋 **O Que É?**

Assistente de chat inteligente que pode ser **embutido em sites** ou usado como **widget standalone** para:
- Atendimento 24/7 automático
- Qualificação de leads
- FAQ inteligente
- Agendamento de reuniões
- Suporte ao cliente

### 🏗️ **Arquitetura Atual**

```
assistente-virtual/
├── src/
│   ├── chatbot.py          # FastAPI + WebSocket
│   ├── qualifier.py        # Qualificação de leads
│   └── __init__.py
└── requirements.txt
```

### ✅ **O Que Já Está Implementado**

#### 1. **Infraestrutura Base**
- ✅ FastAPI como framework web
- ✅ WebSocket para chat em tempo real
- ✅ API REST alternativa
- ✅ CORS configurado
- ✅ Middleware de segurança
- ✅ Integração com banco de dados (salva conversas)

#### 2. **Chat em Tempo Real**
- ✅ Conexão WebSocket (`/ws/{user_id}`)
- ✅ Gerenciamento de conexões ativas
- ✅ Mensagens de boas-vindas
- ✅ Persistência de conversas no banco

#### 3. **Qualificação de Leads**
- ✅ Classe `LeadQualifier` implementada
- ✅ Score automático baseado em palavras-chave
- ✅ Extração de informações (email, telefone, empresa)
- ✅ Classificação: alta/média/baixa prioridade

#### 4. **Processamento Básico**
- ✅ Respostas pré-definidas para perguntas comuns
- ✅ Integração com banco de dados
- ✅ Logs estruturados

### ⚠️ **O Que Falta Implementar**

#### 1. **Integração com IA**
- ❌ Usar LLM (Gemini/OpenAI) para respostas inteligentes
- ❌ Contexto jurídico do Kermartin
- ❌ Memória de conversação
- ❌ Personalização por tipo de usuário

#### 2. **Funcionalidades Avançadas**
- ❌ Agendamento real de reuniões (integração com calendário)
- ❌ Envio de emails automáticos
- ❌ Integração com CRM
- ❌ Analytics e métricas de conversão

#### 3. **Widget para Site**
- ❌ Componente React/Vue para embed
- ❌ Estilização profissional
- ❌ Responsivo mobile
- ❌ Multi-idioma

### 🎯 **Como Deveria Funcionar**

#### **Fluxo Completo:**

```
1. Usuário acessa site → Widget do assistente aparece
2. Usuário envia mensagem → WebSocket envia para backend
3. Backend processa com IA:
   - Analisa intenção
   - Busca contexto no Kermartin (se jurídico)
   - Gera resposta inteligente
   - Qualifica lead automaticamente
4. Resposta enviada → Widget exibe resposta
5. Se lead qualificado → Notifica equipe de vendas
```

#### **Integração com Kermartin:**

```python
# Quando pergunta jurídica é detectada
if is_legal_question(user_message):
    # Buscar no Kermartin
    contexto = kermartin_service.buscar_jurisprudencia(user_message)
    
    # Gerar resposta com contexto
    resposta = ai_service.responder_com_contexto(
        pergunta=user_message,
        contexto_kermartin=contexto
    )
```

#### **Qualificação de Leads:**

```python
# Durante conversa
qualifier = LeadQualifier()
score = qualifier.analisar_conversa(mensagens)

if score >= 70:
    # Lead quente - notificar vendas
    notificar_vendas(lead_info)
    
    # Oferecer demo ou reunião
    resposta += "\n\n💡 Gostaria de agendar uma demo? Digite 'agendar'"
```

### 📊 **Métricas e Analytics**

**Dados a coletar:**
- Total de conversas iniciadas
- Taxa de conversão (lead qualificado)
- Tempo médio de resposta
- Satisfação do usuário
- Assuntos mais perguntados
- Horários de pico

---

## 📅 AUTOMAÇÃO DE PRAZOS PROCESSUAIS

### 📋 **O Que É?**

Sistema automatizado que:
- Monitora prazos processuais de múltiplos processos
- Calcula automaticamente datas de vencimento
- Envia alertas proativos (7, 3, 1 dia antes)
- Integra com processos do Kermartin
- Fornece dashboard de controle

### 🏗️ **Arquitetura Atual**

```
automacao-prazos/
├── src/
│   ├── scheduler.py       # APScheduler - tarefas agendadas
│   ├── notifier.py        # Sistema de notificações
│   ├── api.py             # API REST FastAPI
│   └── __init__.py
└── requirements.txt
```

### ✅ **O Que Já Está Implementado**

#### 1. **Scheduler Automático**
- ✅ APScheduler configurado
- ✅ Verificação a cada 6 horas
- ✅ Verificação urgente a cada hora
- ✅ Background scheduler rodando continuamente

#### 2. **Sistema de Notificações**
- ✅ Estrutura para Email, Telegram, WhatsApp
- ✅ Níveis de urgência (crítica, alta, normal)
- ✅ Registro de notificações no banco
- ✅ Mensagens formatadas por canal

#### 3. **API REST Completa**
- ✅ Criar prazos (`POST /prazos/`)
- ✅ Listar prazos (`GET /prazos/`)
- ✅ Obter prazo específico (`GET /prazos/{id}`)
- ✅ Concluir prazo (`PATCH /prazos/{id}/concluir`)
- ✅ Estatísticas (`GET /estatisticas/`)
- ✅ Rate limiting
- ✅ Cache Redis
- ✅ CORS seguro

#### 4. **Funcionalidades**
- ✅ Cálculo automático de dias restantes
- ✅ Filtros por status
- ✅ Estatísticas por usuário
- ✅ Persistência no banco

### ⚠️ **O Que Falta Implementar**

#### 1. **Integração com Kermartin** 🔥 **PRIORIDADE MÁXIMA**
- ❌ Extrair prazos automaticamente de processos coletados
- ❌ Calcular prazos baseado em movimentações
- ❌ Sincronizar com processos monitorados
- ❌ Detectar novos prazos automaticamente

#### 2. **Notificações Reais**
- ❌ Envio real de emails (SMTP configurado)
- ❌ Integração com Telegram Bot API
- ❌ Integração com WhatsApp Business API
- ❌ Templates profissionais de mensagens

#### 3. **Dashboard Web**
- ❌ Interface visual para gerenciar prazos
- ❌ Gráficos e estatísticas
- ❌ Filtros avançados
- ❌ Exportação de relatórios

#### 4. **Funcionalidades Avançadas**
- ❌ Integração com calendário (Google Calendar, Outlook)
- ❌ Alertas via SMS
- ❌ Lembretes múltiplos personalizáveis
- ❌ Delegar prazos para outros usuários

### 🎯 **Como Deveria Funcionar**

#### **Fluxo Completo:**

```
1. Kermartin coleta processo → Extrai movimentações
2. Sistema analisa movimentações → Identifica prazos
3. Calcula datas de vencimento → Salva no banco
4. Scheduler verifica periodicamente → Detecta prazos próximos
5. Envia alertas proativos → Email, Telegram, WhatsApp
6. Usuário recebe notificação → Visualiza no dashboard
7. Usuário cumpre prazo → Marca como concluído
```

#### **Integração com Kermartin:**

```python
# Quando processo é coletado/atualizado no Kermartin
def sincronizar_prazos_kermartin(user_id: int, processo_numero: str):
    # Buscar processo no Kermartin
    processo = kermartin_service.buscar_processo_por_numero(processo_numero)
    
    # Extrair movimentações
    movimentacoes = processo.get('movimentacoes', [])
    
    # Analisar cada movimentação
    for mov in movimentacoes:
        # Detectar tipo de prazo
        tipo_prazo = detectar_tipo_prazo(mov['tipo'])
        
        if tipo_prazo:
            # Calcular data de vencimento
            data_vencimento = calcular_vencimento(
                tipo=tipo_prazo,
                data_movimentacao=mov['data']
            )
            
            # Criar ou atualizar prazo
            criar_ou_atualizar_prazo(
                user_id=user_id,
                processo=processo_numero,
                tipo=tipo_prazo,
                data_vencimento=data_vencimento
            )
```

#### **Cálculo Automático de Prazos:**

```python
def calcular_vencimento(tipo: str, data_movimentacao: date) -> date:
    """
    Calcula data de vencimento baseado no tipo de prazo
    """
    regras = {
        'contestacao': timedelta(days=15),  # 15 dias úteis
        'recurso': timedelta(days=15),
        'embargos': timedelta(days=15),
        'agravo': timedelta(days=10),
        'intimacao': timedelta(days=5),
        # ... mais regras
    }
    
    prazo_dias = regras.get(tipo.lower(), timedelta(days=15))
    
    # Adicionar dias úteis (excluindo fins de semana e feriados)
    return adicionar_dias_uteis(data_movimentacao, prazo_dias)
```

### 📊 **Sistema de Alertas**

#### **Níveis de Urgência:**

```
🔴 CRÍTICO (≤1 dia)
   → Email + Telegram + WhatsApp + SMS
   → Notificação a cada hora
   
🟡 ALTO (2-3 dias)
   → Email + Telegram
   → Notificação diária
   
🟢 NORMAL (4-7 dias)
   → Email apenas
   → Notificação a cada 2 dias
   
⚪ BAIXO (>7 dias)
   → Email semanal
```

#### **Preferências do Usuário:**

```python
# Configurado via /alerta no bot-telegram
{
    "canal": "telegram",  # email, telegram, whatsapp
    "intervalo_dias": 3,   # 7, 3, 1
    "horario_preferido": "09:00",
    "dias_semana": [0,1,2,3,4]  # Segunda a Sexta
}
```

---

## 🔗 INTEGRAÇÃO ENTRE COMPONENTES

### **Como os 3 Produtos Trabalham Juntos:**

```
┌─────────────────────────────────────────────┐
│          KERMARTIN (Base de Dados)          │
│  • Processos coletados                     │
│  • Movimentações extraídas                 │
│  • Jurisprudência                          │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌──────────────┐  ┌──────────────┐
│ Bot Telegram│  │ Automação    │
│              │  │ Prazos       │
│ • Consultas  │  │              │
│ • Alertas    │◄─┤ • Monitora   │
│ • Busca      │  │ • Notifica   │
└──────────────┘  └──────────────┘
       │
       ▼
┌──────────────┐
│ Assistente   │
│ Virtual      │
│              │
│ • FAQ        │
│ • Qualifica  │
│ • Agenda     │
└──────────────┘
```

### **Fluxo de Dados:**

1. **Kermartin coleta processo** → Salva no banco
2. **Automação de Prazos detecta** → Extrai prazos automaticamente
3. **Bot Telegram consulta** → Busca processos do Kermartin
4. **Assistente Virtual responde** → Usa dados do Kermartin quando jurídico

---

## 🚀 IMPLEMENTAÇÃO RECOMENDADA

### **Fase 1: Automação de Prazos (Prioridade Alta)**

#### **Semana 1-2:**
1. ✅ Integrar extração de prazos do Kermartin
2. ✅ Implementar cálculo automático de vencimentos
3. ✅ Configurar envio real de emails
4. ✅ Integrar com bot-telegram para notificações

#### **Semana 3-4:**
5. ✅ Dashboard web básico
6. ✅ Integração com WhatsApp
7. ✅ Calendário integrado
8. ✅ Relatórios e estatísticas

### **Fase 2: Assistente Virtual (Prioridade Média)**

#### **Semana 5-6:**
1. ✅ Integrar LLM (Gemini/OpenAI)
2. ✅ Conectar com Kermartin para contexto jurídico
3. ✅ Melhorar qualificação de leads
4. ✅ Widget React para sites

#### **Semana 7-8:**
5. ✅ Agendamento real de reuniões
6. ✅ Integração com CRM
7. ✅ Analytics completo
8. ✅ Multi-idioma

---

## 📁 Estrutura de Arquivos Proposta

```
tier1/
├── assistente-virtual/
│   ├── src/
│   │   ├── chatbot.py          # ✅ Implementado (básico)
│   │   ├── qualifier.py        # ✅ Implementado
│   │   ├── ai_service.py       # ❌ Fazer: Integração LLM
│   │   ├── kermartin_client.py # ❌ Fazer: Cliente Kermartin
│   │   └── analytics.py        # ❌ Fazer: Métricas
│   ├── widget/                 # ❌ Fazer: Widget React
│   │   ├── src/
│   │   └── package.json
│   └── requirements.txt
│
├── automacao-prazos/
│   ├── src/
│   │   ├── scheduler.py        # ✅ Implementado
│   │   ├── notifier.py         # ⚠️ Parcial (faltam envios reais)
│   │   ├── api.py              # ✅ Implementado
│   │   ├── kermartin_integration.py # ❌ Fazer: Integração Kermartin
│   │   ├── prazo_calculator.py # ❌ Fazer: Cálculo automático
│   │   └── dashboard/          # ❌ Fazer: Dashboard web
│   │       ├── static/
│   │       └── templates/
│   └── requirements.txt
│
└── shared/                      # ✅ Código compartilhado
    ├── config/
    ├── database/
    └── utils/
```

---

## 🔧 Exemplo de Integração Kermartin → Automação Prazos

```python
# automacao-prazos/src/kermartin_integration.py

from services.kermartin_service import kermartin_service
from .prazo_calculator import PrazoCalculator

class KermartinPrazosIntegration:
    """Integra automação de prazos com processos do Kermartin"""
    
    def sincronizar_processo(self, user_id: int, processo_numero: str):
        """Sincroniza prazos de um processo do Kermartin"""
        
        # Buscar processo no Kermartin
        processo = kermartin_service.buscar_processo_por_numero(processo_numero)
        
        if not processo:
            return
        
        # Extrair movimentações
        movimentacoes = processo.get('movimentacoes', [])
        
        # Calcular prazos de cada movimentação
        calculator = PrazoCalculator()
        
        for mov in movimentacoes:
            # Detectar se gera prazo
            tipo_prazo = calculator.detectar_tipo_prazo(mov)
            
            if tipo_prazo:
                # Calcular vencimento
                data_vencimento = calculator.calcular_vencimento(
                    tipo=tipo_prazo,
                    data_movimentacao=mov['data'],
                    tribunal=processo.get('tribunal')
                )
                
                # Criar prazo no banco
                criar_prazo_automatico(
                    user_id=user_id,
                    processo=processo_numero,
                    tipo=tipo_prazo,
                    data_vencimento=data_vencimento,
                    origem='kermartin'  # Identificar origem
                )
```

---

## 📊 Exemplo de Integração Kermartin → Assistente Virtual

```python
# assistente-virtual/src/kermartin_client.py

from services.kermartin_service import kermartin_service
from services.ia_service import ai_service

class AssistenteComKermartin:
    """Assistente Virtual com contexto do Kermartin"""
    
    async def responder_pergunta_juridica(self, pergunta: str, user_id: int):
        """Responde pergunta jurídica usando dados do Kermartin"""
        
        # Detectar se é pergunta jurídica
        if self._eh_pergunta_juridica(pergunta):
            # Buscar contexto no Kermartin
            contexto = kermartin_service.buscar_jurisprudencia(pergunta)
            
            # Processos relevantes
            processos = kermartin_service.buscar_processos_rag({
                'assunto': self._extrair_assunto(pergunta)
            })
            
            # Gerar resposta com IA + contexto
            resposta = await ai_service.responder_com_contexto(
                pergunta=pergunta,
                contexto_jurisprudencia=contexto,
                processos_relevantes=processos[:5]
            )
            
            return resposta
        else:
            # Pergunta geral - usar IA normal
            return await ai_service.process_message(pergunta)
```

---

## 🎯 Próximos Passos Recomendados

### **Curto Prazo (2 semanas):**

1. **Automação de Prazos:**
   - ✅ Integrar extração de prazos do Kermartin
   - ✅ Implementar cálculo automático
   - ✅ Configurar envio real de emails
   - ✅ Conectar com bot-telegram

2. **Assistente Virtual:**
   - ✅ Integrar LLM para respostas inteligentes
   - ✅ Conectar com Kermartin para contexto jurídico
   - ✅ Melhorar qualificação de leads

### **Médio Prazo (1 mês):**

3. **Dashboard Web para Prazos**
4. **Widget React para Assistente**
5. **Integrações externas (WhatsApp, CRM)**

---

## ✅ Conclusão

**Status Atual:**
- ✅ Infraestrutura base implementada
- ✅ APIs funcionais
- ⚠️ Faltam integrações com Kermartin
- ⚠️ Faltam funcionalidades avançadas

**Potencial:**
- 🚀 Alto impacto quando integrado com Kermartin
- 💰 Grande valor para usuários
- 📈 Escalável e modular

**Próximo Passo:** Implementar integração Kermartin → Automação de Prazos

---

**Documentação criada em:** 2025-01-27  
**Status:** 📋 **ARQUITETURA DEFINIDA - PRONTO PARA IMPLEMENTAÇÃO**

