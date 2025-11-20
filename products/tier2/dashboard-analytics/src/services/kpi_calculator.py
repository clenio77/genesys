"""
KPI Calculator - Calcula métricas e KPIs
"""

from typing import Dict, Any
from src.services.aggregator import DataAggregator


class KPICalculator:
    """Calcula KPIs para o dashboard"""
    
    def __init__(self):
        self.aggregator = DataAggregator()
    
    def calculate_all(self, time_window: str = "today") -> Dict[str, Any]:
        """
        Calcula todos os KPIs
        
        Args:
            time_window: Janela de tempo
        
        Returns:
            Dict com todos os KPIs
        """
        return {
            "total_revenue": self.calculate_revenue(time_window),
            "total_processos": self.calculate_total_processos(time_window),
            "prazos_vencidos": self.calculate_prazos_vencidos(time_window),
            "prazos_hoje": self.calculate_prazos_hoje(time_window),
            "taxa_conversao": self.calculate_taxa_conversao(time_window),
            "tempo_medio_resposta": self.calculate_tempo_medio_resposta(time_window),
            "satisfacao_cliente": self.calculate_satisfacao_cliente(time_window),
            "cpu_usage": self.calculate_cpu_usage(),
            "memory_usage": self.calculate_memory_usage(),
            "active_users": self.calculate_active_users(time_window)
        }
    
    def calculate_single(self, kpi_name: str, time_window: str = "today") -> Any:
        """
        Calcula um KPI específico
        
        Args:
            kpi_name: Nome do KPI
            time_window: Janela de tempo
        
        Returns:
            Valor do KPI
        """
        calculations = {
            "total_revenue": self.calculate_revenue(time_window),
            "total_processos": self.calculate_total_processos(time_window),
            "prazos_vencidos": self.calculate_prazos_vencidos(time_window),
            "prazos_hoje": self.calculate_prazos_hoje(time_window),
            "taxa_conversao": self.calculate_taxa_conversao(time_window),
            "tempo_medio_resposta": self.calculate_tempo_medio_resposta(time_window),
            "satisfacao_cliente": self.calculate_satisfacao_cliente(time_window)
        }
        
        return calculations.get(kpi_name, 0)
    
    def calculate_revenue(self, time_window: str) -> float:
        """Calcula receita total"""
        summary = self.aggregator.get_summary(time_window)
        return summary.get('total_receita', 0)
    
    def calculate_total_processos(self, time_window: str) -> int:
        """Calcula total de processos"""
        summary = self.aggregator.get_summary(time_window)
        return summary.get('total_processos', 0)
    
    def calculate_prazos_vencidos(self, time_window: str) -> int:
        """Calcula prazos vencidos"""
        prazos = self.aggregator.sources.get('prazos', [])
        return sum(1 for prazo in prazos if prazo.get('dias_restantes', 0) < 0)
    
    def calculate_prazos_hoje(self, time_window: str) -> int:
        """Calcula prazos vencendo hoje"""
        prazos = self.aggregator.sources.get('prazos', [])
        return sum(1 for prazo in prazos if prazo.get('dias_restantes', 0) == 0)
    
    def calculate_taxa_conversao(self, time_window: str) -> float:
        """Calcula taxa de conversão de leads"""
        summary = self.aggregator.get_summary(time_window)
        total_leads = summary.get('total_leads', 0)
        conversoes = sum(1 for lead in self.aggregator.sources.get('lead_qualifications', []) 
                        if lead.get('converted', False))
        
        if total_leads > 0:
            return (conversoes / total_leads) * 100
        return 0.0
    
    def calculate_tempo_medio_resposta(self, time_window: str) -> float:
        """Calcula tempo médio de resposta"""
        # Mock data para MVP
        return 2.5  # minutos
    
    def calculate_satisfacao_cliente(self, time_window: str) -> float:
        """Calcula índice de satisfação"""
        # Mock data para MVP
        return 4.5  # de 5.0
    
    def calculate_cpu_usage(self) -> float:
        """Calcula uso de CPU"""
        # Mock data para MVP
        return 45.2  # porcentagem
    
    def calculate_memory_usage(self) -> float:
        """Calcula uso de memória"""
        # Mock data para MVP
        return 68.5  # porcentagem
    
    def calculate_active_users(self, time_window: str) -> int:
        """Calcula usuários ativos"""
        # Mock data para MVP
        return 125

