"""
Serviço de Notificações - Portal do Cliente
Envia notificações via WhatsApp quando há novas movimentações processuais
"""

import os
import requests
from datetime import datetime
from typing import Dict, Optional

class NotificationService:
    def __init__(self):
        self.whatsapp_api_url = os.getenv("WHATSAPP_API_URL", "http://localhost:8002/api/message/send")
        self.enabled = os.getenv("NOTIFICATIONS_ENABLED", "false").lower() == "true"
    
    def send_process_update(
        self, 
        phone: str, 
        client_name: str, 
        process_title: str, 
        process_cnj: str, 
        event_title: str,
        event_description: str
    ) -> bool:
        """
        Envia notificação de atualização processual via WhatsApp
        
        Args:
            phone: Número do WhatsApp (formato: +55 11 98765-4321)
            client_name: Nome do cliente
            process_title: Título do processo
            process_cnj: Número CNJ
            event_title: Título do evento (ex: "Nova Movimentação")
            event_description: Descrição simplificada
        
        Returns:
            bool: True se enviado com sucesso
        """
        if not self.enabled:
            print(f"[NOTIFICAÇÃO SIMULADA] {phone}: {event_title}")
            return True
        
        message = self._format_message(
            client_name, 
            process_title, 
            process_cnj, 
            event_title,
            event_description
        )
        
        try:
            response = requests.post(
                self.whatsapp_api_url,
                json={
                    "to": phone,
                    "message": message
                },
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao enviar notificação WhatsApp: {e}")
            return False
    
    def _format_message(
        self, 
        client_name: str, 
        process_title: str, 
        process_cnj: str, 
        event_title: str,
        event_description: str
    ) -> str:
        """Formata mensagem para WhatsApp"""
        return f"""🔔 *Nova Atualização no seu Processo*

Olá, {client_name}!

📋 *Processo:* {process_title}
📄 *CNJ:* {process_cnj}

✨ *{event_title}*
{event_description}

Acesse o Portal do Cliente para mais detalhes:
👉 https://portal.genesys.com.br

---
_Genesys Tecnologia Jurídica_"""
    
    def send_deadline_reminder(
        self,
        phone: str,
        client_name: str,
        process_title: str,
        deadline_date: datetime,
        days_remaining: int
    ) -> bool:
        """Envia lembrete de prazo próximo"""
        
        emoji = "⚠️" if days_remaining <= 3 else "📅"
        urgency = "URGENTE" if days_remaining <= 3 else "Atenção"
        
        message = f"""{emoji} *{urgency}: Prazo se aproximando*

Olá, {client_name}!

📋 *Processo:* {process_title}
⏰ *Prazo final:* {deadline_date.strftime('%d/%m/%Y')}
📊 *Faltam:* {days_remaining} dia(s)

Entre em contato com seu advogado se tiver dúvidas.

---
_Genesys Tecnologia Jurídica_"""
        
        if not self.enabled:
            print(f"[LEMBRETE SIMULADO] {phone}: {days_remaining} dias restantes")
            return True
        
        try:
            response = requests.post(
                self.whatsapp_api_url,
                json={"to": phone, "message": message},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao enviar lembrete: {e}")
            return False
    
    def send_welcome(self, phone: str, client_name: str) -> bool:
        """Envia mensagem de boas-vindas ao novo cliente"""
        
        message = f"""👋 Bem-vindo ao Portal do Cliente, {client_name}!

Agora você pode acompanhar seus processos em tempo real, diretamente pelo WhatsApp ou pelo nosso portal web.

🔔 Você receberá notificações automáticas sempre que houver:
• Nova movimentação processual
• Prazos se aproximando
• Audiências agendadas
• Decisões importantes

📱 *Acesse:* https://portal.genesys.com.br
🔐 *Login:* Use seu CPF

Qualquer dúvida, estamos à disposição!

---
_Genesys Tecnologia Jurídica_"""
        
        if not self.enabled:
            print(f"[BOAS-VINDAS SIMULADA] {phone}")
            return True
        
        try:
            response = requests.post(
                self.whatsapp_api_url,
                json={"to": phone, "message": message},
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao enviar boas-vindas: {e}")
            return False
