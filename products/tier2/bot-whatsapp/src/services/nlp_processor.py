"""
NLP Processor - Análise de intenção e sentiment analysis
"""

import re
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Intent:
    """Representa uma intenção detectada"""
    name: str
    confidence: float
    entities: Dict[str, str]


@dataclass
class Sentiment:
    """Análise de sentimento"""
    label: str  # positive, neutral, negative
    score: float


class NLPProcessor:
    """Processa linguagem natural das mensagens"""
    
    def __init__(self):
        self.intents = {
            'saudacao': ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'hello'],
            'ajuda': ['ajuda', 'help', 'como funciona', 'quais opções'],
            'consulta': ['consultar', 'buscar', 'pesquisar', 'encontrar', 'procurar'],
            'agendamento': ['agendar', 'marcar', 'consulta', 'horário', 'disponibilidade'],
            'prazo': ['prazo', 'prazos', 'vencimento', 'dias restantes'],
            'preco': ['preço', 'valor', 'custo', 'quanto', 'tarifa'],
            'contato': ['contato', 'telefone', 'email', 'endereço', 'localização']
        }
        
        self.stop_words = {
            'de', 'da', 'do', 'das', 'dos',
            'em', 'na', 'no', 'nas', 'nos',
            'a', 'o', 'as', 'os',
            'e', 'ou', 'mas', 'para', 'com',
            'um', 'uma', 'uns', 'umas'
        }
    
    def tokenize(self, text: str) -> List[str]:
        """Tokeniza o texto removendo stop words"""
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        
        # Remover stop words
        tokens = [t for t in tokens if t not in self.stop_words]
        
        return tokens
    
    def detect_intent(self, text: str) -> Intent:
        """
        Detecta a intenção da mensagem
        
        Args:
            text: Texto da mensagem
        
        Returns:
            Intent detectado
        """
        tokens = self.tokenize(text)
        text_lower = text.lower()
        
        scores = {}
        
        for intent_name, keywords in self.intents.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            
            if len(tokens) > 0:
                scores[intent_name] = score / len(tokens)
            else:
                scores[intent_name] = 0
        
        # Encontrar melhor intent
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]
        
        return Intent(
            name=best_intent,
            confidence=confidence,
            entities={}
        )
    
    def analyze_sentiment(self, text: str) -> Sentiment:
        """
        Analisa o sentimento da mensagem
        
        Args:
            text: Texto da mensagem
        
        Returns:
            Sentiment analysis
        """
        positive_words = ['obrigado', 'obrigada', 'ótimo', 'excelente', 'perfeito', 'ótima', 'fantástico']
        negative_words = ['ruim', 'terrível', 'horrível', 'péssimo', 'não gostei', 'insatisfeito']
        
        text_lower = text.lower()
        
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        if positive_score > negative_score:
            return Sentiment('positive', min(1.0, positive_score / len(text.split())))
        elif negative_score > positive_score:
            return Sentiment('negative', min(1.0, negative_score / len(text.split())))
        else:
            return Sentiment('neutral', 0.5)
    
    def extract_entities(self, text: str) -> Dict[str, str]:
        """
        Extrai entidades do texto
        
        Args:
            text: Texto da mensagem
        
        Returns:
            Dict com entidades extraídas
        """
        entities = {}
        
        # Extrair email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            entities['email'] = emails[0]
        
        # Extrair telefone
        phone_pattern = r'(\+?55\s?)?(\d{2}\s?)?\d{4,5}-?\d{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            entities['phone'] = phones[0]
        
        # Extrair prazos (números + dias)
        prazo_pattern = r'(\d+)\s*(dias?|d)'
        prazos = re.findall(prazo_pattern, text)
        if prazos:
            entities['prazo_dias'] = prazos[0][0]
        
        # Extrair valores
        valor_pattern = r'R\$\s?(\d+(?:\.\d{3})*(?:,\d{2})?)'
        valores = re.findall(valor_pattern, text)
        if valores:
            entities['valor'] = valores[0]
        
        return entities

