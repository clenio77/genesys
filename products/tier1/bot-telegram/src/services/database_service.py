"""
Serviço para interagir com banco de dados
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy.orm import Session
from sqlalchemy import desc
from shared.config.database import get_db
from shared.database.models import User, Chat, Prazo, Notificacao, ConsultaJurisprudencia
from shared.utils.logger import bot_telegram_logger as logger


class DatabaseService:
    """Serviço para operações de banco de dados"""
    
    def get_or_create_user(self, telegram_id: int, username: str, full_name: str) -> Optional[User]:
        """
        Busca ou cria um usuário
        Retorna None se houver erro (banco não disponível) - não crítico para funcionamento do bot
        """
        try:
            db: Session = next(get_db())
            
            try:
                user = db.query(User).filter(User.telegram_id == telegram_id).first()
                
                if not user:
                    user = User(
                        telegram_id=telegram_id,
                        name=full_name,
                        role="user",
                        alerta_canal="telegram",  # Default
                        alerta_intervalo_dias=3,  # Default
                        alerta_ativo=True  # Default
                    )
                    db.add(user)
                    db.commit()
                    db.refresh(user)
                    logger.info(f"Usuário criado: {telegram_id} - {full_name}")
                else:
                    # Atualizar nome se mudou
                    if user.name != full_name:
                        user.name = full_name
                        db.commit()
                        db.refresh(user)
                
                return user
                
            except Exception as e:
                logger.warning(f"⚠️ Banco de dados não disponível: {e}")
                logger.info("💡 Bot continuará funcionando sem banco de dados")
                db.rollback()
                return None
            finally:
                db.close()
        except Exception as e:
            # Erro ao conectar ao banco - não crítico
            logger.warning(f"⚠️ Erro ao conectar ao banco de dados: {e}")
            logger.info("💡 Bot continuará funcionando sem banco de dados")
            return None
    
    def save_chat(self, user_id: int, message: str, response: str, metadata: Optional[Dict] = None):
        """Salva conversa no histórico"""
        db: Session = next(get_db())
        
        try:
            chat = Chat(
                user_id=user_id,
                service="telegram",
                message=message,
                response=response,
                metadata=metadata
            )
            db.add(chat)
            db.commit()
            
        except Exception as e:
            logger.error(f"Erro ao salvar chat: {e}")
            db.rollback()
        finally:
            db.close()
    
    def get_user_prazos(self, user_id: int) -> List[Prazo]:
        """Busca prazos do usuário"""
        db: Session = next(get_db())
        
        try:
            prazos = db.query(Prazo).filter(
                Prazo.user_id == user_id,
                Prazo.status == "pendente"
            ).order_by(desc(Prazo.data_vencimento)).limit(10).all()
            
            return prazos
            
        except Exception as e:
            logger.error(f"Erro ao buscar prazos: {e}")
            return []
        finally:
            db.close()
    
    def get_recent_chats(self, user_id: int, limit: int = 5) -> List[Dict]:
        """Busca conversas recentes do usuário"""
        db: Session = next(get_db())
        
        try:
            chats = db.query(Chat).filter(
                Chat.user_id == user_id
            ).order_by(desc(Chat.created_at)).limit(limit).all()
            
            return [{
                "message": chat.message,
                "response": chat.response,
                "created_at": chat.created_at
            } for chat in chats]
            
        except Exception as e:
            logger.error(f"Erro ao buscar chats: {e}")
            return []
        finally:
            db.close()
    
    def save_jurisprudencia_query(self, user_id: int, query: str, results: Dict):
        """Salva consulta de jurisprudência"""
        db: Session = next(get_db())
        
        try:
            consulta = ConsultaJurisprudencia(
                user_id=user_id,
                query=query,
                results=results,
                service="telegram"
            )
            db.add(consulta)
            db.commit()
            
        except Exception as e:
            logger.error(f"Erro ao salvar consulta de jurisprudência: {e}")
            db.rollback()
        finally:
            db.close()
    
    def get_historico_consultas(self, user_id: int, tipo: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Busca histórico de consultas do usuário
        
        Args:
            user_id: ID do usuário
            tipo: Tipo de consulta ('processo', 'magistrado', 'promotor', 'buscar', None para todos)
            limit: Limite de resultados
            
        Returns:
            Lista de consultas
        """
        db: Session = next(get_db())
        
        try:
            historico = []
            
            # Buscar conversas gerais
            if tipo is None or tipo == 'geral':
                chats = db.query(Chat).filter(
                    Chat.user_id == user_id
                ).order_by(desc(Chat.created_at)).limit(limit).all()
                
                for chat in chats:
                    # Detectar tipo de consulta pela mensagem
                    msg_lower = chat.message.lower()
                    tipo_detectado = 'geral'
                    
                    if any(p in msg_lower for p in ['processo', 'cnj', 'número']):
                        tipo_detectado = 'processo'
                    elif 'magistrado' in msg_lower or 'juiz' in msg_lower:
                        tipo_detectado = 'magistrado'
                    elif 'promotor' in msg_lower:
                        tipo_detectado = 'promotor'
                    elif any(p in msg_lower for p in ['buscar', 'jurisprudência', 'decisão']):
                        tipo_detectado = 'buscar'
                    
                    historico.append({
                        'tipo': tipo_detectado,
                        'consulta': chat.message[:100] + '...' if len(chat.message) > 100 else chat.message,
                        'resposta': chat.response[:150] + '...' if len(chat.response) > 150 else chat.response,
                        'data': chat.created_at,
                        'metadata': chat.metadata
                    })
            
            # Buscar consultas de jurisprudência
            if tipo is None or tipo == 'buscar':
                consultas_juris = db.query(ConsultaJurisprudencia).filter(
                    ConsultaJurisprudencia.user_id == user_id
                ).order_by(desc(ConsultaJurisprudencia.created_at)).limit(limit).all()
                
                for consulta in consultas_juris:
                    historico.append({
                        'tipo': 'buscar',
                        'consulta': consulta.query[:100] + '...' if len(consulta.query) > 100 else consulta.query,
                        'resposta': f"Resultados: {len(consulta.results) if isinstance(consulta.results, (list, dict)) else 'N/A'}",
                        'data': consulta.created_at,
                        'metadata': consulta.results
                    })
            
            # Filtrar por tipo se especificado
            if tipo and tipo != 'geral':
                historico = [h for h in historico if h['tipo'] == tipo]
            
            # Ordenar por data e limitar
            historico.sort(key=lambda x: x['data'], reverse=True)
            return historico[:limit]
            
        except Exception as e:
            logger.error(f"Erro ao buscar histórico: {e}")
            return []
        finally:
            db.close()
    
    def limpar_historico(self, user_id: int, tipo: Optional[str] = None) -> tuple[bool, str]:
        """
        Limpa histórico do usuário
        
        Args:
            user_id: ID do usuário
            tipo: Tipo a limpar (None para todos)
            
        Returns:
            (sucesso, mensagem)
        """
        db: Session = next(get_db())
        
        try:
            if tipo is None:
                # Limpar tudo
                chats_deletados = db.query(Chat).filter(Chat.user_id == user_id).delete()
                consultas_deletadas = db.query(ConsultaJurisprudencia).filter(
                    ConsultaJurisprudencia.user_id == user_id
                ).delete()
                db.commit()
                
                total = chats_deletados + consultas_deletadas
                return True, f"✅ Histórico limpo com sucesso! {total} registro(s) removido(s)."
            else:
                # Limpar apenas tipo específico
                if tipo == 'buscar':
                    deletados = db.query(ConsultaJurisprudencia).filter(
                        ConsultaJurisprudencia.user_id == user_id
                    ).delete()
                else:
                    # Para outros tipos, filtrar por metadata ou mensagem
                    deletados = 0
                    chats = db.query(Chat).filter(Chat.user_id == user_id).all()
                    for chat in chats:
                        msg_lower = chat.message.lower()
                        if tipo == 'processo' and any(p in msg_lower for p in ['processo', 'cnj']):
                            db.delete(chat)
                            deletados += 1
                        elif tipo == 'magistrado' and ('magistrado' in msg_lower or 'juiz' in msg_lower):
                            db.delete(chat)
                            deletados += 1
                        elif tipo == 'promotor' and 'promotor' in msg_lower:
                            db.delete(chat)
                            deletados += 1
                
                db.commit()
                return True, f"✅ Histórico de '{tipo}' limpo com sucesso! {deletados} registro(s) removido(s)."
                
        except Exception as e:
            logger.error(f"Erro ao limpar histórico: {e}")
            db.rollback()
            return False, "❌ Erro ao limpar histórico. Tente novamente."
        finally:
            db.close()


# Instância global
db_service = DatabaseService()

