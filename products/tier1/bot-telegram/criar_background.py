#!/usr/bin/env python3
"""
Script para criar imagem de fundo sutil para o chat do bot Telegram
Com logo Genesys de forma muito discreta
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL/Pillow não está instalado. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
    PIL_AVAILABLE = True

# Caminhos
BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR.parent.parent.parent / "public" / "images" / "genesys-logo.png"
OUTPUT_DIR = BASE_DIR / "backgrounds"
OUTPUT_DIR.mkdir(exist_ok=True)


def criar_background_sutil():
    """Cria imagem de fundo sutil com logo Genesys"""
    
    # Dimensões típicas para wallpaper do Telegram (mobile)
    width = 1080
    height = 1920
    
    # Criar imagem base com gradiente suave
    img = Image.new('RGB', (width, height), color='#1a1a2e')  # Cor escura elegante
    
    # Criar gradiente sutil
    draw = ImageDraw.Draw(img)
    
    # Gradiente vertical suave
    for y in range(height):
        # Variação muito sutil do escuro para um pouco mais claro
        r = int(26 + (y / height) * 5)  # 26-31 (muito escuro)
        g = int(26 + (y / height) * 5)
        b = int(46 + (y / height) * 5)  # 46-51
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    # Adicionar logo de forma muito sutil
    try:
        if LOGO_PATH.exists():
            logo = Image.open(LOGO_PATH)
            
            # Converter para RGBA se necessário
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')
            
            # Redimensionar logo (pequeno e discreto)
            logo_size = min(width, height) // 8  # 1/8 da tela
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Tornar logo muito transparente (apenas 3% de opacidade - bem sutil)
            alpha = logo.split()[3]
            alpha = alpha.point(lambda p: int(p * 0.03))  # 3% de opacidade - muito sutil
            logo.putalpha(alpha)
            
            # Posicionar no canto inferior direito (muito discreto)
            x_position = width - logo_size - 40
            y_position = height - logo_size - 100
            
            # Converter imagem base para RGBA temporariamente
            img_rgba = img.convert('RGBA')
            
            # Criar imagem temporária para composição
            temp_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            temp_img.paste(logo, (x_position, y_position), logo)
            
            # Mesclar com a imagem base
            img = Image.alpha_composite(img_rgba, temp_img).convert('RGB')
            
            print(f"✅ Logo adicionada de forma muito sutil")
        else:
            print(f"⚠️ Logo não encontrada em {LOGO_PATH}")
            print("💡 Criando fundo sem logo...")
    except Exception as e:
        print(f"⚠️ Erro ao adicionar logo: {e}")
        print("💡 Continuando sem logo...")
    
    # Adicionar padrão de pontos muito sutil (textura)
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Padrão de pontos discretos
    dot_spacing = 60
    dot_opacity = 5  # Muito transparente
    
    for x in range(0, width, dot_spacing):
        for y in range(0, height, dot_spacing):
            overlay_draw.ellipse(
                [x-2, y-2, x+2, y+2],
                fill=(255, 255, 255, dot_opacity)
            )
    
    # Mesclar padrão
    img_rgba = img.convert('RGBA')
    img = Image.alpha_composite(img_rgba, overlay).convert('RGB')
    
    # Salvar imagem principal
    output_path = OUTPUT_DIR / "genesys_chat_background.jpg"
    img.save(output_path, "JPEG", quality=85)
    
    print(f"✅ Imagem de fundo criada: {output_path}")
    print(f"📐 Dimensões: {width}x{height}px")
    print(f"💾 Tamanho: {output_path.stat().st_size / 1024:.1f} KB")
    print(f"🎨 Logo com 3% de opacidade (muito sutil)")
    
    return output_path


def criar_background_alternativo():
    """Cria versão ainda mais sutil (apenas gradiente)"""
    
    width = 1080
    height = 1920
    
    # Criar gradiente muito suave
    img = Image.new('RGB', (width, height), color='#1e293b')  # Cor escura azulada
    
    draw = ImageDraw.Draw(img)
    
    # Gradiente vertical muito sutil
    for y in range(height):
        r = int(30 + (y / height) * 3)
        g = int(41 + (y / height) * 3)
        b = int(59 + (y / height) * 3)
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)
    
    output_path = OUTPUT_DIR / "genesys_chat_background_minimal.jpg"
    img.save(output_path, "JPEG", quality=90)
    
    print(f"✅ Versão minimalista criada: {output_path}")
    return output_path


if __name__ == "__main__":
    print("=" * 60)
    print("🎨 Criando Imagem de Fundo Sutil para Chat do Bot")
    print("=" * 60)
    print()
    
    # Criar versão com logo
    path1 = criar_background_sutil()
    print()
    
    # Criar versão minimalista
    path2 = criar_background_alternativo()
    print()
    
    print("=" * 60)
    print("✅ Backgrounds criados com sucesso!")
    print("=" * 60)
    print()
    print("📱 Como aplicar no Telegram:")
    print("   1. Abra o chat com o bot")
    print("   2. Clique nos três pontos (menu)")
    print("   3. Selecione 'Papel de Parede' ou 'Background'")
    print("   4. Escolha 'Escolher da galeria'")
    print("   5. Selecione o arquivo criado")
    print()
    print(f"💡 Arquivos criados em: {OUTPUT_DIR}")

