"""
Módulo de qualificação automática de leads
"""

import sys
from pathlib import Path
from typing import Dict, Optional

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.utils.logger import setup_logger

logger = setup_logger("qualifier", "qualifier.log")


class LeadQualifier:
    """Qualifica leads automaticamente com base na conversa"""
    
    def __init__(self):
        self.score_max = 100
    
    def analisar_conversa(self, mensagens: list) -> Dict:
        """
        Analisa conversa e retorna score do lead
        
        Args:
            mensagens: Lista de mensagens trocadas
        
        Returns:
            Dict com score e informações qualificadas
        """
        
        score = 0
        dados_extraidos = {}
        
        # Analisar cada mensagem
        for msg in mensagens:
            texto = msg.get("message", "").lower()
            
            # Indicadores de interesse
            if any(palavra in texto for palavra in ['preço', 'valor', 'quanto custa']):
                score += 20
                dados_extraidos["interesse_preco"] = True
            
            if any(palavra in texto for palavra in ['agendar', 'demo', 'reunião']):
                score += 30
                dados_extraidos["interesse_compra"] = True
            
            if any(palavra in texto for palavra in ['prazo', 'urgente', 'preciso']):
                score += 15
                dados_extraidos["urgencia"] = True
            
            if any(palavra in texto for palavra in ['empresa', 'escritório', 'equipe']):
                score += 10
                dados_extraidos["empresa"] = True
            
            if any(palavra in texto for palavra in ['agora', 'imediato', 'hoje']):
                score += 20
                dados_extraidos["urgencia_alta"] = True
        
        # Determinar qualificação
        if score >= 70:
            qualificacao = "alta"
            prioridade = "alta"
        elif score >= 40:
            qualificacao = "media"
            prioridade = "media"
        else:
            qualificacao = "baixa"
            prioridade = "baixa"
        
        return {
            "score": min(score, self.score_max),
            "qualificacao": qualificacao,
            "prioridade": prioridade,
            "dados_extraidos": dados_extraidos
        }
    
    def extrair_informacoes(self, conversa: list) -> Dict:
        """Extrai informações relevantes da conversa"""
        
        informacoes = {}
        
        for msg in conversa:
            texto = msg.get("message", "")
            
            # Email
            import re
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', texto)
            if emails:
                informacoes["email"] = emails[0]
            
            # Telefone
            telefones = re.findall(r'\(?\d{2}\)?\s*\d{4,5}[\s-]?\d{4}', texto)
            if telefones:
                informacoes["telefone"] = telefones[0]
            
            # Empresa
            if any(palavra in texto.lower() for palavra in ['empresa', 'advocacia', 'escritório']):
                # Tentar extrair nome da empresa
                palavras = texto.split()
                if 'empresa' in palavras or 'chamo' in palavras:
                    idx = palavras.index('empresa') if 'empresa' in palavras else palavras.index('chamo')
                    if idx + 1 < len(palavras):
                        informacoes["empresa"] = palavras[idx + 1]
        
        return informacoes

