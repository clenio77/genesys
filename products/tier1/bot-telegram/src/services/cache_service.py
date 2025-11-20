"""
Serviço de cache em memória para o bot
Gerencia cache de consultas de processos, magistrados, etc.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import threading
import time

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.utils.logger import bot_telegram_logger as logger


class CacheEntry:
    """Entrada de cache com TTL (Time To Live)"""
    
    def __init__(self, value: Any, ttl_seconds: int = 3600):
        """
        Args:
            value: Valor a ser armazenado
            ttl_seconds: Tempo de vida em segundos (padrão: 1 hora)
        """
        self.value = value
        self.created_at = datetime.now()
        self.ttl_seconds = ttl_seconds
        self.access_count = 0
        self.last_accessed = datetime.now()
    
    def is_expired(self) -> bool:
        """Verifica se a entrada expirou"""
        age = (datetime.now() - self.created_at).total_seconds()
        return age > self.ttl_seconds
    
    def access(self) -> Any:
        """Acessa a entrada e atualiza estatísticas"""
        self.access_count += 1
        self.last_accessed = datetime.now()
        return self.value
    
    def get_age_seconds(self) -> float:
        """Retorna idade da entrada em segundos"""
        return (datetime.now() - self.created_at).total_seconds()
    
    def get_size_estimate(self) -> int:
        """Estima tamanho em bytes (aproximado)"""
        import sys
        return sys.getsizeof(self.value)


class CacheService:
    """
    Serviço de cache em memória com TTL e limite de tamanho
    
    Características:
    - Cache thread-safe
    - TTL configurável por tipo de dado
    - Limite máximo de memória
    - Estatísticas de uso
    - Limpeza automática de entradas expiradas
    """
    
    # TTL padrão por tipo de dado (em segundos)
    DEFAULT_TTL = {
        'processo': 3600,      # 1 hora - processos não mudam muito
        'magistrado': 86400,    # 24 horas - perfis são estáveis
        'jurisprudencia': 1800, # 30 minutos - pode ter atualizações
        'default': 3600         # 1 hora padrão
    }
    
    # Limite máximo de memória (em MB)
    MAX_MEMORY_MB = 100
    
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = threading.RLock()  # Thread-safe
        self._stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_size_bytes': 0
        }
        
        # Iniciar limpeza automática em background
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()
        
        logger.info("✅ CacheService inicializado")
    
    def get(self, key: str, cache_type: str = 'default') -> Optional[Any]:
        """
        Obtém valor do cache
        
        Args:
            key: Chave do cache
            cache_type: Tipo de cache (afeta TTL)
            
        Returns:
            Valor armazenado ou None se não encontrado/expirado
        """
        with self._lock:
            entry = self._cache.get(key)
            
            if entry is None:
                self._stats['misses'] += 1
                logger.debug(f"Cache MISS: {key}")
                return None
            
            if entry.is_expired():
                # Remover entrada expirada
                del self._cache[key]
                self._stats['misses'] += 1
                self._stats['total_size_bytes'] -= entry.get_size_estimate()
                logger.debug(f"Cache EXPIRED: {key}")
                return None
            
            # Cache hit
            self._stats['hits'] += 1
            logger.debug(f"Cache HIT: {key} (acessado {entry.access_count} vezes)")
            return entry.access()
    
    def set(self, key: str, value: Any, cache_type: str = 'default', ttl_seconds: Optional[int] = None):
        """
        Armazena valor no cache
        
        Args:
            key: Chave do cache
            value: Valor a armazenar
            cache_type: Tipo de cache (afeta TTL padrão)
            ttl_seconds: TTL específico (sobrescreve padrão do tipo)
        """
        with self._lock:
            # Determinar TTL
            if ttl_seconds is None:
                ttl_seconds = self.DEFAULT_TTL.get(cache_type, self.DEFAULT_TTL['default'])
            
            # Verificar limite de memória antes de adicionar
            current_size_mb = self._stats['total_size_bytes'] / (1024 * 1024)
            
            if current_size_mb >= self.MAX_MEMORY_MB:
                # Tentar limpar cache expirado primeiro
                self._cleanup_expired()
                current_size_mb = self._stats['total_size_bytes'] / (1024 * 1024)
                
                # Se ainda estiver no limite, remover entradas menos usadas
                if current_size_mb >= self.MAX_MEMORY_MB:
                    self._evict_least_used()
            
            # Criar entrada
            entry = CacheEntry(value, ttl_seconds)
            
            # Remover entrada antiga se existir
            if key in self._cache:
                old_entry = self._cache[key]
                self._stats['total_size_bytes'] -= old_entry.get_size_estimate()
            
            # Adicionar nova entrada
            self._cache[key] = entry
            self._stats['total_size_bytes'] += entry.get_size_estimate()
            
            logger.debug(f"Cache SET: {key} (TTL: {ttl_seconds}s, tipo: {cache_type})")
    
    def delete(self, key: str):
        """Remove entrada do cache"""
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                self._stats['total_size_bytes'] -= entry.get_size_estimate()
                del self._cache[key]
                logger.debug(f"Cache DELETE: {key}")
    
    def clear(self):
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
            self._stats['total_size_bytes'] = 0
            logger.info("Cache CLEARED")
    
    def _cleanup_expired(self):
        """Remove entradas expiradas"""
        expired_keys = []
        
        for key, entry in self._cache.items():
            if entry.is_expired():
                expired_keys.append(key)
        
        for key in expired_keys:
            entry = self._cache[key]
            self._stats['total_size_bytes'] -= entry.get_size_estimate()
            del self._cache[key]
        
        if expired_keys:
            logger.debug(f"Removidas {len(expired_keys)} entradas expiradas do cache")
    
    def _evict_least_used(self, count: int = 10):
        """Remove entradas menos usadas quando cache está cheio"""
        if len(self._cache) == 0:
            return
        
        # Ordenar por número de acessos e última vez acessado
        entries = [(key, entry) for key, entry in self._cache.items()]
        entries.sort(key=lambda x: (x[1].access_count, x[1].last_accessed))
        
        # Remover as menos usadas
        to_remove = min(count, len(entries))
        for i in range(to_remove):
            key, entry = entries[i]
            self._stats['total_size_bytes'] -= entry.get_size_estimate()
            del self._cache[key]
            self._stats['evictions'] += 1
        
        logger.info(f"Evictadas {to_remove} entradas do cache (memória cheia)")
    
    def _cleanup_loop(self):
        """Loop de limpeza automática em background"""
        while True:
            try:
                time.sleep(300)  # Limpar a cada 5 minutos
                with self._lock:
                    self._cleanup_expired()
            except Exception as e:
                logger.error(f"Erro no loop de limpeza do cache: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        with self._lock:
            total_requests = self._stats['hits'] + self._stats['misses']
            hit_rate = (self._stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'entries': len(self._cache),
                'hits': self._stats['hits'],
                'misses': self._stats['misses'],
                'hit_rate_percent': round(hit_rate, 2),
                'evictions': self._stats['evictions'],
                'memory_mb': round(self._stats['total_size_bytes'] / (1024 * 1024), 2),
                'max_memory_mb': self.MAX_MEMORY_MB,
                'memory_usage_percent': round((self._stats['total_size_bytes'] / (1024 * 1024)) / self.MAX_MEMORY_MB * 100, 2)
            }
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Retorna informações detalhadas de memória"""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            return {
                'rss_mb': round(memory_info.rss / (1024 * 1024), 2),  # Resident Set Size
                'vms_mb': round(memory_info.vms / (1024 * 1024), 2),  # Virtual Memory Size
                'cache_mb': round(self._stats['total_size_bytes'] / (1024 * 1024), 2),
                'cache_entries': len(self._cache),
                'psutil_available': True
            }
        except ImportError:
            # psutil não disponível - retornar informações básicas
            return {
                'cache_mb': round(self._stats['total_size_bytes'] / (1024 * 1024), 2),
                'cache_entries': len(self._cache),
                'psutil_available': False,
                'note': 'Instale psutil para informações detalhadas de memória'
            }


# Instância global do cache
cache_service = CacheService()

