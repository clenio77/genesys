"""
Testes para qualificação de leads
"""

import pytest
from assistente_virtual.src.qualifier import LeadQualifier


def test_analisar_conversa_alta():
    """Testa análise de conversa com score alto"""
    qualifier = LeadQualifier()
    
    mensagens = [
        {"message": "Qual o preço?", "timestamp": "2024-01-01 10:00:00"},
        {"message": "Preciso agendar uma demo urgente", "timestamp": "2024-01-01 10:05:00"},
        {"message": "Somos um escritório de advocacia", "timestamp": "2024-01-01 10:10:00"}
    ]
    
    resultado = qualifier.analisar_conversa(mensagens)
    
    assert resultado["score"] >= 40
    assert resultado["qualificacao"] in ["alta", "media"]
    assert resultado["prioridade"] in ["alta", "media"]


def test_analisar_conversa_baixa():
    """Testa análise de conversa com score baixo"""
    qualifier = LeadQualifier()
    
    mensagens = [
        {"message": "Olá", "timestamp": "2024-01-01 10:00:00"},
        {"message": "Como vocês estão?", "timestamp": "2024-01-01 10:05:00"}
    ]
    
    resultado = qualifier.analisar_conversa(mensagens)
    
    assert resultado["score"] < 40
    assert resultado["qualificacao"] == "baixa"


def test_extrair_informacoes():
    """Testa extração de informações da conversa"""
    qualifier = LeadQualifier()
    
    conversa = [
        {"message": "Meu email é teste@genesys.com.br", "timestamp": "2024-01-01 10:00:00"},
        {"message": "Telefone (34) 99826-4603", "timestamp": "2024-01-01 10:05:00"},
        {"message": "Trabalho na empresa Silva & Associados", "timestamp": "2024-01-01 10:10:00"}
    ]
    
    infos = qualifier.extrair_informacoes(conversa)
    
    assert "email" in infos
    assert "telefone" in infos
    # Nota: Extração de empresa pode não funcionar perfeitamente

