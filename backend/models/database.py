"""
SQLAlchemy database models for the Astrology-Synthesis API.
Defines all tables for users, charts, predictions, transits, and caching.
"""

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, 
    ForeignKey, Enum, Index, CheckConstraint, JSONB, INET, LargeBinary
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

Base = declarative_base()


class SubscriptionTierEnum(str, enum.Enum):
    """Subscription tier levels."""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class DeviceTypeEnum(str, enum.Enum):
    """Device types for sessions."""
    MOBILE = "mobile"
    DESKTOP = "desktop"
    TABLET = "tablet"
    OTHER = "other"


class User(Base):
    """User account model."""
    
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime, nullable=True)
    password_hash = Column(String(255), nullable=False)
    password_changed_at = Column(DateTime, default=datetime.utcnow)
    
    # Profile
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    phone_number = Column(String(20), nullable=True)
    timezone = Column(String(50), default="UTC")
    language = Column(String(10), default="en")
    
    # Subscription
    subscription_tier = Column(String(50), default="free")
    subscription_started_at = Column(DateTime, default=datetime.utcnow)
    subscription_expires_at = Column(DateTime, nullable=True)
    subscription_cancelled_at = Column(DateTime, nullable=True)
    
    # API Access
    api_key_hash = Column(String(255), unique=True, nullable=True)
    api_key_created_at = Column(DateTime, nullable=True)
    
    # Account Status
    is_active = Column(Boolean, default=True, index=True)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    # Metadata
    last_login_at = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)  # Soft delete
    
    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    birth_charts = relationship("BirthChart", back_populates="user", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")
    transits = relationship("Transit", back_populates="user", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint("email ~ '^[^@]+@[^@]+\\.[^@]+$'", name="email_format"),
    )


class Session(Base):
    """User session model for JWT token management."""
    
    __tablename__ = "sessions"
    
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    
    access_token_hash = Column(String(255), unique=True, nullable=False)
    refresh_token_hash = Column(String(255), unique=True, nullable=False)
    
    access_token_expires_at = Column(DateTime, nullable=False)
    refresh_token_expires_at = Column(DateTime, nullable=False)
    
    # Session Details
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    device_type = Column(String(50), nullable=True)
    device_os = Column(String(50), nullable=True)
    
    is_valid = Column(Boolean, default=True, index=True)
    revoked_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    last_activity_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="sessions")


class BirthChart(Base):
    """Birth chart storage model."""
    
    __tablename__ = "birth_charts"
    
    chart_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    
    # Birth Data
    birth_date = Column(DateTime, nullable=False)
    birth_latitude = Column(Float, nullable=False)
    birth_longitude = Column(Float, nullable=False)
    birth_timezone = Column(String(50), nullable=False)
    birth_location_name = Column(String(255), nullable=True)
    
    # Chart Data (Stored as JSON for flexibility)
    chart_data = Column(JSONB, nullable=False)  # Stores computed positions
    
    # Ayanamsa
    ayanamsa = Column(Float, default=24.147)  # Lahiri default
    
    # Metadata
    name = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    is_favorite = Column(Boolean, default=False)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="birth_charts")
    predictions = relationship("Prediction", back_populates="birth_chart")
    transits = relationship("Transit", back_populates="birth_chart")


class Prediction(Base):
    """Stored prediction model."""
    
    __tablename__ = "predictions"
    
    prediction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    chart_id = Column(UUID(as_uuid=True), ForeignKey("birth_charts.chart_id", ondelete="CASCADE"), index=True)
    
    # Query
    query_text = Column(Text, nullable=False)
    query_date = Column(DateTime, default=datetime.utcnow)
    
    # Prediction Window
    prediction_start_date = Column(DateTime, nullable=False)
    prediction_end_date = Column(DateTime, nullable=False)
    
    # Results
    prediction_data = Column(JSONB, nullable=False)  # All prediction events
    confidence_score = Column(Float, nullable=False)  # 0-1 score
    
    # Synthesis Details
    kp_contribution = Column(Float, nullable=True)      # KP score
    dasha_contribution = Column(Float, nullable=True)   # Dasha score
    transit_contribution = Column(Float, nullable=True) # Transit score
    
    # Metadata
    model_version = Column(String(50), nullable=False)  # Track model version
    calculation_time_ms = Column(Integer, nullable=True)
    
    # User Feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 star rating
    user_feedback = Column(Text, nullable=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="predictions")
    birth_chart = relationship("BirthChart", back_populates="predictions")
    events = relationship("PredictionEvent", back_populates="prediction", cascade="all, delete-orphan")
    remedies = relationship("PredictionRemedy", back_populates="prediction", cascade="all, delete-orphan")


