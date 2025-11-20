"""
Security Middleware
HTTPS enforcement, CORS, e outras medidas de segurança
"""

from fastapi import Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from typing import List


def configure_cors_seguro(app: FastAPI, allowed_origins: List[str]):
    """
    Configura CORS de forma segura
    
    Args:
        app: Aplicação FastAPI
        allowed_origins: Lista de domínios permitidos
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Content-Type", "Authorization", "X-API-Key"],
        expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining"],
        max_age=3600,
    )


async def enforce_https(request: Request, call_next):
    """
    Middleware para forçar HTTPS em produção
    
    Usage:
    @app.middleware("http")
    async def https_middleware(request: Request, call_next):
        return await enforce_https(request, call_next)
    """
    import os
    env = os.getenv("ENVIRONMENT", "development")
    
    # Apenas em produção
    if env == "production":
        # Verificar se é HTTP
        if request.url.scheme == "http":
            # Verificar header X-Forwarded-Proto
            forwarded_proto = request.headers.get("X-Forwarded-Proto")
            
            if forwarded_proto == "http":
                # Redirecionar para HTTPS
                from fastapi.responses import RedirectResponse
                url = str(request.url).replace("http://", "https://", 1)
                return RedirectResponse(url=url, status_code=status.HTTP_301_MOVED_PERMANENTLY)
    
    response = await call_next(request)
    return response


def add_security_headers(response):
    """
    Adiciona headers de segurança
    
    Headers adicionados:
    - X-Content-Type-Options: nosniff
    - X-Frame-Options: DENY
    - X-XSS-Protection: 1; mode=block
    - Strict-Transport-Security: max-age=31536000
    - Content-Security-Policy: default-src 'self'
    - Referrer-Policy: strict-origin-when-cross-origin
    - Permissions-Policy: geolocation=(), microphone=(), camera=()
    """
    # X-Content-Type-Options
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # X-Frame-Options
    response.headers["X-Frame-Options"] = "DENY"
    
    # X-XSS-Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Strict-Transport-Security
    import os
    if os.getenv("ENVIRONMENT") == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # Content-Security-Policy
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    # Referrer-Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Permissions-Policy
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    return response


def add_security_middleware(app: FastAPI):
    """Adiciona middleware de segurança à aplicação"""
    
    @app.middleware("http")
    async def security_middleware(request: Request, call_next):
        """Aplica todas as medidas de segurança"""
        
        # Forçar HTTPS em produção
        response = await enforce_https(request, call_next)
        
        # Adicionar headers de segurança
        response = add_security_headers(response)
        
        return response

