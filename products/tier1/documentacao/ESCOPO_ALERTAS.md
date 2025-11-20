# 🎯 Escopo dos Alertas - O Que Será Monitorado

## 📋 Tipos de Alertas Planejados

Com base no modelo do banco de dados (`Alerta.tipo`), os alertas devem cobrir **3 tipos principais**:

---

## 1. 📅 **ALERTAS DE PRAZOS** ✅ IMPLEMENTADO PARCIALMENTE

**Tipo:** `'prazo'`

**O que monitora:**
- ⏰ Prazos processuais vencendo
- 📋 Tipos: Contestação, Recursos, Embargos, etc.
- 🏛️ Por tribunal/processo
- ⚠️ Níveis de urgência: 1, 3, 7 dias antes

**Estado Atual:**
- ✅ Interface `/alerta` funcionando
- ✅ Scheduler automático existe (`automacao-prazos/src/scheduler.py`)
- ✅ Notificações por Telegram/Email/WhatsApp
- ❌ Preferências do usuário não são salvas ainda

**Exemplos de Alerta:**
```
🔴 URGENTE: Prazo Vencendo Hoje!
📄 Processo: 0001234-56.2024.8.26.0100
📋 Tipo: Contestação
🏛️ Tribunal: TJMG
⏰ Vence em: 02/11/2024 (HOJE!)
```

---

## 2. 🔄 **ALERTAS DE MOVIMENTAÇÕES** ❌ NÃO IMPLEMENTADO

**Tipo:** `'movimentacao'`

**O que deve monitorar:**
- 📝 Novas movimentações em processos monitorados
- 🔔 Sentenças publicadas
- 📤 Intimações recebidas
- ⚡ Decisões importantes
- 📊 Mudanças de status do processo
- 🏛️ Publicações em diários oficiais

**Estado Atual:**
- ❌ Não implementado
- ❌ Não há integração com APIs de tribunais
- ❌ Não há monitoramento de processos específicos

**Exemplos Futuros de Alerta:**
```
🔄 Nova Movimentação Detectada!
📄 Processo: 0001234-56.2024.8.26.0100
📝 Tipo: Sentença Publicada
📅 Data: 02/11/2024
💡 Verifique detalhes no sistema
```

---

## 3. 📚 **ALERTAS LEGISLATIVOS** ❌ NÃO IMPLEMENTADO

**Tipo:** `'legislativo'`

**O que deve monitorar:**
- 📜 Novas leis publicadas (Diário Oficial)
- 🔄 Alterações em legislações relevantes
- 📊 Mudanças em súmulas/jurisprudência
- ⚖️ Decisões importantes de tribunais superiores (STF, STJ)
- 📋 Novas portarias/resoluções

**Estado Atual:**
- ❌ Não implementado
- ❌ Não há integração com fontes legislativas
- ❌ Não há monitoramento de mudanças legais

**Exemplos Futuros de Alerta:**
```
📚 Nova Legislação Publicada!
📜 Lei 14.XXX/2024 - Alterações na CLT
📅 Publicado em: 01/11/2024
🔗 Link: [Diário Oficial]
💡 Relevante para seu perfil trabalhista
```

---

## 🎯 Situação Atual

### O Que Funciona AGORA:
```
✅ Prazos Processuais
   └─ Scheduler verifica automaticamente
   └─ Envia alertas por Telegram/Email
   └─ 3 níveis de urgência (1, 3, 7 dias)
```

### O Que NÃO Funciona:
```
❌ Movimentações de Processos
   └─ Precisa integração com APIs de tribunais
   └─ Precisa sistema de monitoramento de processos
   
❌ Alertas Legislativos
   └─ Precisa integração com Diário Oficial
   └─ Precisa sistema de análise de relevância
```

---

## 🤔 Dúvida: Qual é o Foco?

### **OPÇÃO 1: Apenas Prazos (Foco Atual)**
**Vantagens:**
- ✅ Já está parcialmente implementado
- ✅ Mais simples e direto
- ✅ Alto valor para usuários

**Limitações:**
- Apenas notifica sobre vencimentos
- Não monitora mudanças nos processos

### **OPÇÃO 2: Prazos + Movimentações (Recomendado)**
**Vantagens:**
- 📋 Cobertura completa de processos
- 🔄 Notifica sobre mudanças importantes
- ⚡ Mais valor agregado

**Requisitos:**
- Integração com APIs de tribunais (e-SAJ, eProc)
- Sistema de monitoramento de processos específicos
- Web scraping ou APIs pagas

### **OPÇÃO 3: Tudo (Prazos + Movimentações + Legislativo)**
**Vantagens:**
- 🎯 Solução completa
- 📚 Monitora ambiente jurídico completo
- 💎 Alto valor premium

**Requisitos:**
- Desenvolvimento complexo
- Múltiplas integrações
- Custos com APIs/scraping
- Processamento de dados em grande volume

---

## 💡 Recomendação

### **FASE 1 (Atual): Prazos Processuais** ✅
- Focar em completar salvamento de preferências
- Melhorar interface de configuração
- Estabilizar sistema de notificações

### **FASE 2 (Futuro): Movimentações** 📋
- Adicionar comando `/processo` funcional
- Criar sistema de monitoramento de processos
- Integrar com APIs de tribunais (quando disponível)

### **FASE 3 (Longo Prazo): Legislativo** 📚
- Monitoramento de Diário Oficial
- Alertas sobre mudanças relevantes
- Análise de relevância por área do direito

---

## 📊 Comparação Visual

| Tipo | Status | Prioridade | Complexidade | Valor |
|------|--------|------------|--------------|-------|
| **Prazos** | ⚠️ Parcial | 🔴 Alta | 🟢 Baixa | ⭐⭐⭐⭐⭐ |
| **Movimentações** | ❌ Não | 🟡 Média | 🟡 Média | ⭐⭐⭐⭐ |
| **Legislativo** | ❌ Não | 🟢 Baixa | 🔴 Alta | ⭐⭐⭐ |

---

## ❓ Para Você Decidir

1. **Os alertas devem ser APENAS para prazos?**
   - Foco: vencimentos de prazos processuais
   - Mais simples, implementação rápida

2. **Ou também para MOVIMENTAÇÕES de processos?**
   - Foco: notificar sobre novas movimentações
   - Requer integração com tribunais

3. **E alertas LEGISLATIVOS?**
   - Foco: mudanças em leis/jurisprudência
   - Mais complexo, baixa prioridade inicial

**Recomendação:** Começar focando em **PRAZOS** (completando o que falta) e depois expandir para **MOVIMENTAÇÕES** quando tiver integração com tribunais.

---

**Status Atual:** Alertas focados em **PRAZOS PROCESSUAIS** apenas  
**Próximo Passo:** Completar salvamento de preferências e expandir conforme decisão

