"""
Serviço de notificações para prazos processuais
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.config.settings import settings
from shared.config.database import get_db
from shared.database.models import Prazo, Notificacao
from shared.utils.logger import setup_logger

logger = setup_logger("automacao_prazos", "automacao_prazos.log")


class NotificationService:
    """Gerencia envio de notificações"""
    
    def __init__(self):
        self.db = next(get_db())
    
    def notificar_prazo(self, prazo: Prazo, dias_restantes: int):
        """Envia notificações para um prazo"""
        logger.info(f"Notificando prazo {prazo.id} - {dias_restantes} dias restantes")
        
        # Determinar canais baseado em dias restantes
        if dias_restantes <= 1:
            # Urgente: Todos os canais
            self._enviar_email(prazo, dias_restantes)
            self._enviar_telegram(prazo, dias_restantes)
            self._enviar_whatsapp(prazo, dias_restantes)
        elif dias_restantes <= 3:
            # Alto: Email + Telegram
            self._enviar_email(prazo, dias_restantes)
            self._enviar_telegram(prazo, dias_restantes)
        else:
            # Normal: Apenas email
            self._enviar_email(prazo, dias_restantes)
    
    def enviar_notificacao_urgente(self, prazo: Prazo, dias_restantes: int, prioridade: str):
        """Envia notificação urgente"""
        logger.warning(f"Enviando notificação urgente para prazo {prazo.id}")
        
        mensagem = self._gerar_mensagem_urgente(prazo, dias_restantes)
        
        # Registrar notificação
        notificacao = Notificacao(
            prazo_id=prazo.id,
            user_id=prazo.user_id,
            canal="email",
            mensagem=mensagem,
            status="enviada",
            metadata={"prioridade": prioridade, "dias_restantes": dias_restantes}
        )
        
        self.db.add(notificacao)
        self.db.commit()
    
    def _enviar_email(self, prazo: Prazo, dias_restantes: int):
        """Envia notificação por email"""
        logger.info(f"Enviando email para prazo {prazo.id}")
        
        # TODO: Implementar envio de email real
        mensagem = f"Lembrete: Prazo {prazo.tipo} vence em {dias_restantes} dias"
        
        # Registrar notificação
        notificacao = Notificacao(
            prazo_id=prazo.id,
            user_id=prazo.user_id,
            canal="email",
            mensagem=mensagem
        )
        
        self.db.add(notificacao)
        self.db.commit()
    
    def _enviar_telegram(self, prazo: Prazo, dias_restantes: int):
        """Envia notificação por Telegram"""
        logger.info(f"Enviando Telegram para prazo {prazo.id}")
        
        # TODO: Implementar envio via Telegram Bot API
        
        mensagem = f"⚠️ Prazo {prazo.tipo} vence em {dias_restantes} dias"
        
        notificacao = Notificacao(
            prazo_id=prazo.id,
            user_id=prazo.user_id,
            canal="telegram",
            mensagem=mensagem
        )
        
        self.db.add(notificacao)
        self.db.commit()
    
    def _enviar_whatsapp(self, prazo: Prazo, dias_restantes: int):
        """Envia notificação por WhatsApp"""
        logger.info(f"Enviando WhatsApp para prazo {prazo.id}")
        
        # TODO: Implementar envio via WhatsApp Business API
        
        mensagem = f"🚨 URGENTE: Prazo {prazo.tipo} vence em {dias_restantes} dias"
        
        notificacao = Notificacao(
            prazo_id=prazo.id,
            user_id=prazo.user_id,
            canal="whatsapp",
            mensagem=mensagem
        )
        
        self.db.add(notificacao)
        self.db.commit()
    
    def _gerar_mensagem_urgente(self, prazo: Prazo, dias_restantes: int) -> str:
        """Gera mensagem de notificação urgente"""
        if dias_restantes == 0:
            return f"🚨 PRAZO HOJE: {prazo.tipo}"
        elif dias_restantes == 1:
            return f"⚠️ PRAZO AMANHÃ: {prazo.tipo}"
        else:
            return f"📅 Prazo {prazo.tipo} vence em {dias_restantes} dias"
    
    def get_estatisticas_notificacoes(self, user_id: int, days: int = 30) -> dict:
        """Retorna estatísticas de notificações do usuário"""
        desde = datetime.now() - timedelta(days=days)
        
        notificacoes = self.db.query(Notificacao).filter(
            Notificacao.user_id == user_id,
            Notificacao.created_at >= desde
        ).all()
        
        return {
            "total": len(notificacoes),
            "por_canal": {
                "email": len([n for n in notificacoes if n.canal == "email"]),
                "telegram": len([n for n in notificacoes if n.canal == "telegram"]),
                "whatsapp": len([n for n in notificacoes if n.canal == "whatsapp"])
            }
        }

