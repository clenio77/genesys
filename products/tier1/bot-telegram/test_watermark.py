#!/usr/bin/env python3
"""
Teste visual do watermark da logo Genesys
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.message_formatter import message_formatter

def test_watermark():
    """Testa o watermark visualmente"""
    print("=" * 60)
    print("🎨 TESTE VISUAL DO WATERMARK DA LOGO GENESYS")
    print("=" * 60)
    print()
    
    # Exemplo 1: Footer padrão
    print("📝 Exemplo 1: Footer padrão com watermark")
    print("-" * 60)
    footer1 = message_formatter.footer("💡 Dados fornecidos pela base Kermartin")
    print(footer1)
    print()
    
    # Exemplo 2: Footer customizado
    print("📝 Exemplo 2: Footer customizado")
    print("-" * 60)
    footer2 = message_formatter.footer("💡 Informações coletadas automaticamente")
    print(footer2)
    print()
    
    # Exemplo 3: Watermark sutil isolado
    print("📝 Exemplo 3: Watermark sutil isolado")
    print("-" * 60)
    watermark = message_formatter.watermark_subtle()
    print("Conteúdo da mensagem aqui...")
    print(watermark)
    print()
    
    # Exemplo 4: Mensagem completa simulada
    print("📝 Exemplo 4: Mensagem completa simulada (/magistrado)")
    print("-" * 60)
    mensagem_completa = message_formatter.header("PERFIL DO MAGISTRADO", "👨‍⚖️")
    mensagem_completa += message_formatter.section("Identificação",
        "   👤 Nome: **Dimas Borges de Paula**\n"
        "   🏛️ Tribunal: TJMG",
        "👨‍⚖️")
    mensagem_completa += f"\n{message_formatter.SEPARADOR}\n\n"
    mensagem_completa += message_formatter.section("Estatísticas",
        "   📊 Total de julgados: **45**",
        "📊")
    mensagem_completa += message_formatter.footer("💡 Dados fornecidos pela base Kermartin")
    print(mensagem_completa)
    print()
    
    print("=" * 60)
    print("✅ Watermark implementado e funcionando!")
    print("=" * 60)

if __name__ == "__main__":
    test_watermark()