class PredictionEvent(Base):
    """Individual prediction events."""
    
    __tablename__ = "prediction_events"
    
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.prediction_id", ondelete="CASCADE"), index=True)
    
    # Event Details
    event_type = Column(String(100), nullable=False)  # e.g., "transit", "dasha_change", "aspect"
    event_date = Column(DateTime, nullable=False, index=True)
    event_window_start = Column(DateTime, nullable=False)
    event_window_end = Column(DateTime, nullable=False)
    
    # Planets/Houses Involved
    primary_planet = Column(String(50), nullable=True)
    secondary_planet = Column(String(50), nullable=True)
    houses_involved = Column(String(100), nullable=True)  # Comma-separated
    
    # Event Strength
    strength_score = Column(Float, nullable=False)  # 0-1
    influence_area = Column(String(100), nullable=True)  # e.g., "career", "relationships", "finance"
    
    # Description
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    prediction = relationship("Prediction", back_populates="events")


class Transit(Base):
    """Current transit analysis model."""
    
    __tablename__ = "transits"
    
    transit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    chart_id = Column(UUID(as_uuid=True), ForeignKey("birth_charts.chart_id", ondelete="CASCADE"), index=True)
    
    # Transit Date
    transit_date = Column(DateTime, nullable=False, index=True)
    
    # Transit Data
    transit_data = Column(JSONB, nullable=False)
    
    # Analysis
    significant_transits = Column(JSONB, nullable=False)  # Array of significant transits
    overall_influence = Column(String(50), nullable=False)  # positive, neutral, negative
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transits")
    birth_chart = relationship("BirthChart", back_populates="transits")


class Remedy(Base):
    """Remediation recommendations model."""
    
    __tablename__ = "remedies"
    
    remedy_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Remedy Details
    remedy_type = Column(String(100), nullable=False)  # mantra, gemstone, ritual, charity, etc.
    planet_associated = Column(String(50), nullable=False)
    house_associated = Column(Integer, nullable=True)
    
    # Description
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    procedure = Column(Text, nullable=False)
    duration_days = Column(Integer, nullable=True)
    cost_estimate = Column(String(100), nullable=True)
    
    # Efficacy
    efficacy_score = Column(Float, nullable=True)  # 0-1 based on historical data
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prediction_remedies = relationship("PredictionRemedy", back_populates="remedy")


class PredictionRemedy(Base):
    """Association between predictions and remedies."""
    
    __tablename__ = "prediction_remedies"
    
    prediction_remedy_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.prediction_id", ondelete="CASCADE"), index=True)
    remedy_id = Column(UUID(as_uuid=True), ForeignKey("remedies.remedy_id", ondelete="CASCADE"), index=True)
    
    # Relationship Details
    recommendation_strength = Column(Float, nullable=False)  # 0-1
    recommended_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    
    # User Feedback
    effectiveness_rating = Column(Integer, nullable=True)  # 1-5
    notes = Column(Text, nullable=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prediction = relationship("Prediction", back_populates="remedies")
    remedy = relationship("Remedy", back_populates="prediction_remedies")


class EphemerisCache(Base):
    """Cached ephemeris calculations for performance."""
    
    __tablename__ = "ephemeris_cache"
    
    cache_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Cache Key
    calculation_date = Column(DateTime, nullable=False, index=True)
    calculation_type = Column(String(100), nullable=False)  # planet_position, house_cusps, etc.
    
    # Cache Data
    cached_data = Column(JSONB, nullable=False)
    
    # Cache Management
    hit_count = Column(Integer, default=0)
    last_accessed_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_ephemeris_cache_key", "calculation_date", "calculation_type", unique=True),
    )


class AuditLog(Base):
    """Audit log for tracking API activity."""
    
    __tablename__ = "audit_logs"
    
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # User Info
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    # Request Info
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    
    # Details
    request_body = Column(JSONB, nullable=True)
    response_data = Column(JSONB, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Performance
    execution_time_ms = Column(Float, nullable=True)
    
    # IP & User Agent
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index("idx_audit_logs_created_at", "created_at", postgresql_using="brin"),
    )
