"""
SQLAlchemy database models for the Astrology-Synthesis API.
Simplified version compatible with both SQLite and PostgreSQL.
Uses String UUIDs and JSON (not JSONB) for universal compatibility.
"""

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text,
    ForeignKey, JSON, Index, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

Base = declarative_base()


# ============================================================================
# AUTHENTICATION LAYER
# ============================================================================

class User(Base):
    """Users table - user accounts with authentication."""
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(100))
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, index=True)

    # Relationships
    api_keys = relationship("APIKey", back_populates="user")
    birth_charts = relationship("BirthChart", back_populates="user")
    predictions = relationship("Prediction", back_populates="user")
    transits = relationship("Transit", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")


class APIKey(Base):
    """API Keys table - programmatic access management."""
    __tablename__ = "api_keys"

    key_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    key_name = Column(String(100), nullable=False)
    api_key_hash = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    last_used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="api_keys")


# ============================================================================
# DATA LAYER
# ============================================================================

class BirthChart(Base):
    """Birth Charts table - user's astrological birth charts."""
    __tablename__ = "birth_charts"

    chart_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    birth_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    birth_time = Column(String(8), nullable=True)    # HH:MM:SS
    birth_latitude = Column(Float, nullable=False)
    birth_longitude = Column(Float, nullable=False)
    birth_location = Column(String(255))
    timezone = Column(String(50))
    chart_data = Column(JSON, nullable=False)  # Stores computed positions
    ayanamsa = Column(String(50), default="LAHIRI")
    house_system = Column(String(50), default="PLACIDUS")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, index=True)

    # Constraints
    __table_args__ = (
        CheckConstraint("birth_latitude >= -90 AND birth_latitude <= 90"),
        CheckConstraint("birth_longitude >= -180 AND birth_longitude <= 180"),
    )

    # Relationships
    user = relationship("User", back_populates="birth_charts")
    predictions = relationship("Prediction", back_populates="birth_chart")


class Prediction(Base):
    """Predictions table - astrological predictions for users."""
    __tablename__ = "predictions"

    prediction_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    chart_id = Column(String(36), ForeignKey("birth_charts.chart_id", ondelete="CASCADE"), nullable=True, index=True)
    prediction_type = Column(String(50), nullable=False, index=True)
    prediction_date_start = Column(DateTime, nullable=False, index=True)
    prediction_date_end = Column(DateTime, nullable=True)
    confidence_score = Column(Integer, default=0)
    strength_classification = Column(String(50))
    prediction_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, index=True)

    # Constraints
    __table_args__ = (
        CheckConstraint("confidence_score >= 0 AND confidence_score <= 100"),
    )

    # Relationships
    user = relationship("User", back_populates="predictions")
    birth_chart = relationship("BirthChart", back_populates="predictions")


class Transit(Base):
    """Transits table - planetary transits and their effects."""
    __tablename__ = "transits"

    transit_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    chart_id = Column(String(36), ForeignKey("birth_charts.chart_id", ondelete="CASCADE"), nullable=True, index=True)
    transit_planet = Column(String(50), nullable=False, index=True)
    natal_planet = Column(String(50), nullable=False, index=True)
    transit_date_start = Column(DateTime, nullable=False, index=True)
    transit_date_end = Column(DateTime, nullable=True)
    orb_degrees = Column(Float)
    interpretation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="transits")


# ============================================================================
# CALCULATION LAYER (CACHING)
# ============================================================================

class KPCalculation(Base):
    """KP Calculations cache - Krishnamurthy Paddhati results."""
    __tablename__ = "kp_calculations"

    calc_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    chart_id = Column(String(36), ForeignKey("birth_charts.chart_id", ondelete="CASCADE"), nullable=False, index=True)
    calculation_type = Column(String(100), nullable=False)
    calculation_data = Column(JSON)
    confidence_score = Column(Float)
    expires_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DashaCalculation(Base):
    """Dasha Calculations cache - Vimshottari Dasha periods."""
    __tablename__ = "dasha_calculations"

    calc_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    chart_id = Column(String(36), ForeignKey("birth_charts.chart_id", ondelete="CASCADE"), nullable=False, index=True)
    mahadasha_lord = Column(String(50), index=True)
    antardasha_lord = Column(String(50))
    pratyantardasha_lord = Column(String(50))
    period_start_date = Column(DateTime)
    period_end_date = Column(DateTime)
    calculation_data = Column(JSON)
    expires_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TransitCalculation(Base):
    """Transit Calculations cache - Transit analysis results."""
    __tablename__ = "transit_calculations"

    calc_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    chart_id = Column(String(36), ForeignKey("birth_charts.chart_id", ondelete="CASCADE"), nullable=False, index=True)
    transit_date = Column(DateTime, nullable=False, index=True)
    calculation_data = Column(JSON)
    event_probability = Column(Float)
    expires_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EphemerisCache(Base):
    """Ephemeris cache - Planetary positions cache."""
    __tablename__ = "ephemeris_cache"

    cache_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    calculation_date = Column(DateTime, nullable=False, index=True)
    body = Column(String(50), nullable=False, index=True)
    position_data = Column(JSON)
    expires_at = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_ephemeris_date_body", "calculation_date", "body"),
    )


# ============================================================================
# KNOWLEDGE LAYER
# ============================================================================

class Remedy(Base):
    """Remedies table - astrological remedies and recommendations."""
    __tablename__ = "remedies"

    remedy_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    remedy_name = Column(String(255), nullable=False)
    remedy_type = Column(String(100), nullable=False, index=True)
    associated_planet = Column(String(50), index=True)
    associated_sign = Column(String(50))
    cost_estimate_low = Column(Integer)
    cost_estimate_high = Column(Integer)
    description = Column(Text)
    recommendation_timing = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Interpretation(Base):
    """Interpretations table - astrological interpretations library."""
    __tablename__ = "interpretations"

    interpretation_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    interpretation_type = Column(String(100), nullable=False, index=True)
    subject_area = Column(String(100), nullable=False, index=True)
    interpretation_text = Column(Text)
    confidence_level = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EventPattern(Base):
    """Event Patterns table - historical event patterns for validation."""
    __tablename__ = "event_patterns"

    pattern_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    pattern_name = Column(String(255), nullable=False)
    pattern_type = Column(String(100), nullable=False, index=True)
    accuracy_percentage = Column(Float)
    sample_size = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AstrologicalConstant(Base):
    """Astrological Constants table - system constants for calculations."""
    __tablename__ = "astrological_constants"

    constant_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    constant_name = Column(String(255), unique=True, nullable=False, index=True)
    constant_value = Column(Text, nullable=False)
    constant_type = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# SYSTEM LAYER
# ============================================================================

class AuditLog(Base):
    """Audit Logs table - track all significant user actions."""
    __tablename__ = "audit_logs"

    log_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True, index=True)
    action_type = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(100))
    resource_id = Column(String(100))
    changes = Column(Text)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")


class SystemSetting(Base):
    """System Settings table - configuration for API behavior."""
    __tablename__ = "system_settings"

    setting_id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    setting_name = Column(String(255), unique=True, nullable=False, index=True)
    setting_value = Column(Text, nullable=False)
    setting_type = Column(String(100), nullable=False)
    description = Column(Text)
    is_editable = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
