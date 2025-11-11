"""
Main FastAPI application.
Sets up the API, middleware, exception handlers, and route registration.
"""

# Load environment variables first
from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from backend.config.settings import settings
from backend.config.database import init_db
from backend.api.v1 import routes

# Configure logging
logging.basicConfig(
    level=settings.api.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    # Startup
    logger.info("🚀 Starting Astrology-Synthesis API...")
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Astrology-Synthesis API...")


# Create FastAPI app
app = FastAPI(
    title=settings.api.title,
    version=settings.api.version,
    description=settings.api.description,
    lifespan=lifespan,
)

# ============================================================================
# Middleware Setup
# ============================================================================

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trusted host middleware
# Disabled during development/testing to allow TestClient
# allowed_hosts = ["localhost", "127.0.0.1", "testserver"]  # Added testserver for testing
# if not settings.api.debug:
#     allowed_hosts = ["astrology-synthesis.com"]
# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=allowed_hosts
# )


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_code": "VALIDATION_ERROR",
            "error_message": "Request validation failed",
            "errors": exc.errors(),
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "error_message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat(),
        },
    )


# ============================================================================
# Logging Middleware
# ============================================================================

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log all HTTP requests."""
    import time
    
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # Convert to ms
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}ms"
    )
    
    # Add response time header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# ============================================================================
# Routes Registration
# ============================================================================

# Include authentication routes
app.include_router(routes.auth.router, prefix="/api/v1", tags=["Authentication"])

# Include prediction routes
app.include_router(routes.predictions.router, prefix="/api/v1", tags=["Predictions"])

# Include chart routes
app.include_router(routes.charts.router, prefix="/api/v1", tags=["Charts"])

# Include transit routes
app.include_router(routes.transits.router, prefix="/api/v1", tags=["Transits"])

# Include health routes
app.include_router(routes.health.router, prefix="/api/v1", tags=["Health"])

# Include Phase 5 LLM/Perplexity routes
app.include_router(routes.perplexity_endpoints.router, tags=["LLM & Interpretations"])

# Include Phase 5 Knowledge Base routes
app.include_router(routes.knowledge.router, tags=["Knowledge Base"])

# Include Consultant Chat routes (Mula app)
app.include_router(routes.consultant.router, prefix="/api/v1", tags=["Consultant"])

# Include Fortune Reading routes (Mula app)
app.include_router(routes.fortune.router, prefix="/api/v1", tags=["Fortune"])

# Include Personal Development routes
app.include_router(routes.personal_development.router, prefix="/api/v1", tags=["Personal Development"])

# Include Synastry routes
app.include_router(routes.synastry.router, prefix="/api/v1", tags=["Synastry"])


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Astrology-Synthesis API",
        "version": settings.api.version,
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.api.version}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.api.debug,
        log_level=settings.api.log_level.lower(),
    )
