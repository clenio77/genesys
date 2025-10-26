"""
Chatbot principal do Assistente Virtual 24/7
"""

import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.config.settings import settings
from shared.config.database import get_db
from shared.database.models import Chat, User
from shared.utils.logger import setup_logger

logger = setup_logger("assistente_virtual", "assistente_virtual.log")

app = FastAPI(title="Assistente Virtual 24/7", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatManager:
    """Gerencia conexões WebSocket e conversas"""
    
    def __init__(self):
        self.active_connections: dict = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Conecta um novo cliente"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"Cliente {user_id} conectado")
    
    def disconnect(self, user_id: int):
        """Desconecta um cliente"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"Cliente {user_id} desconectado")
    
    async def send_message(self, user_id: int, message: dict):
        """Envia mensagem para um cliente"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        """Envia mensagem para todos os clientes"""
        for user_id in self.active_connections:
            await self.send_message(user_id, message)


chat_manager = ChatManager()


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "service": "Assistente Virtual 24/7",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy"}


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """WebSocket endpoint para chat em tempo real"""
    
    await chat_manager.connect(websocket, user_id)
    
    # Mensagem de boas-vindas
    await chat_manager.send_message(user_id, {
        "type": "welcome",
        "message": "Olá! Sou o assistente da Genesys Tecnologia. Como posso ajudar?"
    })
    
    db = next(get_db())
    
    try:
        while True:
            # Receber mensagem do cliente
            data = await websocket.receive_json()
            
            user_message = data.get("message", "")
            
            logger.info(f"Usuário {user_id} enviou: {user_message}")
            
            # Salvar mensagem no banco
            chat = Chat(
                user_id=user_id,
                service="web",
                message=user_message,
                response="",  # Será preenchido após processar
                metadata={"websocket": True}
            )
            db.add(chat)
            db.commit()
            
            # Processar mensagem com IA
            response = processar_mensagem(user_message, user_id)
            
            # Atualizar chat com resposta
            chat.response = response
            db.commit()
            
            # Enviar resposta
            await chat_manager.send_message(user_id, {
                "type": "response",
                "message": response
            })
    
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id)
        db.close()
        logger.info(f"Cliente {user_id} desconectado")
    
    except Exception as e:
        logger.error(f"Erro no WebSocket: {e}")
        chat_manager.disconnect(user_id)
        db.close()


def processar_mensagem(mensagem: str, user_id: int) -> str:
    """
    Processa mensagem do usuário e retorna resposta
    
    TODO: Integrar com LLM (OpenAI/Gemini) para respostas inteligentes
    """
    
    mensagem_lower = mensagem.lower()
    
    # Processamento básico (sem IA ainda)
    if any(palavra in mensagem_lower for palavra in ['ola', 'olá', 'oi', 'hello']):
        return "Olá! Bem-vindo à Genesys Tecnologia! 🤖\n\nComo posso ajudar você hoje?"
    
    elif any(palavra in mensagem_lower for palavra in ['preco', 'preço', 'valor', 'custo', 'quanto']):
        return "💰 **Preços dos Nossos Serviços:**\n\n" \
               "• Bot de Telegram: A partir de R$ 299/mês\n" \
               "• Automação de Prazos: A partir de R$ 399/mês\n" \
               "• Assistente Virtual: A partir de R$ 499/mês\n\n" \
               "💡 Todos os planos incluem suporte completo e atualizações!"
    
    elif any(palavra in mensagem_lower for palavra in ['contato', 'falar', 'suporte']):
        return "📞 **Contato Genesys:**\n\n" \
               "📧 Email: contato@genesys-tecnologia.com.br\n" \
               "📱 WhatsApp: +55 34 99826-4603\n" \
               "🌐 Site: https://genesys-tecnologia.com.br\n\n" \
               "💬 Estamos disponíveis para esclarecer dúvidas!"
    
    elif any(palavra in mensagem_lower for palavra in ['servicos', 'serviços', 'o que', 'o que vocês fazem']):
        return "🚀 **Nossos Serviços:**\n\n" \
               "• Bot de Telegram Jurídico 🤖\n" \
               "• Automação de Prazos Processuais 📅\n" \
               "• Assistente Virtual 24/7 💬\n" \
               "• Pesquisa Jurisprudencial com IA 🔍\n" \
               "• Calculadora Trabalhista ⚖️\n\n" \
               "💡 Quer saber mais sobre algum serviço específico?"
    
    elif any(palavra in mensagem_lower for palavra in ['agendar', 'reuniao', 'reunião', 'demo']):
        return "📅 **Agendar Reunião:**\n\n" \
               "Que ótimo! Vou conectar você com nossa equipe.\n\n" \
               "📧 Envie email para: contato@genesys-tecnologia.com.br\n" \
               "📱 Ou chame no WhatsApp: +55 34 99826-4603\n\n" \
               "💬 Podemos agendar uma demo personalizada!"
    
    elif any(palavra in mensagem_lower for palavra in ['despedir', 'tchau', 'obrigado', 'obrigada']):
        return "Até logo! 👋\n\n" \
               "Foi um prazer ajudar você. Qualquer dúvida, estou aqui!\n\n" \
               "🚀 Transforme sua prática jurídica com Genesys!"
    
    else:
        return "🤖 **Assistente IA Jurídica**\n\n" \
               "Olá! Sou o assistente da Genesys Tecnologia.\n\n" \
               "Posso ajudar com:\n" \
               "• Informações sobre nossos serviços\n" \
               "• Preços e planos\n" \
               "• Agendamento de demos\n" \
               "• Contato e suporte\n\n" \
               "💡 Digite 'serviços' para ver nossa oferta completa!"


@app.post("/api/chat")
async def api_chat(message: dict):
    """API REST para chat (alternativa ao WebSocket)"""
    
    user_id = message.get("user_id")
    user_message = message.get("message")
    
    if not user_id or not user_message:
        return {"error": "user_id and message are required"}
    
    # Processar mensagem
    response = processar_mensagem(user_message, user_id)
    
    # Salvar no banco
    db = next(get_db())
    
    try:
        chat = Chat(
            user_id=user_id,
            service="api",
            message=user_message,
            response=response
        )
        db.add(chat)
        db.commit()
    finally:
        db.close()
    
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)

