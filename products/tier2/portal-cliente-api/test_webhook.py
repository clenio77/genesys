#!/usr/bin/env python3
"""
Script de teste para simular novas movimentações processuais
e testar o sistema de notificações.
"""

import requests
import json

API_URL = "http://localhost:8001"

def test_webhook_movimentacao():
    """Testa o webhook de nova movimentação"""
    
    print("🔔 Simulando nova movimentação processual...\n")
    
    payload = {
        "process_cnj": "5001234-12.2024.8.13.0024",
        "title": "Sentença Publicada",
        "description": "O Juiz decidiu o seu processo. Você ganhou a causa! Verifique os detalhes no portal.",
        "icon_type": "gavel"
    }
    
    print(f"📤 Enviando para: {API_URL}/api/webhook/movimentacao")
    print(f"📋 Payload:\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n")
    
    try:
        response = requests.post(
            f"{API_URL}/api/webhook/movimentacao",
            json=payload,
            timeout=10
        )
        
        print(f"✅ Status Code: {response.status_code}\n")
        print(f"📨 Resposta:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
        
        if response.status_code == 200:
            print("✨ Sucesso! Nova movimentação registrada e notificação enviada.")
            print("\n💡 Dica: Acesse http://localhost:3000/portal-cliente")
            print("   Use CPF: 123.456.789-00")
            print("   Você verá a nova movimentação na timeline!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: API não está rodando!")
        print("   Execute: cd products/tier2/portal-cliente-api && ./run.sh")
    except Exception as e:
        print(f"❌ Erro: {e}")

def test_health_check():
    """Testa o health check"""
    print("🏥 Verificando saúde da API...\n")
    
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API está online!")
            print(f"   Serviço: {data['service']}")
            print(f"   Versão: {data['version']}\n")
            return True
        else:
            print(f"⚠️  API retornou status {response.status_code}\n")
            return False
    except:
        print("❌ API offline ou inacessível\n")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("   TESTE DE WEBHOOK - PORTAL DO CLIENTE")
    print("=" * 60)
    print()
    
    # Verificar se API está online
    if test_health_check():
        # Testar webhook
        test_webhook_movimentacao()
    else:
        print("\n💡 Certifique-se de que a API está rodando:")
        print("   cd products/tier2/portal-cliente-api")
        print("   ./run.sh")
    
    print("\n" + "=" * 60)
