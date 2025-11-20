"""
Testes para funções auxiliares
"""

import pytest
from datetime import date, datetime
from shared.utils.helpers import (
    calcular_dias_restantes,
    formatar_data_brasil,
    sanitizar_texto,
    extrair_emails,
    extrair_telefones,
    validar_cpf,
    validar_cnpj
)


def test_calcular_dias_restantes():
    """Testa cálculo de dias restantes"""
    data_futura = date.today() + timedelta(days=10)
    assert calcular_dias_restantes(data_futura) == 10
    
    data_passada = date.today() - timedelta(days=5)
    assert calcular_dias_restantes(data_passada) == -5
    
    data_hoje = date.today()
    assert calcular_dias_restantes(data_hoje) == 0


def test_formatar_data_brasil():
    """Testa formatação de data brasileira"""
    data = date(2024, 3, 15)
    assert formatar_data_brasil(data) == "15/03/2024"


def test_sanitizar_texto():
    """Testa sanitização de texto"""
    texto_sujo = "  Teste   com    espaços    e @#$   caracteres   "
    assert sanitizar_texto(texto_sujo) == "Teste com espaços e caracteres"


def test_extrair_emails():
    """Testa extração de emails"""
    texto = "Contact me at teste@genesys.com.br or admin@example.com"
    emails = extrair_emails(texto)
    assert "teste@genesys.com.br" in emails
    assert "admin@example.com" in emails


def test_extrair_telefones():
    """Testa extração de telefones"""
    texto = "Meu telefone é (34) 99826-4603 ou 34 998264603"
    telefones = extrair_telefones(texto)
    assert len(telefones) > 0


def test_validar_cpf():
    """Testa validação de CPF"""
    # CPF válido
    cpf_valido = "12345678909"  # Exemplo de CPF válido
    assert validar_cpf(cpf_valido) == True
    
    # CPF inválido
    cpf_invalido = "11111111111"
    assert validar_cpf(cpf_invalido) == False


def test_validar_cnpj():
    """Testa validação de CNPJ"""
    # CNPJ válido
    cnpj_valido = "11222333000181"  # Exemplo de CNPJ válido
    assert validar_cnpj(cnpj_valido) == True
    
    # CNPJ inválido
    cnpj_invalido = "11111111111111"
    assert validar_cnpj(cnpj_invalido) == False

