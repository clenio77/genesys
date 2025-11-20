"""
Data Aggregator - Coleta e agrega dados de múltiplas fontes
"""

import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime, timedelta

# Adiciona paths para shared
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "tier1" / "shared"))

from shared.utils.logger import setup_logger

logger = setup_logger("aggregator", "aggregator.log")


class DataAggregator:
    """Agrega dados de múltiplas fontes"""
    
    def __init__(self):
        self.sources = {
            'prazos': [],
            'processos': [],
            'consultas': [],
            'receitas': [],
            'lead_qualifications': []
        }
    
    def collect_from_source(self, source: str, data: List[Dict]) -> None:
        """
        Coleta dados de uma fonte específica
        
        Args:
            source: Nome da fonte
            data: Lista de dados
        """
        if source in self.sources:
            self.sources[source] = data
            logger.info(f"Collected {len(data)} records from {source}")
    
    def get_summary(self, time_window: str = "30d") -> Dict[str, Any]:
        """
        Obtém resumo agregado dos dados
        
        Args:
            time_window: Janela de tempo
        
        Returns:
            Dict com resumo
        """
        days = self._get_days_for_window(time_window)
        
        return {
            "total_processos": len(self.sources.get('processos', [])),
            "total_prazos": len(self.sources.get('prazos', [])),
            "total_consultas": len(self.sources.get('consultas', [])),
            "total_receita": sum(item.get('valor', 0) for item in self.sources.get('receitas', [])),
            "total_leads": len(self.sources.get('lead_qualifications', [])),
            "time_window": time_window,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """
        Obtém alertas ativos
        
        Returns:
            Lista de alertas
        """
        alerts = []
        
        # Alertas de prazos próximos
        prazos_urgentes = [
            prazo for prazo in self.sources.get('prazos', [])
            if prazo.get('dias_restantes', float('inf')) <= 3
        ]
        
        if prazos_urgentes:
            alerts.append({
                "type": "urgent_deadline",
                "severity": "high",
                "message": f"{len(prazos_urgentes)} prazos próximos de vencer",
                "count": len(prazos_urgentes)
            })
        
        # Alertas de processos sem atividade
        processos_inativos = [
            proc for proc in self.sources.get('processos', [])
            if (datetime.now() - proc.get('last_update', datetime.now())).days > 30
        ]
        
        if processos_inativos:
            alerts.append({
                "type": "inactive_processes",
                "severity": "medium",
                "message": f"{len(processos_inativos)} processos inativos há mais de 30 dias",
                "count": len(processos_inativos)
            })
        
        return alerts
    
    def get_revenue_trend(self, time_window: str = "30d") -> List[Dict[str, Any]]:
        """
        Obtém tendência de receita
        
        Args:
            time_window: Janela de tempo
        
        Returns:
            Lista com dados de receita por dia
        """
        days = self._get_days_for_window(time_window)
        
        # Mock data for MVP
        trend = []
        for i in range(days):
            date = datetime.now() - timedelta(days=days - i)
            trend.append({
                "date": date.strftime("%Y-%m-%d"),
                "revenue": 1000 + (i * 50) + (i % 3 * 100),  # Mock trend
                "transactions": 5 + (i % 3)
            })
        
        return trend
    
    def get_process_status_distribution(self) -> Dict[str, int]:
        """
        Distribuição de status de processos
        
        Returns:
            Dict com contagem por status
        """
        processos = self.sources.get('processos', [])
        
        distribution = {}
        for proc in processos:
            status = proc.get('status', 'unknown')
            distribution[status] = distribution.get(status, 0) + 1
        
        return distribution
    
    def _get_days_for_window(self, time_window: str) -> int:
        """Converte time window em dias"""
        windows = {
            "today": 1,
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "365d": 365
        }
        return windows.get(time_window, 30)

