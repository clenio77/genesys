"""
Microserviço 4: Answer Generator
Responsável por gerar respostas usando GPT-4
"""

from typing import Dict, Optional
from openai import OpenAI

from src.config import Config


class AnswerGenerator:
    """Gera respostas inteligentes usando GPT-4"""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None
        self.model = Config.OPENAI_MODEL
        self.max_tokens = 2000
    
    async def generate_answer(
        self,
        context: Dict,
        temperature: float = 0.3
    ) -> Dict:
        """
        Gera resposta baseada no contexto
        
        Args:
            context: Contexto construído pelo Context Builder
            temperature: Criatividade da resposta (0-1)
            
        Returns:
            Dict com resposta e metadata
        """
        if not self.client:
            return {
                "answer": "OpenAI não configurada. Configure OPENAI_API_KEY.",
                "confidence": 0.0,
                "error": "missing_api_key"
            }
        
        try:
            # Extrair prompt formatado
            prompt = context.get("formatted_prompt", "")
            
            if not prompt:
                raise ValueError("Prompt vazio")
            
            # Chamar GPT-4
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente jurídico especializado."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=self.max_tokens,
                top_p=0.95,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extrair resposta
            answer_text = response.choices[0].message.content
            
            # Calcular confiança baseado em fatores
            confidence = self._calculate_confidence(
                response,
                context,
                answer_text
            )
            
            # Extrair citações da resposta
            citations = self._extract_citations(answer_text)
            
            return {
                "answer": answer_text,
                "confidence": confidence,
                "citations_in_answer": citations,
                "tokens_used": response.usage.total_tokens,
                "model": self.model,
                "finish_reason": response.choices[0].finish_reason
            }
        
        except Exception as e:
            print(f"❌ Erro ao gerar resposta: {e}")
            return {
                "answer": f"Erro ao gerar resposta: {str(e)}",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _calculate_confidence(
        self,
        response,
        context: Dict,
        answer: str
    ) -> float:
        """Calcula score de confiança da resposta"""
        confidence_factors = []
        
        # Fator 1: Relevância dos documentos
        avg_relevance = context.get("metadata", {}).get("avg_relevance", 0)
        confidence_factors.append(avg_relevance)
        
        # Fator 2: Número de documentos usados
        doc_count = context.get("document_count", 0)
        doc_factor = min(doc_count / 5.0, 1.0)  # Normalizar para 5 docs
        confidence_factors.append(doc_factor)
        
        # Fator 3: Presença de citações na resposta
        if "[Doc" in answer:
            citation_count = answer.count("[Doc")
            citation_factor = min(citation_count / 3.0, 1.0)
            confidence_factors.append(citation_factor)
        else:
            confidence_factors.append(0.3)
        
        # Fator 4: Tamanho da resposta (respostas muito curtas = baixa confiança)
        answer_length = len(answer.split())
        if answer_length > 50:
            confidence_factors.append(1.0)
        elif answer_length > 20:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.4)
        
        # Fator 5: Finish reason (se completou normalmente)
        finish_reason = response.choices[0].finish_reason
        if finish_reason == "stop":
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.6)
        
        # Média ponderada
        confidence = sum(confidence_factors) / len(confidence_factors)
        
        return round(confidence, 4)
    
    def _extract_citations(self, answer: str) -> list:
        """Extrai referências [Doc N] da resposta"""
        import re
        citations = re.findall(r'\[Doc\s+(\d+)\]', answer)
        return [int(c) for c in citations] if citations else []
    
    async def summarize_document(self, content: str) -> str:
        """
        Gera resumo de um documento
        
        Args:
            content: Conteúdo do documento
            
        Returns:
            Resumo do documento
        """
        if not self.client:
            return "OpenAI não configurada"
        
        try:
            prompt = f"""Resuma o seguinte documento jurídico em 2-3 parágrafos, 
destacando os pontos mais importantes:

{content[:3000]}  # Limitar para evitar excesso

RESUMO:"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um assistente especializado em resumir documentos jurídicos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"❌ Erro ao resumir documento: {e}")
            return f"Erro ao resumir: {str(e)}"

