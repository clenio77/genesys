"""
Report Generator - Gera relatórios automáticos
"""

from typing import Dict, List, Any
from datetime import datetime
from src.services.aggregator import DataAggregator
from src.services.kpi_calculator import KPICalculator


class ReportGenerator:
    """Gera relatórios para o dashboard"""
    
    def __init__(self):
        self.aggregator = DataAggregator()
        self.kpi_calculator = KPICalculator()
    
    def list_reports(self) -> List[Dict[str, str]]:
        """
        Lista relatórios disponíveis
        
        Returns:
            Lista de relatórios
        """
        return [
            {
                "id": "daily_summary",
                "name": "Resumo Diário",
                "description": "Resumo completo do dia",
                "type": "summary"
            },
            {
                "id": "weekly_performance",
                "name": "Performance Semanal",
                "description": "Análise de performance semanal",
                "type": "performance"
            },
            {
                "id": "deadline_report",
                "name": "Relatório de Prazos",
                "description": "Prazos próximos e vencidos",
                "type": "deadlines"
            },
            {
                "id": "revenue_report",
                "name": "Relatório de Receita",
                "description": "Análise de receita e transações",
                "type": "revenue"
            }
        ]
    
    def generate(self, report_type: str, time_window: str = "30d") -> Dict[str, Any]:
        """
        Gera um relatório
        
        Args:
            report_type: Tipo de relatório
            time_window: Janela de tempo
        
        Returns:
            Dict com dados do relatório
        """
        if report_type == "daily_summary":
            return self._generate_daily_summary(time_window)
        
        if report_type == "weekly_performance":
            return self._generate_weekly_performance(time_window)
        
        if report_type == "deadline_report":
            return self._generate_deadline_report(time_window)
        
        if report_type == "revenue_report":
            return self._generate_revenue_report(time_window)
        
        raise ValueError(f"Unknown report type: {report_type}")
    
    def _generate_daily_summary(self, time_window: str) -> Dict[str, Any]:
        """Gera resumo diário"""
        kpis = self.kpi_calculator.calculate_all(time_window)
        
        return {
            "type": "daily_summary",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "kpis": kpis,
            "alerts": self.aggregator.get_active_alerts(),
            "summary": self.aggregator.get_summary(time_window)
        }
    
    def _generate_weekly_performance(self, time_window: str) -> Dict[str, Any]:
        """Gera relatório de performance semanal"""
        return {
            "type": "weekly_performance",
            "period": time_window,
            "kpis": self.kpi_calculator.calculate_all(time_window),
            "trends": {
                "revenue_trend": self.aggregator.get_revenue_trend(time_window),
                "process_status": self.aggregator.get_process_status_distribution()
            }
        }
    
    def _generate_deadline_report(self, time_window: str) -> Dict[str, Any]:
        """Gera relatório de prazos"""
        prazos = self.aggregator.sources.get('prazos', [])
        
        vencidos = [p for p in prazos if p.get('dias_restantes', 0) < 0]
        hoje = [p for p in prazos if p.get('dias_restantes', 0) == 0]
        proximos = [p for p in prazos if 0 < p.get('dias_restantes', 10) <= 7]
        
        return {
            "type": "deadline_report",
            "total": len(prazos),
            "vencidos": len(vencidos),
            "hoje": len(hoje),
            "proximos_7_dias": len(proximos),
            "lista_vencidos": vencidos[:10],  # Top 10
            "lista_hoje": hoje,
            "lista_proximos": proximos
        }
    
    def _generate_revenue_report(self, time_window: str) -> Dict[str, Any]:
        """Gera relatório de receita"""
        return {
            "type": "revenue_report",
            "period": time_window,
            "total_revenue": self.kpi_calculator.calculate_revenue(time_window),
            "trend": self.aggregator.get_revenue_trend(time_window),
            "breakdown": {
                "by_service": {
                    "consultoria": 50000,
                    "automação": 30000,
                    "consultas": 20000
                }
            }
        }

