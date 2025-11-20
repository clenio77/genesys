"""
Dialog Manager - Gerenciamento de conversas e contexto
"""

from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Conversation:
    """Representa uma conversa ativa"""
    phone: str
    context: Dict[str, any]
    history: list
    created_at: datetime
    last_activity: datetime
    
    def __post_init__(self):
        if 'step' not in self.context:
            self.context['step'] = 'greeting'
        if 'data' not in self.context:
            self.context['data'] = {}


class DialogManager:
    """Gerencia contexto e fluxos de conversação"""
    
    def __init__(self):
        self.conversations: Dict[str, Conversation] = {}
        self.timeout = timedelta(hours=2)
    
    def get_or_create_conversation(self, phone: str) -> Conversation:
        """
        Obtém ou cria uma conversa
        
        Args:
            phone: Número do telefone
        
        Returns:
            Conversation object
        """
        if phone not in self.conversations:
            self.conversations[phone] = Conversation(
                phone=phone,
                context={},
                history=[],
                created_at=datetime.now(),
                last_activity=datetime.now()
            )
        
        # Verificar timeout
        conv = self.conversations[phone]
        if datetime.now() - conv.last_activity > self.timeout:
            # Resetar conversa
            conv.context = {'step': 'greeting'}
            conv.history = []
        
        conv.last_activity = datetime.now()
        
        return conv
    
    def add_message_to_history(self, phone: str, message: str, from_user: bool = True):
        """
        Adiciona mensagem ao histórico
        
        Args:
            phone: Número do telefone
            message: Conteúdo da mensagem
            from_user: True se do usuário, False se do bot
        """
        conv = self.get_or_create_conversation(phone)
        
        conv.history.append({
            'message': message,
            'from_user': from_user,
            'timestamp': datetime.now()
        })
    
    def set_context_data(self, phone: str, key: str, value: any):
        """
        Define dado no contexto
        
        Args:
            phone: Número do telefone
            key: Chave do dado
            value: Valor
        """
        conv = self.get_or_create_conversation(phone)
        conv.context['data'][key] = value
    
    def get_context_data(self, phone: str, key: str, default=None):
        """
        Obtém dado do contexto
        
        Args:
            phone: Número do telefone
            key: Chave do dado
            default: Valor padrão
        
        Returns:
            Valor do contexto
        """
        conv = self.get_or_create_conversation(phone)
        return conv.context['data'].get(key, default)
    
    def set_step(self, phone: str, step: str):
        """
        Define o step atual da conversa
        
        Args:
            phone: Número do telefone
            step: Nome do step
        """
        conv = self.get_or_create_conversation(phone)
        conv.context['step'] = step
    
    def get_step(self, phone: str) -> str:
        """
        Obtém o step atual
        
        Args:
            phone: Número do telefone
        
        Returns:
            Nome do step
        """
        conv = self.get_or_create_conversation(phone)
        return conv.context.get('step', 'greeting')
    
    def reset_conversation(self, phone: str):
        """
        Reseta a conversa
        
        Args:
            phone: Número do telefone
        """
        if phone in self.conversations:
            self.conversations[phone].context = {'step': 'greeting'}
            self.conversations[phone].history = []
    
    def get_recent_messages(self, phone: str, limit: int = 5) -> list:
        """
        Obtém últimas mensagens
        
        Args:
            phone: Número do telefone
            limit: Número de mensagens
        
        Returns:
            Lista de mensagens recentes
        """
        conv = self.get_or_create_conversation(phone)
        return conv.history[-limit:]

