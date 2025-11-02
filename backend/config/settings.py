"""
Configuration management for the FastAPI application.
Handles environment variables, database connections, and API settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class DatabaseConfig(BaseSettings):
    """Database configuration - supports SQLite (dev) and PostgreSQL (prod)."""
    
    driver: str = os.getenv("DB_DRIVER", "sqlite")  # "sqlite" or "postgresql"
    
    # SQLite config
    sqlite_db_path: str = os.getenv("SQLITE_DB_PATH", "./astrology_synthesis.db")
    
    # PostgreSQL config
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    user: str = os.getenv("DB_USER", "astrology_user")
    password: str = os.getenv("DB_PASSWORD", "secure_password")
    database: str = os.getenv("DB_NAME", "astrology_synthesis")
    
    @property
    def url(self) -> str:
        """Return database connection string (SQLite or PostgreSQL)."""
        if self.driver == "sqlite":
            return f"sqlite:///{self.sqlite_db_path}"
        else:
            return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    @property
    def async_url(self) -> str:
        """Return async database connection string."""
        if self.driver == "sqlite":
            # SQLite doesn't have native async, but we can use aiosqlite
            return f"sqlite+aiosqlite:///{self.sqlite_db_path}"
        else:
            return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseSettings):
    """Redis configuration."""
    
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    database: int = int(os.getenv("REDIS_DB", "0"))
    password: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    
    @property
    def url(self) -> str:
        """Return Redis connection string."""
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.database}"
        return f"redis://{self.host}:{self.port}/{self.database}"


class SecurityConfig(BaseSettings):
    """Security configuration."""
    
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # API Keys
    enable_api_key_auth: bool = os.getenv("ENABLE_API_KEY_AUTH", "true").lower() == "true"
    
    # CORS
    cors_origins: list = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]
    cors_credentials: bool = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
    cors_methods: list = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_headers: list = ["*"]


class APIConfig(BaseSettings):
    """API configuration."""
    
    title: str = "Astrology-Synthesis API"
    version: str = "1.0.0"
    description: str = "Syncretic Astrology Prediction Engine combining KP, Vedic, Vodou, Rosicrucian, and Arabic traditions"
    
    # Performance
    max_prediction_window_days: int = 365
    default_prediction_window_days: int = 30
    
    # Rate Limiting
    rate_limit_enabled: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_period_seconds: int = int(os.getenv("RATE_LIMIT_PERIOD_SECONDS", "60"))
    
    # Caching
    cache_enabled: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


class Settings(BaseSettings):
    """Main settings class combining all configurations."""
    
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    database: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    security: SecurityConfig = SecurityConfig()
    api: APIConfig = APIConfig()
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
