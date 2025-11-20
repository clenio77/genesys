"""
Agendador de tarefas para verificação de prazos processuais
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.config.database import get_db
from shared.database.models import Prazo, Notificacao
from shared.utils.logger import automacao_logger as logger
from .notifier import NotificationService


class PrazoScheduler:
    """Gerencia o agendamento de verificação de prazos"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.notifier = NotificationService()
    
    def verificar_prazos(self):
        """Verifica prazos pendentes e envia notificações"""
        logger.info("Iniciando verificação de prazos...")
        
        db = next(get_db())
        
        try:
            # Obter prazos que expiram nos próximos 7 dias
            hoje = datetime.now().date()
            data_7_dias = hoje + timedelta(days=7)
            
            prazos = db.query(Prazo).filter(
                Prazo.data_vencimento <= data_7_dias,
                Prazo.data_vencimento >= hoje,
                Prazo.status == "pendente"
            ).all()
            
            logger.info(f"Encontrados {len(prazos)} prazos a vencer")
            
            for prazo in prazos:
                dias_restantes = (prazo.data_vencimento - hoje).days
                
                # Verificar se já foi notificado hoje
                hoje_inicio = datetime.combine(hoje, datetime.min.time())
                ultima_notif = prazo.ultima_notificacao
                
                if not ultima_notif or ultima_notif < hoje_inicio:
                    # Notificar usuário
                    self.notifier.notificar_prazo(prazo, dias_restantes)
                    
                    # Atualizar prazo
                    prazo.ultima_notificacao = datetime.now()
                    if dias_restantes <= 1:
                        prazo.alertas_enviados += 1
                    
                    db.commit()
                    logger.info(f"Notificação enviada para prazo {prazo.id}")
        
        except Exception as e:
            logger.error(f"Erro ao verificar prazos: {e}")
            db.rollback()
        finally:
            db.close()
    
    def verificar_prazos_urgentes(self):
        """Verifica prazos que expiram hoje ou amanhã"""
        logger.info("Verificando prazos urgentes...")
        
        db = next(get_db())
        
        try:
            hoje = datetime.now().date()
            amanha = hoje + timedelta(days=1)
            
            prazos_urgentes = db.query(Prazo).filter(
                Prazo.data_vencimento <= amanha,
                Prazo.data_vencimento >= hoje,
                Prazo.status == "pendente"
            ).all()
            
            logger.info(f"Encontrados {len(prazos_urgentes)} prazos urgentes")
            
            for prazo in prazos_urgentes:
                dias_restantes = (prazo.data_vencimento - hoje).days
                prioridade = "critica" if dias_restantes == 0 else "alta"
                
                # Enviar notificação urgente
                self.notifier.enviar_notificacao_urgente(prazo, dias_restantes, prioridade)
        
        except Exception as e:
            logger.error(f"Erro ao verificar prazos urgentes: {e}")
        finally:
            db.close()
    
    def iniciar(self):
        """Inicia o agendador"""
        logger.info("Iniciando scheduler de prazos...")
        
        # Verificar prazos a cada 6 horas
        self.scheduler.add_job(
            self.verificar_prazos,
            trigger=CronTrigger(hour='*/6'),
            id='verificar_prazos',
            name='Verificar Prazos Processuais'
        )
        
        # Verificar prazos urgentes a cada hora
        self.scheduler.add_job(
            self.verificar_prazos_urgentes,
            trigger=CronTrigger(hour='*'),
            id='verificar_prazos_urgentes',
            name='Verificar Prazos Urgentes'
        )
        
        self.scheduler.start()
        logger.info("Scheduler iniciado com sucesso!")
    
    def parar(self):
        """Para o agendador"""
        logger.info("Parando scheduler...")
        self.scheduler.shutdown()


def main():
    """Função principal"""
    scheduler = PrazoScheduler()
    
    try:
        scheduler.iniciar()
        
        # Manter o processo rodando
        import time
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("Interrompido pelo usuário")
        scheduler.parar()
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        scheduler.parar()
        sys.exit(1)


if __name__ == "__main__":
    main()

