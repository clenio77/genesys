"""
Testes para Data Extractor
"""

import pytest
from src.services.data_extractor import DataExtractor


class TestDataExtractor:
    """Testes do Data Extractor"""
    
    def test_extract_prazos(self):
        """Testa extração de prazos"""
        extractor = DataExtractor()
        
        text = "O prazo para manifestação é de 15 dias a partir de hoje."
        prazos = extractor.extract_prazos(text)
        
        assert len(prazos) > 0
        assert any("prazo" in p["text"].lower() for p in prazos)
    
    def test_extract_valores(self):
        """Testa extração de valores"""
        extractor = DataExtractor()
        
        text = "O valor da indenização é de R$ 10.000,00."
        valores = extractor.extract_valores(text)
        
        assert len(valores) > 0
        assert any(valor["value"] > 0 for valor in valores)
    
    def test_extract_cpf(self):
        """Testa extração de CPF"""
        extractor = DataExtractor()
        
        text = "CPF: 123.456.789-00"
        cpfs = extractor.extract_cpfs(text)
        
        assert len(cpfs) > 0
        assert "123.456.789-00" in cpfs or "12345678900" in "".join(cpfs)
    
    def test_extract_processo(self):
        """Testa extração de número de processo"""
        extractor = DataExtractor()
        
        text = "Processo número 0001234-56.2023.8.26.0100"
        processo = extractor.extract_processo(text)
        
        assert processo is not None
        assert "0001234" in processo

