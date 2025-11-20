"""
Visualization Engine - Gera dados para gráficos
"""

from typing import Dict, List, Any
from src.services.aggregator import DataAggregator
from src.services.kpi_calculator import KPICalculator


class VisualizationEngine:
    """Gerencia visualizações e gráficos"""
    
    def __init__(self):
        self.aggregator = DataAggregator()
        self.kpi_calculator = KPICalculator()
    
    def generate_chart(self, chart_type: str, time_window: str) -> Dict[str, Any]:
        """
        Gera dados para um gráfico específico
        
        Args:
            chart_type: Tipo de gráfico
            time_window: Janela de tempo
        
        Returns:
            Dict com dados do gráfico
        """
        if chart_type == "process_status":
            return self._generate_process_status_chart()
        
        if chart_type == "revenue_trend":
            return self._generate_revenue_trend_chart(time_window)
        
        if chart_type == "deadline_alerts":
            return self._generate_deadline_alerts_chart()
        
        if chart_type == "lead_conversion":
            return self._generate_lead_conversion_chart(time_window)
        
        raise ValueError(f"Unknown chart type: {chart_type}")
    
    def _generate_process_status_chart(self) -> Dict[str, Any]:
        """Gera gráfico de status de processos"""
        distribution = self.aggregator.get_process_status_distribution()
        
        labels = list(distribution.keys())
        data = list(distribution.values())
        
        return {
            "type": "pie",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Processos",
                    "data": data,
                    "backgroundColor": [
                        "#3b82f6",  # blue
                        "#10b981",  # green
                        "#f59e0b",  # amber
                        "#ef4444",  # red
                        "#8b5cf6"   # purple
                    ]
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": "Status de Processos"
                    }
                }
            }
        }
    
    def _generate_revenue_trend_chart(self, time_window: str) -> Dict[str, Any]:
        """Gera gráfico de tendência de receita"""
        trend_data = self.aggregator.get_revenue_trend(time_window)
        
        labels = [item['date'] for item in trend_data]
        revenue = [item['revenue'] for item in trend_data]
        transactions = [item['transactions'] for item in trend_data]
        
        return {
            "type": "line",
            "data": {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Receita (R$)",
                        "data": revenue,
                        "borderColor": "#3b82f6",
                        "backgroundColor": "rgba(59, 130, 246, 0.1)",
                        "yAxisID": "y"
                    },
                    {
                        "label": "Transações",
                        "data": transactions,
                        "borderColor": "#10b981",
                        "backgroundColor": "rgba(16, 185, 129, 0.1)",
                        "yAxisID": "y1"
                    }
                ]
            },
            "options": {
                "responsive": True,
                "interaction": {
                    "mode": "index",
                    "intersect": False
                },
                "plugins": {
                    "title": {
                        "display": True,
                        "text": "Tendência de Receita"
                    }
                },
                "scales": {
                    "y": {
                        "type": "linear",
                        "display": True,
                        "position": "left"
                    },
                    "y1": {
                        "type": "linear",
                        "display": True,
                        "position": "right",
                        "grid": {
                            "drawOnChartArea": False
                        }
                    }
                }
            }
        }
    
    def _generate_deadline_alerts_chart(self) -> Dict[str, Any]:
        """Gera gráfico de alertas de prazos"""
        prazos = self.aggregator.sources.get('prazos', [])
        
        vencidos = sum(1 for p in prazos if p.get('dias_restantes', 0) < 0)
        hoje = sum(1 for p in prazos if p.get('dias_restantes', 0) == 0)
        proximos_3 = sum(1 for p in prazos if 0 < p.get('dias_restantes', 10) <= 3)
        proximos_7 = sum(1 for p in prazos if 3 < p.get('dias_restantes', 10) <= 7)
        ok = sum(1 for p in prazos if p.get('dias_restantes', 10) > 7)
        
        return {
            "type": "bar",
            "data": {
                "labels": ["Vencidos", "Hoje", "Próximos 3 dias", "Próximos 7 dias", "OK"],
                "datasets": [{
                    "label": "Prazos",
                    "data": [vencidos, hoje, proximos_3, proximos_7, ok],
                    "backgroundColor": [
                        "#ef4444",  # red
                        "#f59e0b",  # amber
                        "#eab308",  # yellow
                        "#84cc16",  # lime
                        "#10b981"   # green
                    ]
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": "Alertas de Prazos"
                    }
                }
            }
        }
    
    def _generate_lead_conversion_chart(self, time_window: str) -> Dict[str, Any]:
        """Gera gráfico de conversão de leads"""
        summary = self.aggregator.get_summary(time_window)
        total_leads = summary.get('total_leads', 0)
        
        # Mock data para MVP
        return {
            "type": "doughnut",
            "data": {
                "labels": ["Convertidos", "Não Convertidos"],
                "datasets": [{
                    "data": [
                        int(total_leads * 0.35),  # 35% conversão
                        int(total_leads * 0.65)  # 65% não convertidos
                    ],
                    "backgroundColor": ["#10b981", "#e5e7eb"]
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": "Taxa de Conversão de Leads"
                    }
                }
            }
        }

