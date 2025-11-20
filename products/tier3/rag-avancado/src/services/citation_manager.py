"""
Microserviço 5: Citation Manager
Responsável por gerenciar citações e referências
"""

from typing import Dict, List
from datetime import datetime
import re


class CitationManager:
    """Gerencia citações e referências jurídicas"""
    
    def __init__(self):
        self.citation_cache = {}
    
    async def process_citations(
        self,
        answer: str,
        documents: List[Dict],
        query_id: int = None
    ) -> List[Dict]:
        """
        Processa citações na resposta e gera referências completas
        
        Args:
            answer: Resposta gerada com citações [Doc N]
            documents: Lista de documentos usados
            query_id: ID da query (opcional)
            
        Returns:
            Lista de citações com formato completo
        """
        # Extrair números de documentos citados
        cited_docs = self._extract_cited_documents(answer)
        
        citations = []
        for doc_num in cited_docs:
            # doc_num começa em 1, lista em 0
            doc_index = doc_num - 1
            
            if doc_index < len(documents):
                doc = documents[doc_index]
                citation = await self._format_citation(doc, doc_num, query_id)
                citations.append(citation)
        
        return citations
    
    def _extract_cited_documents(self, answer: str) -> List[int]:
        """Extrai números de documentos citados [Doc N]"""
        citations = re.findall(r'\[Doc\s+(\d+)\]', answer)
        return [int(c) for c in set(citations)]  # Remover duplicatas
    
    async def _format_citation(
        self,
        document: Dict,
        doc_number: int,
        query_id: int = None
    ) -> Dict:
        """
        Formata citação no padrão ABNT
        
        Args:
            document: Documento a ser citado
            doc_number: Número do documento na resposta
            query_id: ID da query
            
        Returns:
            Dict com citação formatada
        """
        metadata = document.get("metadata", {})
        content = document.get("content", "")
        
        # Construir citação ABNT
        abnt_citation = self._build_abnt_citation(metadata)
        
        # Extrair trecho relevante (contexto da citação)
        excerpt = self._extract_excerpt(content)
        
        citation = {
            "document_number": doc_number,
            "document_id": document.get("id"),
            "citation_abnt": abnt_citation,
            "excerpt": excerpt,
            "relevance_score": document.get("similarity_score", 0),
            "metadata": {
                "tipo": metadata.get("tipo", "Documento"),
                "tribunal": metadata.get("tribunal"),
                "data": metadata.get("data"),
                "numero_processo": metadata.get("numero_processo"),
                "magistrado": metadata.get("magistrado"),
                "assunto": metadata.get("assunto")
            },
            "url": self._build_url(metadata),
            "query_id": query_id
        }
        
        return citation
    
    def _build_abnt_citation(self, metadata: Dict) -> str:
        """Constrói citação no formato ABNT"""
        tipo = metadata.get("tipo", "Documento")
        
        if tipo == "jurisprudencia":
            return self._format_jurisprudencia_abnt(metadata)
        elif tipo == "processo":
            return self._format_processo_abnt(metadata)
        elif tipo == "legislacao":
            return self._format_legislacao_abnt(metadata)
        else:
            return self._format_generic_abnt(metadata)
    
    def _format_jurisprudencia_abnt(self, metadata: Dict) -> str:
        """Formata jurisprudência em ABNT"""
        tribunal = metadata.get("tribunal", "").upper()
        numero = metadata.get("numero_processo", "")
        data = metadata.get("data", "")
        magistrado = metadata.get("magistrado", "")
        
        parts = []
        
        if tribunal:
            parts.append(tribunal)
        
        if numero:
            parts.append(f"Processo {numero}")
        
        if magistrado:
            parts.append(f"Rel. {magistrado}")
        
        if data:
            parts.append(f"j. {data}")
        
        return ". ".join(parts) + "."
    
    def _format_processo_abnt(self, metadata: Dict) -> str:
        """Formata processo em ABNT"""
        numero = metadata.get("numero_processo", "")
        tribunal = metadata.get("tribunal", "")
        data = metadata.get("data", "")
        
        citation = f"Processo nº {numero}"
        if tribunal:
            citation += f", {tribunal}"
        if data:
            citation += f", {data}"
        
        return citation + "."
    
    def _format_legislacao_abnt(self, metadata: Dict) -> str:
        """Formata legislação em ABNT"""
        tipo_lei = metadata.get("tipo_lei", "Lei")
        numero = metadata.get("numero", "")
        data = metadata.get("data", "")
        ementa = metadata.get("ementa", "")
        
        citation = f"{tipo_lei}"
        if numero:
            citation += f" nº {numero}"
        if data:
            citation += f", de {data}"
        if ementa:
            citation += f". {ementa[:100]}..."
        
        return citation + "."
    
    def _format_generic_abnt(self, metadata: Dict) -> str:
        """Formato genérico ABNT"""
        titulo = metadata.get("titulo", "Documento")
        autor = metadata.get("autor", "")
        data = metadata.get("data", "")
        
        citation = titulo
        if autor:
            citation = f"{autor}. {citation}"
        if data:
            citation += f". {data}"
        
        return citation + "."
    
    def _extract_excerpt(self, content: str, max_length: int = 300) -> str:
        """Extrai trecho relevante do documento"""
        # Limpar e limitar
        content = content.strip()
        if len(content) <= max_length:
            return content
        
        # Tentar cortar em fim de sentença
        excerpt = content[:max_length]
        last_period = excerpt.rfind('.')
        
        if last_period > max_length * 0.7:  # Se encontrou perto do fim
            return excerpt[:last_period + 1]
        
        return excerpt + "..."
    
    def _build_url(self, metadata: Dict) -> str:
        """Constrói URL para o documento"""
        # URLs base dos tribunais
        tribunal_urls = {
            "TJMG": "https://www5.tjmg.jus.br/jurisprudencia/",
            "TJSP": "https://esaj.tjsp.jus.br/",
            "TRF1": "https://www.trf1.jus.br/",
            "STJ": "https://www.stj.jus.br/",
            "STF": "https://www.stf.jus.br/"
        }
        
        tribunal = metadata.get("tribunal", "").upper()
        numero_processo = metadata.get("numero_processo", "")
        
        if tribunal in tribunal_urls and numero_processo:
            base_url = tribunal_urls[tribunal]
            return f"{base_url}?processo={numero_processo}"
        
        return ""
    
    async def get_citation_stats(self, query_ids: List[int]) -> Dict:
        """Retorna estatísticas de citações"""
        # TODO: Implementar query ao banco
        return {
            "total_citations": 0,
            "most_cited_documents": [],
            "citation_types": {}
        }

