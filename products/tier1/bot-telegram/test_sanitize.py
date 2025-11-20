#!/usr/bin/env python3
"""
Teste da função sanitize_text
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.utils.text_sanitizer import sanitize_text

# Casos de teste problemáticos
test_cases = [
    "o que é direito adquirido?",
    "oi",
    "texto com \\x inválido",
    "texto com \\x12 válido",
    "texto com \\n",
    "texto com \\t",
    "texto com \\_",
    "texto com \\*",
    "texto com \\x",
    "texto com \\x1",
    "texto com \\x12",
    "texto com \\xXY",
    "texto normal",
]

print("=" * 60)
print("🧪 TESTE DE SANITIZAÇÃO")
print("=" * 60)
print()

for i, test in enumerate(test_cases, 1):
    try:
        result = sanitize_text(test)
        print(f"✅ Teste {i}: '{test[:30]}...' → OK")
        print(f"   Resultado: '{result[:50]}...'")
    except Exception as e:
        print(f"❌ Teste {i}: '{test[:30]}...' → ERRO: {e}")
    print()

print("=" * 60)
print("✅ TESTES CONCLUÍDOS")
print("=" * 60)


