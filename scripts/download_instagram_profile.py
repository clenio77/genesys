#!/usr/bin/env python3
"""
Script para baixar imagem de perfil do Instagram
Uso: python download_instagram_profile.py <username> <output_path>
"""

import sys
import requests
import re
from pathlib import Path

def get_instagram_profile_image(username):
    """
    Tenta obter a URL da imagem de perfil do Instagram
    """
    url = f"https://www.instagram.com/{username}/"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Tentar encontrar a URL da imagem no HTML
            # Instagram usa diferentes padrões, vamos tentar alguns
            patterns = [
                r'"profile_pic_url_hd":"([^"]+)"',
                r'"profile_pic_url":"([^"]+)"',
                r'<meta property="og:image" content="([^"]+)"',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, response.text)
                if match:
                    image_url = match.group(1).replace('\\u0026', '&')
                    return image_url
        
        print(f"⚠️ Não foi possível encontrar a imagem automaticamente.")
        print(f"💡 Acesse: {url}")
        print(f"💡 Clique com botão direito na foto de perfil > 'Copiar endereço da imagem'")
        return None
        
    except Exception as e:
        print(f"❌ Erro ao acessar Instagram: {e}")
        return None

def download_image(url, output_path):
    """Baixa a imagem da URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30, stream=True)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Imagem baixada com sucesso: {output_path}")
            return True
        else:
            print(f"❌ Erro ao baixar imagem: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro ao baixar imagem: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python download_instagram_profile.py <username> [output_path]")
        print("\nExemplo:")
        print("  python download_instagram_profile.py afonso.clenio public/images/clenio.png")
        sys.exit(1)
    
    username = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else f"public/images/{username.replace('.', '_')}.png"
    
    print(f"🔍 Buscando imagem de perfil do Instagram: @{username}")
    
    image_url = get_instagram_profile_image(username)
    
    if image_url:
        print(f"📸 URL encontrada: {image_url[:80]}...")
        download_image(image_url, output_path)
    else:
        print("\n📝 Instruções manuais:")
        print(f"1. Acesse: https://www.instagram.com/{username}/")
        print("2. Clique com botão direito na foto de perfil")
        print("3. Selecione 'Copiar endereço da imagem' ou 'Inspect'")
        print(f"4. Cole a URL aqui ou baixe manualmente para: {output_path}")

