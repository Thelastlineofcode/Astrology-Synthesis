"""
Database connection and session management.
Handles SQLAlchemy engine, session factory, and dependency injection.
Supports both SQLite (development) and PostgreSQL (production).
"""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool, StaticPool
from backend.config.settings import settings
from backend.models.database import Base
import logging

logger = logging.getLogger(__name__)


# Determine which connection pool to use based on database driver
if "sqlite" in settings.database.url:
    # SQLite: Use StaticPool for thread safety
    engine = create_engine(
        settings.database.url,
        echo=settings.api.debug,
        connect_args={"timeout": 15, "check_same_thread": False},
        poolclass=StaticPool,  # Required for SQLite thread safety
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
        
    logger.info(f"✅ SQLite database configured: {settings.database.sqlite_db_path}")
else:
    # PostgreSQL: Use NullPool for production
    engine = create_engine(
        settings.database.url,
        echo=settings.api.debug,
        pool_pre_ping=True,  # Verify connections before using
        poolclass=NullPool,  # Disable pooling for simplicity (enable for production)
    )
    logger.info(f"✅ PostgreSQL database configured: {settings.database.host}:{settings.database.port}")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency injection for database session.
    Yields a session for the request duration.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database (create tables)."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {str(e)}")
        raise


def drop_db():
    """Drop all tables (for testing/cleanup)."""
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ Database tables dropped successfully")
    except Exception as e:
        logger.error(f"❌ Database drop failed: {str(e)}")
        raise
