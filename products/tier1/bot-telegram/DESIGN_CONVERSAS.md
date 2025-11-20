# 🎨 Design das Conversas no Bot - Resumo

## 📊 Padrão de Design Implementado

Todas as mensagens do bot seguem um padrão profissional consistente usando o `MessageFormatter`:

### **Estrutura Padrão:**

```
┌─────────────────────────────────────────┐
│ 👨‍⚖️ PERFIL DO MAGISTRADO             │
│ ═══════════════════════════════════════ │
│                                         │
│ 👨‍⚖️ Identificação                    │
│    👤 Nome: **Nome do Magistrado**     │
│    🏛️ Tribunal: TJMG                  │
│    🏛️ Comarca: Uberlândia              │
│    ⚖️ Vara: 1ª Vara Criminal          │
│                                         │
│ ─────────────────────────────────────── │
│                                         │
│ 📊 Estatísticas                         │
│    📊 Total de julgados: **45**        │
│    • Taxa de condenação: **78%** (35)  │
│    • Taxa de absolvição: **22%** (10)  │
│                                         │
│ ─────────────────────────────────────── │
│                                         │
│ 📋 Crimes Mais Julgados                 │
│    • Homicídio qualificado: 30 (67%)   │
│    • Roubo qualificado: 15 (33%)        │
│                                         │
│ ─────────────────────────────────────── │
│                                         │
│ 📋 Últimas Decisões                     │
│    1. `0001234-56.2024.8.13.0702`     │
│       🔴 Condenação                     │
│       📅 2024-10-15                    │
│                                         │
│ ─────────────────────────────────────── │
│                                         │
│ 💡 Dados fornecidos pela base Kermartin │
└─────────────────────────────────────────┘
```

---

## 🎯 Características do Design

### **1. Hierarquia Visual Clara**
- ✅ **Cabeçalho** com título em negrito e separador forte (`═════`)
- ✅ **Seções** bem definidas com emojis identificadores
- ✅ **Subseções** com indentação consistente
- ✅ **Rodapé** com separador leve (`─────`) e fonte dos dados

### **2. Separadores Visuais**
- `══════════════════════════` - Separador forte (após cabeçalho)
- `──────────────────────────` - Separador leve (entre seções)

### **3. Emojis Padronizados**
- 👨‍⚖️ Magistrado
- 👤 Promotor
- 🏛️ Tribunal/Comarca
- ⚖️ Vara/Processo
- 📊 Estatísticas
- 📋 Listas/Decisões
- 📅 Datas
- ✅ Sucesso
- ⚠️ Aviso
- ❌ Erro
- 💡 Informação

### **4. Formatação Consistente**
- **Negrito** para títulos e valores importantes
- `Código` para números de processos
- Indentação de 3 espaços para subitens
- Listas numeradas com **negrito**
- Emojis no início de cada linha importante

---

## 📝 Comandos Formatados

### **`/magistrado`**
✅ Usa header profissional
✅ Seções bem organizadas
✅ Estatísticas destacadas
✅ Últimas decisões formatadas
✅ Padrões identificados destacados

### **`/promotor`**
✅ Mesmo padrão do `/magistrado`
✅ Header profissional
✅ Seções organizadas
✅ Histórico ou casos formatados

### **`/comarca`**
✅ Header com nome da comarca em maiúsculas
✅ Estatísticas no topo
✅ Lista de processos formatada
✅ Informações truncadas quando necessário

---

## 🔍 Exemplo Visual Completo

### **Comando `/magistrado "Dimas Borges"`**

```
👨‍⚖️ PERFIL DO MAGISTRADO
═══════════════════════════════════════

👨‍⚖️ Identificação
   👤 Nome: **Dimas Borges de Paula**
   🏛️ Tribunal: TJMG
   🏛️ Comarca: Uberlândia
   ⚖️ Vara: 1ª Vara Criminal

───────────────────────────────────────

📊 Estatísticas
   📊 Total de julgados: **45**
   • Taxa de condenação: **78.0%** (35 condenações)
   • Taxa de absolvição: **22.0%** (10 absolvições)

───────────────────────────────────────

📋 Crimes Mais Julgados
   • **Homicídio qualificado**: 30 casos (66.7%)
   • **Roubo qualificado**: 15 casos (33.3%)

───────────────────────────────────────

📋 Últimas Decisões
   1. `0001234-56.2024.8.13.0702`
      🔴 Condenação
      📅 2024-10-15

   2. `0009876-54.2024.8.13.0702`
      🟢 Absolvição
      📅 2024-10-10

───────────────────────────────────────

💡 Padrão Identificado
   Magistrado tende a condenar quando há provas materiais consistentes.

───────────────────────────────────────

💡 Dados fornecidos pela base Kermartin
```

---

## ✅ Benefícios do Design

1. **Legibilidade** - Informações fáceis de escanear
2. **Profissionalismo** - Visual limpo e organizado
3. **Consistência** - Mesmo padrão em todos os comandos
4. **Hierarquia** - Informações importantes destacadas
5. **Branding** - Rodapé identifica a fonte dos dados

---

## 🎨 Cores e Indicadores

- 🔴 **Vermelho** - Condenações
- 🟢 **Verde** - Absolvições
- ⚖️ **Decisões neutras**
- ✅ **Sucesso/Disponível**
- ⚠️ **Aviso**
- ❌ **Erro/Indisponível**

---

**Status:** ✅ **DESIGN PROFISSIONAL IMPLEMENTADO E CONSISTENTE**

