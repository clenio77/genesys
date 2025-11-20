#!/usr/bin/env python3
"""
Script de teste para verificar cache e memória do bot
"""

import sys
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.cache_service import cache_service
from services.cnj_service import cnj_service
import time


def test_cache():
    """Testa funcionalidades do cache"""
    print("=" * 60)
    print("🧪 TESTE DE CACHE E MEMÓRIA")
    print("=" * 60)
    
    # Limpar cache inicial
    cache_service.clear()
    print("\n✅ Cache limpo")
    
    # Teste 1: Armazenar e recuperar
    print("\n📝 Teste 1: Armazenar e recuperar")
    test_data = {"numero": "1234567-89.2024.8.13.0702", "classe": "Teste"}
    cache_service.set("test:processo:1", test_data, cache_type='processo')
    
    retrieved = cache_service.get("test:processo:1", cache_type='processo')
    if retrieved == test_data:
        print("   ✅ Dados recuperados corretamente")
    else:
        print("   ❌ Erro ao recuperar dados")
    
    # Teste 2: Cache miss
    print("\n📝 Teste 2: Cache miss")
    miss_result = cache_service.get("test:inexistente", cache_type='processo')
    if miss_result is None:
        print("   ✅ Cache miss funcionando corretamente")
    else:
        print("   ❌ Erro: deveria retornar None")
    
    # Teste 3: Expiração (simular)
    print("\n📝 Teste 3: TTL e expiração")
    cache_service.set("test:temp", {"data": "temporario"}, cache_type='processo', ttl_seconds=1)
    time.sleep(0.5)
    temp_result = cache_service.get("test:temp", cache_type='processo')
    if temp_result is not None:
        print("   ✅ Dados ainda válidos (< 1s)")
    else:
        print("   ❌ Erro: dados expiraram muito cedo")
    
    time.sleep(0.6)
    temp_result = cache_service.get("test:temp", cache_type='processo')
    if temp_result is None:
        print("   ✅ Dados expirados corretamente (> 1s)")
    else:
        print("   ❌ Erro: dados não expiraram")
    
    # Teste 4: Integração com CNJ Service
    print("\n📝 Teste 4: Integração com CNJ Service")
    print("   (Usando processo de teste - pode não encontrar)")
    resultado = cnj_service.consultar_processo("0000000-00.2024.8.13.0000")
    print(f"   Resultado: {'Encontrado' if resultado and 'erro' not in resultado else 'Não encontrado (esperado)'}")
    
    # Teste 5: Estatísticas
    print("\n📝 Teste 5: Estatísticas")
    stats = cache_service.get_stats()
    print(f"   Entradas: {stats['entries']}")
    print(f"   Hits: {stats['hits']}")
    print(f"   Misses: {stats['misses']}")
    print(f"   Taxa de acerto: {stats['hit_rate_percent']}%")
    print(f"   Memória usada: {stats['memory_mb']} MB")
    
    # Teste 6: Informações de memória
    print("\n📝 Teste 6: Informações de memória")
    memory_info = cache_service.get_memory_info()
    print(f"   Cache: {memory_info['cache_mb']} MB")
    print(f"   Entradas: {memory_info['cache_entries']}")
    if memory_info.get('psutil_available'):
        print(f"   RSS: {memory_info['rss_mb']} MB")
        print(f"   VMS: {memory_info['vms_mb']} MB")
    else:
        print(f"   ⚠️  psutil não disponível: {memory_info.get('note', '')}")
    
    print("\n" + "=" * 60)
    print("✅ TESTES CONCLUÍDOS")
    print("=" * 60)
    
    # Mostrar estatísticas finais
    print("\n📊 Estatísticas Finais:")
    final_stats = cache_service.get_stats()
    for key, value in final_stats.items():
        print(f"   {key}: {value}")


if __name__ == '__main__':
    test_cache()

