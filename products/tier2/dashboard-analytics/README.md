# 📊 Dashboard Analítico - Genesys

Dashboard de BI e analytics para escritórios jurídicos.

## 🚀 Funcionalidades

- ✅ KPIs em tempo real
- ✅ Gráficos interativos
- ✅ Relatórios automáticos
- ✅ Alertas inteligentes
- ✅ Exportação de dados
- ✅ Múltiplas visualizações

## 🏗️ Arquitetura METHOD-BMAD

### B - Backend
- FastAPI
- PostgreSQL
- Redis (cache)
- Pandas (análise)

### M - Modelo
1. Data Aggregator - Agregação de dados
2. KPI Calculator - Cálculo de métricas
3. Report Generator - Geração de relatórios
4. Visualization Engine - Gráficos

### A - API
- `GET /api/kpis` - Listar KPIs
- `GET /api/kpis/:name` - KPI específico
- `GET /api/charts` - Dados para gráficos
- `GET /api/reports` - Listar relatórios
- `POST /api/reports/generate` - Gerar relatório

### D - Data
- KPIs, Reports
- Analytics data, Alerts

## 🚀 Quick Start

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Ambiente

```bash
cp env.example .env
nano .env
```

### 3. Iniciar Dashboard

```bash
python src/app.py
```

### 4. Acessar Dashboard

```bash
http://localhost:8002/api/kpis
```

## 📊 Endpoints

### KPIs
```bash
GET /api/kpis?time_window=30d
GET /api/kpis/total_revenue?time_window=7d
```

### Charts
```bash
GET /api/charts?chart_type=revenue_trend&time_window=30d
GET /api/charts?chart_type=process_status
```

### Reports
```bash
GET /api/reports
POST /api/reports/generate?report_type=daily_summary
```

## 📈 KPIs Disponíveis

- Total Receita
- Total de Processos
- Prazos Vencidos
- Prazos Hoje
- Taxa de Conversão
- Tempo Médio de Resposta
- Satisfação do Cliente
- CPU/Memory Usage
- Usuários Ativos

## 🔐 Segurança

- ✅ Rate limiting
- ✅ HTTPS obrigatório
- ✅ CORS configurado
- ✅ Cache configurável

---

**Desenvolvido por:** Genesys Tecnologia  
**Versão:** 1.0.0

