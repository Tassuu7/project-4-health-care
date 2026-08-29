"""
AegisCare Enterprise Patient Management System - HTTP & Security Middleware
Implements request timing, CORS headers, security policies, and audit logging hooks.
"""

import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from app.config import get_settings

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Applies modern security response headers for healthcare compliance."""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:;"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-AegisCare-Platform"] = "Enterprise-Healthcare-Core-v4.2"
        return response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    """Tracks latency of all incoming requests and attaches correlation ID."""
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.perf_counter()
        
        response = await call_next(request)
        
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time-Ms"] = f"{process_time * 1000:.2f}"
        response.headers["X-Request-ID"] = request_id
        return response
