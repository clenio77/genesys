"""
Cache Middleware usando Redis
Melhora performance reduzindo carga no banco
"""

import json
import hashlib
from typing import Optional, Any
from fastapi import Request
import redis


class RedisCache:
    """Wrapper para Redis cache"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """Inicializa conexão com Redis"""
        self.client = redis.from_url(
            redis_url,
            decode_responses=True,
            socket_connect_timeout=5
        )
        self.default_ttl = 3600  # 1 hora
    
    def get(self, key: str) -> Optional[Any]:
        """
        Obtém valor do cache
        
        Args:
            key: Chave do cache
        
        Returns:
            Valor cacheado ou None
        """
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
        except (redis.RedisError, json.JSONDecodeError):
            pass
        
        return None
    
    def set(
        self, 
        key: str, 
        value: Any, 
        ttl: Optional[int] = None
    ):
        """
        Armazena valor no cache
        
        Args:
            key: Chave do cache
            value: Valor para cachear
            ttl: Time to live em segundos
        """
        try:
            if ttl is None:
                ttl = self.default_ttl
            
            json_value = json.dumps(value)
            self.client.setex(key, ttl, json_value)
        except (redis.RedisError, TypeError):
            pass
    
    def delete(self, key: str):
        """Remove valor do cache"""
        try:
            self.client.delete(key)
        except redis.RedisError:
            pass
    
    def clear_pattern(self, pattern: str):
        """Limpa todos os valores que combinam com o padrão"""
        try:
            keys = self.client.keys(pattern)
            if keys:
                self.client.delete(*keys)
        except redis.RedisError:
            pass


# Instância global (será configurada na inicialização)
cache: Optional[RedisCache] = None


def init_cache(redis_url: str = "redis://localhost:6379/0"):
    """Inicializa o cache global"""
    global cache
    cache = RedisCache(redis_url)


def get_cache_key(request: Request) -> str:
    """
    Gera chave de cache baseada na requisição
    
    Args:
        request: Requisição FastAPI
    
    Returns:
        Chave de cache
    """
    # Incluir path, query params, headers relevantes
    path = str(request.url.path)
    query = str(request.url.query)
    headers = request.headers.get("authorization", "")
    
    key_string = f"{path}:{query}:{headers}"
    key_hash = hashlib.md5(key_string.encode()).hexdigest()
    
    return f"api:{key_hash}"


def cached_response(ttl: int = 3600):
    """
    Decorator para cachear respostas
    
    Args:
        ttl: Time to live em segundos
    
    Usage:
        @cached_response(ttl=300)
        async def endpoint():
            return {"data": "expensive operation"}
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Encontrar Request object
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            for key, value in kwargs.items():
                if isinstance(value, Request):
                    request = value
                    break
            
            # Se não tiver request ou cache não inicializado, chamar função direto
            if not request or not cache:
                return await func(*args, **kwargs)
            
            # Verificar cache
            cache_key = get_cache_key(request)
            cached_value = cache.get(cache_key)
            
            if cached_value:
                from fastapi.responses import JSONResponse
                return JSONResponse(cached_value)
            
            # Executar função
            result = await func(*args, **kwargs)
            
            # Cachear resultado se for JSONResponse
            if hasattr(result, 'body'):
                try:
                    import json
                    body = result.body.decode()
                    data = json.loads(body)
                    cache.set(cache_key, data, ttl)
                except:
                    pass
            
            return result
        
        return wrapper
    
    return decorator

