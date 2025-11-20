"""
Microserviço 1: Query Processor
Responsável por processar e otimizar consultas do usuário
"""

import re
from typing import Dict, List, Optional
from datetime import datetime


class QueryProcessor:
    """Processa e otimiza consultas para o RAG"""
    
    def __init__(self):
        self.stop_words = self._load_stop_words()
        self.legal_terms = self._load_legal_terms()
    
    def process_query(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        Processa consulta do usuário
        
        Args:
            query: Consulta em texto livre
            context: Contexto adicional (histórico, preferências)
            
        Returns:
            Dict com query processada e metadata
        """
        # Limpar e normalizar
        cleaned_query = self._clean_query(query)
        
        # Extrair entidades jurídicas
        entities = self._extract_legal_entities(cleaned_query)
        
        # Identificar tipo de consulta
        query_type = self._identify_query_type(cleaned_query, entities)
        
        # Expandir query com sinônimos jurídicos
        expanded_query = self._expand_query(cleaned_query, entities)
        
        # Aplicar contexto se disponível
        if context:
            expanded_query = self._apply_context(expanded_query, context)
        
        return {
            "original_query": query,
            "processed_query": cleaned_query,
            "expanded_query": expanded_query,
            "query_type": query_type,
            "entities": entities,
            "metadata": {
                "has_tribunal": entities.get("tribunal") is not None,
                "has_magistrado": entities.get("magistrado") is not None,
                "has_processo": entities.get("processo") is not None,
                "complexity": self._calculate_complexity(cleaned_query, entities),
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    def _clean_query(self, query: str) -> str:
        """Limpa e normaliza a query"""
        # Lowercase
        query = query.lower().strip()
        
        # Remover caracteres especiais excessivos
        query = re.sub(r'[^\w\s\-.,?!áàâãéêíóôõúç]', '', query)
        
        # Normalizar espaços
        query = re.sub(r'\s+', ' ', query)
        
        return query
    
    def _extract_legal_entities(self, query: str) -> Dict:
        """Extrai entidades jurídicas da query"""
        entities = {}
        
        # Tribunais
        tribunais = re.findall(r'\b(tj[a-z]{2}|trf\d|tst|tse|stj|stf)\b', query)
        if tribunais:
            entities["tribunal"] = tribunais[0].upper()
        
        # Número de processo (CNJ)
        processos = re.findall(
            r'\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}',
            query
        )
        if processos:
            entities["processo"] = processos[0]
        
        # Magistrados (nomes próprios após palavras-chave)
        magistrado_match = re.search(
            r'(?:magistrad[oa]|ju[ií]z[a]?|desembargador[a]?)\s+([A-ZÁÀÂÃÉÊÍÓÔÕÚ][a-záàâãéêíóôõúç]+(?:\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚ][a-záàâãéêíóôõúç]+)*)',
            query,
            re.IGNORECASE
        )
        if magistrado_match:
            entities["magistrado"] = magistrado_match.group(1).title()
        
        # Temas jurídicos
        temas_encontrados = []
        for tema in self.legal_terms:
            if tema.lower() in query:
                temas_encontrados.append(tema)
        
        if temas_encontrados:
            entities["temas"] = temas_encontrados
        
        return entities
    
    def _identify_query_type(self, query: str, entities: Dict) -> str:
        """Identifica o tipo de consulta"""
        # Consulta específica de processo
        if entities.get("processo"):
            return "processo_especifico"
        
        # Busca por jurisprudência
        if any(word in query for word in ["jurisprudência", "decisão", "acórdão", "súmula"]):
            return "jurisprudencia"
        
        # Perfil de magistrado
        if entities.get("magistrado"):
            return "perfil_magistrado"
        
        # Legislação
        if any(word in query for word in ["lei", "artigo", "código", "constituição"]):
            return "legislacao"
        
        # Análise de tendência
        if any(word in query for word in ["tendência", "padrão", "estatística", "percentual"]):
            return "analise_tendencia"
        
        # Consulta geral semântica
        return "semantica_geral"
    
    def _expand_query(self, query: str, entities: Dict) -> str:
        """Expande query com sinônimos e termos relacionados"""
        expanded = query
        
        # Adicionar sinônimos de termos jurídicos comuns
        synonyms = {
            "ação": ["demanda", "processo", "lide"],
            "sentença": ["decisão", "julgamento"],
            "recurso": ["apelação", "agravo"],
            "dano": ["prejuízo", "lesão"],
        }
        
        for term, syns in synonyms.items():
            if term in expanded and term not in entities.get("temas", []):
                # Adicionar sinônimos relevantes
                expanded += " " + " ".join(syns[:2])
        
        return expanded
    
    def _apply_context(self, query: str, context: Dict) -> str:
        """Aplica contexto da conversa à query"""
        # Se há histórico, adicionar termos relevantes
        if history := context.get("conversation_history", []):
            last_queries = [h.get("query", "") for h in history[-3:]]
            # Extrair temas recorrentes
            recurring_terms = self._find_recurring_terms(last_queries)
            if recurring_terms:
                query += " " + " ".join(recurring_terms)
        
        return query
    
    def _find_recurring_terms(self, queries: List[str]) -> List[str]:
        """Encontra termos recorrentes em queries anteriores"""
        # Simplificado: encontrar palavras que aparecem em múltiplas queries
        all_words = []
        for q in queries:
            words = [w for w in q.split() if w not in self.stop_words]
            all_words.extend(words)
        
        # Contar ocorrências
        from collections import Counter
        word_counts = Counter(all_words)
        
        # Retornar termos que aparecem mais de uma vez
        return [word for word, count in word_counts.items() if count > 1][:3]
    
    def _calculate_complexity(self, query: str, entities: Dict) -> str:
        """Calcula complexidade da query"""
        score = 0
        
        # Tamanho da query
        word_count = len(query.split())
        if word_count > 20:
            score += 2
        elif word_count > 10:
            score += 1
        
        # Número de entidades
        entity_count = len(entities)
        if entity_count > 3:
            score += 2
        elif entity_count > 1:
            score += 1
        
        # Termos técnicos
        if entities.get("temas"):
            score += len(entities["temas"]) * 0.5
        
        # Classificar
        if score > 4:
            return "alta"
        elif score > 2:
            return "media"
        else:
            return "baixa"
    
    def _load_stop_words(self) -> set:
        """Carrega stop words em português"""
        return {
            "a", "o", "de", "da", "do", "e", "em", "para", "com", "por",
            "um", "uma", "os", "as", "dos", "das", "ao", "à", "no", "na",
            "que", "se", "foi", "são", "tem", "mais", "como"
        }
    
    def _load_legal_terms(self) -> List[str]:
        """Carrega termos jurídicos comuns"""
        return [
            "ação civil",
            "ação penal",
            "agravo",
            "apelação",
            "dano moral",
            "dano material",
            "embargos",
            "habeas corpus",
            "indenização",
            "liminar",
            "mandado de segurança",
            "prescrição",
            "recurso especial",
            "recurso extraordinário",
            "sentença",
            "tutela"
        ]

