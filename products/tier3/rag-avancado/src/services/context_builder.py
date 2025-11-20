"""
Microserviço 3: Context Builder
Responsável por construir contexto ótimo para o LLM
"""

from typing import Dict, List
from src.config import Config


class ContextBuilder:
    """Constrói contexto otimizado para geração de respostas"""
    
    def __init__(self):
        self.max_context_length = Config.MAX_CONTEXT_LENGTH
        self.chunk_size = Config.CHUNK_SIZE
    
    async def build_context(
        self,
        query: Dict,
        documents: List[Dict],
        conversation_history: List[Dict] = None
    ) -> Dict:
        """
        Constrói contexto otimizado para o LLM
        
        Args:
            query: Query processada
            documents: Documentos recuperados
            conversation_history: Histórico de conversação
            
        Returns:
            Dict com contexto estruturado
        """
        # Ordenar documentos por relevância
        sorted_docs = sorted(
            documents,
            key=lambda x: x.get("similarity_score", 0),
            reverse=True
        )
        
        # Selecionar documentos até limite de tokens
        selected_docs = self._select_documents(sorted_docs)
        
        # Criar contexto estruturado
        context = {
            "query_info": {
                "original": query.get("original_query"),
                "processed": query.get("processed_query"),
                "type": query.get("query_type"),
                "entities": query.get("entities", {})
            },
            "documents": selected_docs,
            "document_count": len(selected_docs),
            "conversation_history": self._format_history(conversation_history),
            "metadata": {
                "total_retrieved": len(documents),
                "selected": len(selected_docs),
                "avg_relevance": self._calculate_avg_relevance(selected_docs)
            }
        }
        
        # Gerar prompt contextualizado
        context["formatted_prompt"] = self._format_prompt(context)
        
        return context
    
    def _select_documents(self, documents: List[Dict]) -> List[Dict]:
        """Seleciona documentos até limite de contexto"""
        selected = []
        total_length = 0
        
        for doc in documents:
            content = doc.get("content", "")
            # Estimativa de tokens (1 token ≈ 4 caracteres)
            doc_tokens = len(content) // 4
            
            if total_length + doc_tokens > self.max_context_length:
                # Verificar se ainda cabe um resumo
                if total_length + 200 <= self.max_context_length:
                    # Adicionar versão resumida
                    doc_copy = doc.copy()
                    doc_copy["content"] = content[:800] + "..."
                    doc_copy["truncated"] = True
                    selected.append(doc_copy)
                break
            
            selected.append(doc)
            total_length += doc_tokens
        
        return selected
    
    def _format_history(
        self,
        history: List[Dict] = None
    ) -> str:
        """Formata histórico de conversação"""
        if not history or not Config.ENABLE_HISTORY:
            return ""
        
        # Limitar a últimas N interações
        recent_history = history[-5:] if len(history) > 5 else history
        
        formatted = []
        for item in recent_history:
            query = item.get("query", "")
            answer = item.get("answer", "")
            if query and answer:
                formatted.append(f"Q: {query}\nA: {answer}")
        
        return "\n\n".join(formatted) if formatted else ""
    
    def _calculate_avg_relevance(self, documents: List[Dict]) -> float:
        """Calcula relevância média dos documentos"""
        if not documents:
            return 0.0
        
        scores = [doc.get("similarity_score", 0) for doc in documents]
        return round(sum(scores) / len(scores), 4)
    
    def _format_prompt(self, context: Dict) -> str:
        """Formata prompt completo para o LLM"""
        query_info = context["query_info"]
        documents = context["documents"]
        history = context.get("conversation_history", "")
        
        # Sistema de prompt base
        system_prompt = """Você é um assistente jurídico especializado em direito brasileiro.
Sua função é responder perguntas baseando-se em documentos jurídicos, jurisprudência e 
legislação brasileira.

INSTRUÇÕES:
1. Baseie suas respostas APENAS nos documentos fornecidos
2. Cite as fontes usando [Doc N] onde N é o número do documento
3. Se a informação não estiver nos documentos, seja honesto
4. Use linguagem clara e precisa
5. Quando relevante, cite artigos de lei e jurisprudência
6. Mantenha o tom profissional e técnico"""
        
        # Contexto da conversa
        conversation_context = ""
        if history:
            conversation_context = f"\n\nHISTÓRICO DA CONVERSA:\n{history}\n"
        
        # Entidades identificadas
        entities_context = ""
        if entities := query_info.get("entities", {}):
            entities_list = []
            if tribunal := entities.get("tribunal"):
                entities_list.append(f"Tribunal: {tribunal}")
            if magistrado := entities.get("magistrado"):
                entities_list.append(f"Magistrado: {magistrado}")
            if temas := entities.get("temas"):
                entities_list.append(f"Temas: {', '.join(temas)}")
            
            if entities_list:
                entities_context = f"\n\nENTIDADES IDENTIFICADAS:\n" + "\n".join(entities_list)
        
        # Documentos
        docs_context = "\n\nDOCUMENTOS RELEVANTES:\n"
        for i, doc in enumerate(documents, 1):
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            score = doc.get("similarity_score", 0)
            
            # Metadados importantes
            meta_str = ""
            if doc_type := metadata.get("tipo"):
                meta_str += f"Tipo: {doc_type}, "
            if tribunal := metadata.get("tribunal"):
                meta_str += f"Tribunal: {tribunal}, "
            if data := metadata.get("data"):
                meta_str += f"Data: {data}, "
            
            docs_context += f"\n[Doc {i}] ({meta_str}Relevância: {score:.2%})\n{content}\n"
        
        # Query do usuário
        user_query = f"\n\nPERGUNTA DO USUÁRIO:\n{query_info.get('original')}"
        
        # Montar prompt completo
        full_prompt = (
            system_prompt +
            conversation_context +
            entities_context +
            docs_context +
            user_query +
            "\n\nRESPOSTA:"
        )
        
        return full_prompt

