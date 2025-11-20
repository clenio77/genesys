"""
Funções auxiliares compartilhadas
"""

from datetime import date, datetime, timedelta
from typing import Optional


def calcular_dias_restantes(data_vencimento: date) -> int:
    """Calcula quantos dias restam até o vencimento"""
    hoje = date.today()
    return (data_vencimento - hoje).days


def formatar_data_brasil(data: date) -> str:
    """Formata data para formato brasileiro"""
    return data.strftime("%d/%m/%Y")


def formatar_datetime_brasil(dt: datetime) -> str:
    """Formata datetime para formato brasileiro"""
    return dt.strftime("%d/%m/%Y %H:%M")


def obter_faixa_horario():
    """Retorna faixa de horário atual"""
    hora = datetime.now().hour
    
    if 6 <= hora < 12:
        return "manhã"
    elif 12 <= hora < 18:
        return "tarde"
    elif 18 <= hora < 22:
        return "noite"
    else:
        return "madrugada"


def obter_saudacao():
    """Retorna saudação apropriada para o horário"""
    faixa = obter_faixa_horario()
    
    saudacoes = {
        "manhã": "Bom dia",
        "tarde": "Boa tarde",
        "noite": "Boa noite",
        "madrugada": "Boa madrugada"
    }
    
    return saudacoes.get(faixa, "Olá")


def sanitizar_texto(texto: str) -> str:
    """Remove caracteres especiais e sanitiza texto"""
    import re
    # Remove caracteres especiais exceto espaços
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
    # Remove espaços duplicados
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()


def extrair_emails(texto: str) -> list:
    """Extrai emails de um texto"""
    import re
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, texto)


def extrair_telefones(texto: str) -> list:
    """Extrai telefones de um texto"""
    import re
    pattern = r'\(?\d{2}\)?\s*\d{4,5}[\s-]?\d{4}'
    return re.findall(pattern, texto)


def validar_cpf(cpf: str) -> bool:
    """Valida CPF brasileiro"""
    import re
    
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^\d]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula dígitos verificadores
    def calcula_digito(cpf, pesos):
        soma = sum(int(cpf[i]) * pesos[i] for i in range(len(cpf))))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    # Validação
    digito1 = calcula_digito(cpf[:9], list(range(10, 1, -1)))
    digito2 = calcula_digito(cpf[:10], list(range(11, 1, -1)))
    
    return cpf[-2:] == f"{digito1}{digito2}"


def validar_cnpj(cnpj: str) -> bool:
    """Valida CNPJ brasileiro"""
    import re
    
    # Remove caracteres não numéricos
    cnpj = re.sub(r'[^\d]', '', cnpj)
    
    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False
    
    # Calcula dígitos verificadores
    def calcula_digito(cnpj, pesos):
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(weights)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    
    # Validação
    digito1 = calcula_digito(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    digito2 = calcula_digito(cnpj[:13], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    
    return cnpj[-2:] == f"{digito1}{digito2}"

