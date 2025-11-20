"""
Utilitário para sanitização de texto
Remove caracteres problemáticos e normaliza texto para Markdown
"""

import re


def sanitize_text(text: str) -> str:
    """
    Sanitiza texto para evitar problemas com Markdown
    Remove ou escapa caracteres problemáticos
    
    CORREÇÃO CRÍTICA: Esta função deve ser chamada ANTES de qualquer processamento
    que possa tentar interpretar escapes inválidos do Python.
    
    Args:
        text: Texto a ser sanitizado
        
    Returns:
        Texto sanitizado e seguro para Markdown
    """
    if not text:
        return ""
    
    # Converter para string se necessário (de forma segura)
    if not isinstance(text, str):
        try:
            # Usar repr() e depois remover aspas para evitar interpretação de escapes
            text_repr = repr(text)
            # Remove aspas do início e fim: 'texto' -> texto
            if text_repr.startswith("'") and text_repr.endswith("'"):
                text = text_repr[1:-1]
            elif text_repr.startswith('"') and text_repr.endswith('"'):
                text = text_repr[1:-1]
            else:
                text = str(text)
        except Exception:
            return ""
    
    # ETAPA 1: Processar usando bytes para evitar interpretação de escapes pelo Python
    # Isso é crítico para evitar "incomplete escape \x"
    try:
        # Converter para bytes primeiro usando UTF-8 (sem interpretar escapes)
        # Isso remove caracteres inválidos automaticamente
        text_bytes = text.encode('utf-8', errors='ignore')
        text = text_bytes.decode('utf-8', errors='ignore')
    except Exception:
        # Se falhar, tentar método alternativo
        try:
            # Tentar processar caractere por caractere para remover inválidos
            text = ''.join(c for c in text if ord(c) < 0x110000)  # Unicode válido
        except Exception:
            pass
    
    # ETAPA 2: Processar caracteres de escape problemáticos de forma segura
    # Processar caractere por caractere para evitar problemas com regex
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        
        # Se encontrar \, verificar se é escape válido
        if char == '\\' and i + 1 < len(text):
            next_char = text[i + 1]
            
            # Escapes válidos que devem ser preservados
            valid_escapes = ['n', 't', 'r', '\\', 'a', 'b', 'f', 'v', '0']
            
            # Verificar se é \x seguido de 2 dígitos hexadecimais
            if next_char == 'x' and i + 3 < len(text):
                hex_chars = text[i+2:i+4]
                if len(hex_chars) == 2 and all(c in '0123456789abcdefABCDEF' for c in hex_chars):
                    # Escape \x válido - preservar
                    result.append(char + next_char + hex_chars)
                    i += 4
                    continue
                else:
                    # \x inválido - remover apenas o \ e continuar com o próximo caractere
                    # Isso evita que Python tente interpretar \x inválido
                    i += 1
                    continue
            
            # Verificar se é escape válido
            elif next_char in valid_escapes or (next_char.isdigit() and i + 1 < len(text)):
                # Escape válido - preservar
                result.append(char + next_char)
                i += 2
                continue
            else:
                # Escape inválido - remover apenas o \ e continuar
                # Isso evita erros de escape inválido
                i += 1
                continue
        else:
            # Caractere normal - adicionar
            result.append(char)
            i += 1
    
    text = ''.join(result)
    
    # ETAPA 3: Normalizar quebras de linha (após sanitização de escapes)
    text = text.replace('\\n', '\n')
    text = text.replace('\\r', '\r')
    text = text.replace('\\r\\n', '\n')
    
    # Preservar tabs
    text = text.replace('\\t', '\t')
    
    # ETAPA 4: Remover caracteres de controle problemáticos
    # Manter apenas caracteres imprimíveis e quebras de linha válidas
    text = ''.join(c for c in text if ord(c) >= 32 or c in ['\n', '\r', '\t'] or ord(c) == 9)
    
    # ETAPA 5: Escapar caracteres especiais do Markdown
    # Isso evita problemas de parsing no Telegram
    text = text.replace("_", "\\_")
    text = text.replace("*", "\\*")
    text = text.replace("[", "\\[")
    text = text.replace("]", "\\]")
    text = text.replace("`", "\\`")
    
    return text

