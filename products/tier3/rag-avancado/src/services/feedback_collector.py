"""
Microserviço 6: Feedback Collector
Responsável por coletar e processar feedback dos usuários
"""

from typing import Dict, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.query import QueryHistory


class FeedbackCollector:
    """Coleta e processa feedback para melhorar o sistema"""
    
    def __init__(self):
        self.feedback_cache = []
    
    async def collect_feedback(
        self,
        query_id: int,
        feedback_data: Dict,
        db: Session
    ) -> Dict:
        """
        Coleta feedback do usuário
        
        Args:
            query_id: ID da query
            feedback_data: Dados do feedback (rating, comentário, etc)
            db: Sessão do banco
            
        Returns:
            Dict confirmando feedback
        """
        try:
            # Buscar query history
            query = db.query(QueryHistory).filter(
                QueryHistory.id == query_id
            ).first()
            
            if not query:
                return {
                    "success": False,
                    "error": "Query não encontrada"
                }
            
            # Atualizar com feedback
            query.rating = feedback_data.get("rating")
            query.feedback_text = feedback_data.get("comment")
            query.is_helpful = feedback_data.get("is_helpful")
            query.updated_at = datetime.utcnow()
            
            db.commit()
            
            # Processar feedback para métricas
            await self._process_feedback_metrics(query, feedback_data)
            
            return {
                "success": True,
                "query_id": query_id,
                "message": "Feedback registrado com sucesso"
            }
        
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _process_feedback_metrics(
        self,
        query: QueryHistory,
        feedback: Dict
    ):
        """Processa feedback para gerar métricas"""
        # Cache para análise posterior
        self.feedback_cache.append({
            "query_id": query.id,
            "rating": feedback.get("rating"),
            "is_helpful": feedback.get("is_helpful"),
            "query_type": query.query_type,
            "processing_time": query.processing_time_ms,
            "confidence": query.answer_confidence,
            "timestamp": datetime.utcnow()
        })
        
        # TODO: Enviar para sistema de analytics
        # TODO: Treinar modelo com feedback negativo
    
    async def get_feedback_stats(self, db: Session) -> Dict:
        """
        Retorna estatísticas de feedback
        
        Args:
            db: Sessão do banco
            
        Returns:
            Dict com estatísticas
        """
        try:
            from sqlalchemy import func
            
            # Total de queries com feedback
            total_with_feedback = db.query(QueryHistory).filter(
                QueryHistory.rating.isnot(None)
            ).count()
            
            # Média de rating
            avg_rating = db.query(
                func.avg(QueryHistory.rating)
            ).filter(
                QueryHistory.rating.isnot(None)
            ).scalar()
            
            # Distribuição de ratings
            rating_dist = db.query(
                QueryHistory.rating,
                func.count(QueryHistory.id)
            ).filter(
                QueryHistory.rating.isnot(None)
            ).group_by(
                QueryHistory.rating
            ).all()
            
            # Queries úteis vs não úteis
            helpful_count = db.query(QueryHistory).filter(
                QueryHistory.is_helpful == True
            ).count()
            
            not_helpful_count = db.query(QueryHistory).filter(
                QueryHistory.is_helpful == False
            ).count()
            
            return {
                "total_queries": db.query(QueryHistory).count(),
                "queries_with_feedback": total_with_feedback,
                "average_rating": round(avg_rating, 2) if avg_rating else 0,
                "rating_distribution": dict(rating_dist),
                "helpful_queries": helpful_count,
                "not_helpful_queries": not_helpful_count,
                "feedback_rate": round(
                    total_with_feedback / max(db.query(QueryHistory).count(), 1) * 100,
                    2
                )
            }
        
        except Exception as e:
            return {
                "error": str(e)
            }
    
    async def identify_improvement_areas(self, db: Session) -> List[Dict]:
        """
        Identifica áreas que precisam de melhoria
        
        Args:
            db: Sessão do banco
            
        Returns:
            Lista de áreas com problemas
        """
        try:
            # Queries com baixo rating
            low_rated = db.query(QueryHistory).filter(
                QueryHistory.rating <= 2
            ).order_by(
                QueryHistory.created_at.desc()
            ).limit(10).all()
            
            # Queries marcadas como não úteis
            not_helpful = db.query(QueryHistory).filter(
                QueryHistory.is_helpful == False
            ).order_by(
                QueryHistory.created_at.desc()
            ).limit(10).all()
            
            # Analisar padrões
            issues = []
            
            # Agrupar por tipo de query
            for query in low_rated + not_helpful:
                issues.append({
                    "query_id": query.id,
                    "query_text": query.query_text,
                    "query_type": query.query_type,
                    "rating": query.rating,
                    "is_helpful": query.is_helpful,
                    "confidence": query.answer_confidence,
                    "results_count": query.results_count,
                    "feedback": query.feedback_text
                })
            
            return issues
        
        except Exception as e:
            print(f"❌ Erro ao identificar melhorias: {e}")
            return []

