"""
Main FastAPI application for Mula Dasha Timer MVP.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import auth, chart, dasha, advisor, notifications

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    # Startup
    logger.info("🚀 Starting Mula Dasha Timer API...")
    try:
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Mula Dasha Timer API...")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for Mula Dasha Timer MVP - Vedic astrology timing system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(chart.router, prefix=f"{settings.API_V1_PREFIX}/chart", tags=["Birth Charts"])
app.include_router(dasha.router, prefix=f"{settings.API_V1_PREFIX}/dasha", tags=["Dasha Periods"])
app.include_router(advisor.router, prefix=f"{settings.API_V1_PREFIX}/advisor", tags=["Advisors"])
app.include_router(notifications.router, prefix=f"{settings.API_V1_PREFIX}/notifications", tags=["Notifications"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Mula Dasha Timer API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Railway."""
    return {"status": "healthy"}
