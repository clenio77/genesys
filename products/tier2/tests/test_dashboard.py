"""
Testes unitários para Dashboard Analítico
"""

import pytest
from datetime import datetime, timedelta


class TestDataAggregator:
    """Testes para Data Aggregator"""
    
    def test_collect_from_source(self):
        """Testa coleta de dados de fonte"""
        from dashboard_analytics.src.services.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        data = [{"id": 1, "value": 100}, {"id": 2, "value": 200}]
        
        aggregator.collect_from_source("processos", data)
        
        assert len(aggregator.sources.get("processos", [])) == 2
    
    def test_get_summary(self):
        """Testa obtenção de resumo"""
        from dashboard_analytics.src.services.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        summary = aggregator.get_summary("30d")
        
        assert "total_processos" in summary
        assert "total_receita" in summary
        assert "time_window" in summary
    
    def test_get_active_alerts(self):
        """Testa obtenção de alertas ativos"""
        from dashboard_analytics.src.services.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        aggregator.sources["prazos"] = [
            {"dias_restantes": 2},  # Urgente
            {"dias_restantes": 10}  # OK
        ]
        
        alerts = aggregator.get_active_alerts()
        
        assert isinstance(alerts, list)
        # Deve ter alerta de prazo urgente
        urgent_alerts = [a for a in alerts if a["type"] == "urgent_deadline"]
        assert len(urgent_alerts) > 0 if aggregator.sources.get("prazos") else True
    
    def test_get_revenue_trend(self):
        """Testa obtenção de tendência de receita"""
        from dashboard_analytics.src.services.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        trend = aggregator.get_revenue_trend("30d")
        
        assert isinstance(trend, list)
        assert len(trend) > 0
        assert "date" in trend[0]
        assert "revenue" in trend[0]
    
    def test_get_process_status_distribution(self):
        """Testa distribuição de status de processos"""
        from dashboard_analytics.src.services.aggregator import DataAggregator
        
        aggregator = DataAggregator()
        aggregator.sources["processos"] = [
            {"status": "ativo"},
            {"status": "ativo"},
            {"status": "inativo"}
        ]
        
        distribution = aggregator.get_process_status_distribution()
        
        assert isinstance(distribution, dict)
        assert "ativo" in distribution
        assert distribution["ativo"] == 2


class TestKPICalculator:
    """Testes para KPI Calculator"""
    
    def test_calculate_all(self):
        """Testa cálculo de todos os KPIs"""
        from dashboard_analytics.src.services.kpi_calculator import KPICalculator
        
        calculator = KPICalculator()
        kpis = calculator.calculate_all("30d")
        
        assert "total_revenue" in kpis
        assert "total_processos" in kpis
        assert "prazos_vencidos" in kpis
        assert "taxa_conversao" in kpis
    
    def test_calculate_single(self):
        """Testa cálculo de KPI único"""
        from dashboard_analytics.src.services.kpi_calculator import KPICalculator
        
        calculator = KPICalculator()
        revenue = calculator.calculate_single("total_revenue", "30d")
        
        assert isinstance(revenue, (int, float))
    
    def test_calculate_prazos_vencidos(self):
        """Testa cálculo de prazos vencidos"""
        from dashboard_analytics.src.services.kpi_calculator import KPICalculator
        
        calculator = KPICalculator()
        calculator.aggregator.sources["prazos"] = [
            {"dias_restantes": -5},  # Vencido
            {"dias_restantes": 10}   # OK
        ]
        
        count = calculator.calculate_prazos_vencidos("30d")
        assert count >= 0
    
    def test_calculate_taxa_conversao(self):
        """Testa cálculo de taxa de conversão"""
        from dashboard_analytics.src.services.kpi_calculator import KPICalculator
        
        calculator = KPICalculator()
        calculator.aggregator.sources["lead_qualifications"] = [
            {"converted": True},
            {"converted": False},
            {"converted": True}
        ]
        
        taxa = calculator.calculate_taxa_conversao("30d")
        
        assert isinstance(taxa, float)
        assert 0 <= taxa <= 100


class TestReportGenerator:
    """Testes para Report Generator"""
    
    def test_list_reports(self):
        """Testa listagem de relatórios"""
        from dashboard_analytics.src.services.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        reports = generator.list_reports()
        
        assert isinstance(reports, list)
        assert len(reports) > 0
        assert "id" in reports[0]
        assert "name" in reports[0]
    
    def test_generate_daily_summary(self):
        """Testa geração de resumo diário"""
        from dashboard_analytics.src.services.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        report = generator.generate("daily_summary", "30d")
        
        assert "type" in report
        assert "kpis" in report
        assert report["type"] == "daily_summary"
    
    def test_generate_weekly_performance(self):
        """Testa geração de relatório de performance"""
        from dashboard_analytics.src.services.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        report = generator.generate("weekly_performance", "30d")
        
        assert "type" in report
        assert report["type"] == "weekly_performance"
    
    def test_generate_deadline_report(self):
        """Testa geração de relatório de prazos"""
        from dashboard_analytics.src.services.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        report = generator.generate("deadline_report", "30d")
        
        assert "type" in report
        assert report["type"] == "deadline_report"
        assert "total" in report


class TestVisualizationEngine:
    """Testes para Visualization Engine"""
    
    def test_generate_process_status_chart(self):
        """Testa geração de gráfico de status"""
        from dashboard_analytics.src.services.visualization import VisualizationEngine
        
        visualizer = VisualizationEngine()
        visualizer.aggregator.sources["processos"] = [
            {"status": "ativo"},
            {"status": "inativo"}
        ]
        
        chart = visualizer.generate_chart("process_status", "30d")
        
        assert "type" in chart
        assert "data" in chart
        assert chart["type"] == "pie"
    
    def test_generate_revenue_trend_chart(self):
        """Testa geração de gráfico de tendência"""
        from dashboard_analytics.src.services.visualization import VisualizationEngine
        
        visualizer = VisualizationEngine()
        chart = visualizer.generate_chart("revenue_trend", "30d")
        
        assert "type" in chart
        assert chart["type"] == "line"
    
    def test_generate_deadline_alerts_chart(self):
        """Testa geração de gráfico de alertas"""
        from dashboard_analytics.src.services.visualization import VisualizationEngine
        
        visualizer = VisualizationEngine()
        visualizer.aggregator.sources["prazos"] = [
            {"dias_restantes": -5},
            {"dias_restantes": 0},
            {"dias_restantes": 5}
        ]
        
        chart = visualizer.generate_chart("deadline_alerts", "30d")
        
        assert "type" in chart
        assert chart["type"] == "bar"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

