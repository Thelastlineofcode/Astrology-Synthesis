"""
Performance Monitoring Middleware for FastAPI
"""
import time
import sentry_sdk
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable


class PerformanceMiddleware(BaseHTTPMiddleware):
    """
    Middleware to monitor API performance and log slow endpoints.
    """
    
    def __init__(self, app, slow_threshold_seconds: float = 1.0):
        super().__init__(app)
        self.slow_threshold = slow_threshold_seconds
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Start timer
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Add performance header
        response.headers["X-Process-Time"] = str(duration)
        
        # Log slow endpoints
        if duration > self.slow_threshold:
            message = f"Slow API endpoint: {request.method} {request.url.path}"
            
            # Send to Sentry if configured
            try:
                sentry_sdk.capture_message(
                    message,
                    level="warning",
                    contexts={
                        "performance": {
                            "duration_ms": duration * 1000,
                            "method": request.method,
                            "path": request.url.path,
                            "status_code": response.status_code,
                        }
                    }
                )
            except Exception:
                pass  # Sentry not configured or failed
            
            # Also log to console
            print(f"⚠️  {message} - {duration:.2f}s")
        
        return response
