"""
Database models for Mula Dasha Timer MVP.
Uses SQLAlchemy with PostgreSQL.
"""

from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

Base = declarative_base()


class User(Base):
    """User accounts with authentication."""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255))
    
    # Birth data for chart generation
    birth_date = Column(String(10))  # YYYY-MM-DD
    birth_time = Column(String(8))   # HH:MM:SS
    birth_latitude = Column(Float)
    birth_longitude = Column(Float)
    birth_location = Column(String(255))
    timezone = Column(String(50))
    
    # Account status
    is_active = Column(Boolean, default=True, index=True)
    email_verified = Column(Boolean, default=False)
    
    # OAuth providers
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    apple_id = Column(String(255), unique=True, nullable=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    
    # Relationships
    birth_charts = relationship("BirthChart", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("NotificationToken", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")


class BirthChart(Base):
    """Birth charts with calculated data."""
    __tablename__ = "birth_charts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Birth information
    birth_date = Column(String(10), nullable=False)
    birth_time = Column(String(8), nullable=False)
    birth_latitude = Column(Float, nullable=False)
    birth_longitude = Column(Float, nullable=False)
    birth_location = Column(String(255), nullable=False)
    timezone = Column(String(50), nullable=False)
    
    # Chart calculation data (stored as JSON)
    chart_data = Column(JSON, nullable=False)  # Planets, houses, aspects, etc.
    
    # Current dasha information (denormalized for fast access)
    current_mahadasha = Column(String(50))
    current_antardasha = Column(String(50))
    current_pratyantardasha = Column(String(50))
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="birth_charts")
    dasha_periods = relationship("DashaPeriod", back_populates="birth_chart", cascade="all, delete-orphan")


class DashaPeriod(Base):
    """Vimshottari Dasha periods for timeline display."""
    __tablename__ = "dasha_periods"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    chart_id = Column(String(36), ForeignKey("birth_charts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Dasha hierarchy
    mahadasha_lord = Column(String(50), nullable=False, index=True)
    antardasha_lord = Column(String(50), nullable=True)
    pratyantardasha_lord = Column(String(50), nullable=True)
    
    # Period timing
    period_start = Column(DateTime, nullable=False, index=True)
    period_end = Column(DateTime, nullable=False, index=True)
    
    # Interpretation
    interpretation = Column(Text)
    themes = Column(JSON)  # Array of themes/keywords
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    birth_chart = relationship("BirthChart", back_populates="dasha_periods")


class Advisor(Base):
    """Advisor personalities (Papa Legba, Marie Laveau, etc.)."""
    __tablename__ = "advisors"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(100), nullable=False, unique=True)  # "Papa Legba"
    title = Column(String(255))  # "Guardian of Crossroads"
    personality_type = Column(String(50))  # "guidance", "healing", etc.
    
    # Perplexity API configuration
    system_prompt = Column(Text, nullable=False)
    knowledge_context = Column(Text)  # Additional context to inject
    
    # Display
    avatar_url = Column(String(500))
    description = Column(Text)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = relationship("Message", back_populates="advisor")


class Message(Base):
    """Messages between users and advisors."""
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    advisor_id = Column(String(36), ForeignKey("advisors.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Message content
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    
    # Context (for better responses)
    chart_context = Column(JSON)  # Current dasha, transits, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="messages")
    advisor = relationship("Advisor", back_populates="messages")


class NotificationToken(Base):
    """FCM tokens for push notifications."""
    __tablename__ = "notification_tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Token info
    fcm_token = Column(String(500), nullable=False, unique=True)
    device_type = Column(String(50))  # "ios", "android", "web"
    
    # Notification preferences
    daily_dasha_enabled = Column(Boolean, default=True)
    period_change_enabled = Column(Boolean, default=True)
    advisor_messages_enabled = Column(Boolean, default=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime, default=datetime.utcnow)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
