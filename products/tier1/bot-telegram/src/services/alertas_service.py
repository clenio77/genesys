"""
Serviço para gerenciar alertas e preferências do usuário
"""

import sys
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from sqlalchemy.orm import Session
from shared.config.database import get_db
from shared.database.models import User, Alerta, Notificacao
from shared.utils.logger import bot_telegram_logger as logger


class AlertasService:
    """Serviço para gerenciar alertas e preferências"""
    
    def get_user_alert_preferences(self, user_id: int) -> Optional[Dict]:
        """Busca preferências de alerta do usuário"""
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            return {
                "canal": user.alerta_canal or "telegram",
                "intervalo_dias": user.alerta_intervalo_dias or 3,
                "ativo": user.alerta_ativo if user.alerta_ativo is not None else True,
                "horario": user.alerta_horario
            }
        except Exception as e:
            logger.error(f"Erro ao buscar preferências de alerta: {e}")
            return None
        finally:
            db.close()
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Busca usuário por telegram_id"""
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.telegram_id == telegram_id).first()
            return user
        except Exception as e:
            logger.error(f"Erro ao buscar usuário por telegram_id: {e}")
            return None
        finally:
            db.close()
    
    def update_alert_channel(self, user_id: int, canal: str) -> bool:
        """Atualiza canal preferido de alertas"""
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.error(f"Usuário {user_id} não encontrado")
                return False
            
            user.alerta_canal = canal
            user.updated_at = datetime.now()
            db.commit()
            logger.info(f"Preferência de canal atualizada: {canal}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar canal de alerta: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    def update_alert_interval(self, user_id: int, dias: int) -> bool:
        """Atualiza intervalo de dias para alertas"""
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.error(f"Usuário {user_id} não encontrado")
                return False
            
            user.alerta_intervalo_dias = dias
            user.updated_at = datetime.now()
            db.commit()
            logger.info(f"Intervalo de alertas atualizado: {dias} dias")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar intervalo de alertas: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    def toggle_alertas(self, user_id: int, ativo: bool) -> bool:
        """Ativa/desativa alertas do usuário"""
        db: Session = next(get_db())
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                logger.error(f"Usuário {user_id} não encontrado")
                return False
            
            user.alerta_ativo = ativo
            user.updated_at = datetime.now()
            db.commit()
            logger.info(f"Alertas {'ativados' if ativo else 'desativados'} para usuário {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao alterar status de alertas: {e}")
            db.rollback()
            return False
        finally:
            db.close()
    
    def criar_alerta(self, user_id: int, tipo: str, titulo: str, mensagem: str, prioridade: str = "media") -> Optional[Alerta]:
        """Cria um alerta no banco de dados"""
        db: Session = next(get_db())
        
        try:
            alerta = Alerta(
                user_id=user_id,
                tipo=tipo,
                titulo=titulo,
                mensagem=mensagem,
                prioridade=prioridade,
                lido=False
            )
            db.add(alerta)
            db.commit()
            db.refresh(alerta)
            logger.info(f"Alerta criado: {alerta.id} - {titulo}")
            return alerta
            
        except Exception as e:
            logger.error(f"Erro ao criar alerta: {e}")
            db.rollback()
            return None
        finally:
            db.close()
    
    def registrar_notificacao(self, user_id: int, prazo_id: Optional[int], canal: str, mensagem: str, status: str = "enviada") -> Optional[Notificacao]:
        """Registra notificação enviada no histórico"""
        db: Session = next(get_db())
        
        try:
            notificacao = Notificacao(
                user_id=user_id,
                prazo_id=prazo_id,
                canal=canal,
                mensagem=mensagem,
                status=status
            )
            db.add(notificacao)
            db.commit()
            db.refresh(notificacao)
            return notificacao
            
        except Exception as e:
            logger.error(f"Erro ao registrar notificação: {e}")
            db.rollback()
            return None
        finally:
            db.close()
    
    def verificar_alertas_kermartin(self, telegram_id: int) -> List[Dict]:
        """
        Verifica processos do Kermartin para gerar alertas
        
        Args:
            telegram_id: ID do Telegram do usuário
            
        Returns:
            Lista de alertas gerados
        """
        try:
            from services.kermartin_service import kermartin_service
            from services.auth_service import auth_service
            
            # Verificar autenticação
            if not auth_service.is_authenticated(telegram_id):
                return []
            
            user = self.get_user_by_telegram_id(telegram_id)
            if not user or not user.alerta_ativo:
                return []
            
            alertas = []
            
            # Buscar processos recentes do Kermartin
            processos = kermartin_service.buscar_processos_rag({})
            
            # Verificar movimentações recentes (últimas 24h)
            from datetime import timedelta
            data_limite = datetime.now() - timedelta(days=1)
            
            for processo in processos[:50]:  # Limitar busca
                try:
                    metadata = processo.get('metadata_json', {})
                    if isinstance(metadata, str):
                        import json
                        try:
                            metadata = json.loads(metadata)
                        except:
                            metadata = {}
                    
                    ultima_mov = metadata.get('ultima_movimentacao') or metadata.get('data_ultima_mov')
                    numero = processo.get('processo_numero') or processo.get('numero')
                    
                    if numero and ultima_mov:
                        try:
                            data_mov = datetime.strptime(ultima_mov[:10], '%Y-%m-%d')
                            if data_mov >= data_limite:
                                alertas.append({
                                    'tipo': 'nova_movimentacao',
                                    'processo': numero,
                                    'data': data_mov,
                                    'tribunal': metadata.get('tribunal', 'N/A'),
                                    'comarca': metadata.get('comarca', 'N/A'),
                                    'mensagem': f"Nova movimentação no processo {numero}"
                                })
                        except:
                            continue
                            
                except Exception as e:
                    logger.warning(f"Erro ao processar processo para alertas: {e}")
                    continue
            
            logger.info(f"Gerados {len(alertas)} alertas do Kermartin para usuário {telegram_id}")
            return alertas
            
        except Exception as e:
            logger.error(f"Erro ao verificar alertas do Kermartin: {e}")
            return []


# Instância global
alertas_service = AlertasService()

