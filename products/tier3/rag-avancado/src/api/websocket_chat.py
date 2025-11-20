"""
WebSocket para chat em tempo real
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
from datetime import datetime
import json

from src.services import (
    QueryProcessor,
    Retriever,
    ContextBuilder,
    AnswerGenerator
)


class ConnectionManager:
    """Gerencia conexões WebSocket"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Aceita nova conexão"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        print(f"✅ Cliente conectado: {session_id}")
    
    def disconnect(self, session_id: str):
        """Remove conexão"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        print(f"❌ Cliente desconectado: {session_id}")
    
    async def send_message(self, message: dict, session_id: str):
        """Envia mensagem para cliente específico"""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)
    
    def add_to_history(self, session_id: str, query: str, answer: str):
        """Adiciona ao histórico da conversação"""
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        self.conversation_history[session_id].append({
            "query": query,
            "answer": answer,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Limitar histórico a últimas 10 interações
        if len(self.conversation_history[session_id]) > 10:
            self.conversation_history[session_id] = self.conversation_history[session_id][-10:]
    
    def get_history(self, session_id: str) -> List[Dict]:
        """Retorna histórico da sessão"""
        return self.conversation_history.get(session_id, [])


manager = ConnectionManager()


# Inicializar serviços
query_processor = QueryProcessor()
retriever = Retriever()
context_builder = ContextBuilder()
answer_generator = AnswerGenerator()


async def handle_chat_message(
    session_id: str,
    message: str
) -> Dict:
    """
    Processa mensagem do chat
    
    Args:
        session_id: ID da sessão
        message: Mensagem do usuário
        
    Returns:
        Dict com resposta
    """
    try:
        # Obter histórico
        history = manager.get_history(session_id)
        
        # Enviar status "thinking"
        await manager.send_message({
            "type": "status",
            "status": "processing",
            "message": "Processando sua pergunta..."
        }, session_id)
        
        # 1. Processar query
        processed_query = query_processor.process_query(
            message,
            {"conversation_history": history}
        )
        
        # Enviar status "searching"
        await manager.send_message({
            "type": "status",
            "status": "searching",
            "message": "Buscando documentos relevantes..."
        }, session_id)
        
        # 2. Buscar documentos
        documents = await retriever.retrieve(message, processed_query)
        
        if not documents:
            response = {
                "type": "answer",
                "answer": "Desculpe, não encontrei documentos relevantes para sua pergunta. Pode reformular?",
                "confidence": 0.0,
                "documents_found": 0
            }
            await manager.send_message(response, session_id)
            return response
        
        # Enviar status "generating"
        await manager.send_message({
            "type": "status",
            "status": "generating",
            "message": f"Encontrei {len(documents)} documentos. Gerando resposta..."
        }, session_id)
        
        # 3. Construir contexto
        context = await context_builder.build_context(
            processed_query,
            documents,
            history
        )
        
        # 4. Gerar resposta
        answer_result = await answer_generator.generate_answer(context)
        
        # Adicionar ao histórico
        manager.add_to_history(
            session_id,
            message,
            answer_result.get("answer", "")
        )
        
        # Preparar resposta
        response = {
            "type": "answer",
            "query": message,
            "answer": answer_result.get("answer"),
            "confidence": answer_result.get("confidence"),
            "documents_found": len(documents),
            "query_type": processed_query.get("query_type"),
            "entities": processed_query.get("entities", {}),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Enviar resposta final
        await manager.send_message(response, session_id)
        
        return response
    
    except Exception as e:
        error_response = {
            "type": "error",
            "error": str(e),
            "message": "Ocorreu um erro ao processar sua mensagem."
        }
        await manager.send_message(error_response, session_id)
        return error_response

