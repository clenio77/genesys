"""
Rate Limiting Middleware
Protege APIs contra DDoS e abuso
"""

import time
from typing import Dict, Optional
from functools import wraps
from fastapi import Request, HTTPException, status


class RateLimiter:
    """Implementa rate limiting simples em memória"""
    
    def __init__(self):
        # {ip: [(timestamp, requests)]}
        self.requests: Dict[str, list] = {}
        self.cleanup_interval = 300  # 5 minutos
    
    def is_rate_limited(
        self, 
        ip: str, 
        max_requests: int = 100, 
        window_seconds: int = 60
    ) -> bool:
        """
        Verifica se IP excedeu limite de requisições
        
        Args:
            ip: Endereço IP
            max_requests: Máximo de requisições
            window_seconds: Janela de tempo em segundos
        
        Returns:
            True se rate limited, False caso contrário
        """
        now = time.time()
        
        # Limpar requisições antigas
        if ip in self.requests:
            self.requests[ip] = [
                (ts, count) 
                for ts, count in self.requests[ip] 
                if now - ts < window_seconds
            ]
        
        # Contar requisições na janela
        total = sum(count for _, count in self.requests.get(ip, []))
        
        if total >= max_requests:
            return True
        
        # Adicionar requisição atual
        if ip not in self.requests:
            self.requests[ip] = []
        
        self.requests[ip].append((now, 1))
        
        return False
    
    def get_rate_limit_status(self, ip: str) -> Dict:
        """Retorna status do rate limiting para um IP"""
        now = time.time()
        
        if ip not in self.requests:
            return {
                "remaining": 100,
                "reset_at": now + 60,
                "limit": 100
            }
        
        # Limpar requisições antigas
        self.requests[ip] = [
            (ts, count) 
            for ts, count in self.requests[ip] 
            if now - ts < 60
        ]
        
        total = sum(count for _, count in self.requests[ip])
        
        return {
            "remaining": max(0, 100 - total),
            "reset_at": now + 60,
            "limit": 100
        }


# Instância global
rate_limiter = RateLimiter()


def get_client_ip(request: Request) -> str:
    """Obtém IP do cliente"""
    # Verificar headers de proxy
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    return request.client.host if request.client else "unknown"


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """
    Decorator para rate limiting
    
    Args:
        max_requests: Máximo de requisições
        window_seconds: Janela de tempo em segundos
    """
    def decorator(func):
        @wraps(func)
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
            
            if not request:
                raise HTTPException(
                    status_code=500,
                    detail="Rate limiting requires Request object"
                )
            
            # Obter IP
            ip = get_client_ip(request)
            
            # Verificar rate limit
            if rate_limiter.is_rate_limited(ip, max_requests, window_seconds):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds.",
                    headers={
                        "X-RateLimit-Limit": str(max_requests),
                        "X-RateLimit-Reset": str(int(time.time()) + window_seconds)
                    }
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def rate_limit_dependency(max_requests: int = 100, window_seconds: int = 60):
    """
    Dependency para rate limiting em FastAPI
    
    Usage:
    @app.get("/api/")
    async def endpoint(request: Request, _ = Depends(rate_limit_dependency())):
        return {"message": "OK"}
    """
    async def check_rate_limit(request: Request):
        ip = get_client_ip(request)
        
        if rate_limiter.is_rate_limited(ip, max_requests, window_seconds):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds} seconds.",
                headers={
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Reset": str(int(time.time()) + window_seconds)
                }
            )
    
    return check_rate_limit

