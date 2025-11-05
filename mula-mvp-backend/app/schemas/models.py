"""
Pydantic schemas for API request/response validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ============================================================================
# Authentication Schemas
# ============================================================================

class UserSignup(BaseModel):
    """User signup request."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = None


class UserLogin(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: str


class OAuthRequest(BaseModel):
    """OAuth callback request."""
    token: str  # Google/Apple ID token
    name: Optional[str] = None


# ============================================================================
# Birth Chart Schemas
# ============================================================================

class ChartCreate(BaseModel):
    """Birth chart creation request."""
    birth_date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')  # YYYY-MM-DD
    birth_time: str = Field(..., pattern=r'^\d{2}:\d{2}:\d{2}$')  # HH:MM:SS
    birth_latitude: float = Field(..., ge=-90, le=90)
    birth_longitude: float = Field(..., ge=-180, le=180)
    birth_location: str
    timezone: str


class ChartResponse(BaseModel):
    """Birth chart response."""
    id: str
    user_id: str
    birth_date: str
    birth_time: str
    birth_location: str
    chart_data: dict
    current_mahadasha: Optional[str]
    current_antardasha: Optional[str]
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Dasha Schemas
# ============================================================================

class DashaPeriodResponse(BaseModel):
    """Dasha period response."""
    id: str
    mahadasha_lord: str
    antardasha_lord: Optional[str]
    pratyantardasha_lord: Optional[str]
    period_start: datetime
    period_end: datetime
    interpretation: Optional[str]
    themes: Optional[list]
    
    class Config:
        from_attributes = True


class CurrentDashaResponse(BaseModel):
    """Current dasha information."""
    mahadasha: str
    antardasha: str
    pratyantardasha: Optional[str]
    period_start: datetime
    period_end: datetime
    days_remaining: int
    interpretation: str
    themes: list


# ============================================================================
# Advisor Schemas
# ============================================================================

class AdvisorResponse(BaseModel):
    """Advisor information."""
    id: str
    name: str
    title: Optional[str]
    personality_type: str
    description: Optional[str]
    avatar_url: Optional[str]
    
    class Config:
        from_attributes = True


class AdvisorQuery(BaseModel):
    """Query to an advisor."""
    advisor_id: str
    question: str


class MessageResponse(BaseModel):
    """Advisor message response."""
    id: str
    advisor_id: str
    question: str
    response: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============================================================================
# Notification Schemas
# ============================================================================

class NotificationTokenRegister(BaseModel):
    """Register FCM token."""
    fcm_token: str
    device_type: str = Field(..., pattern=r'^(ios|android|web)$')


class NotificationPreferences(BaseModel):
    """Notification preferences."""
    daily_dasha_enabled: bool = True
    period_change_enabled: bool = True
    advisor_messages_enabled: bool = True


class NotificationPreferencesResponse(BaseModel):
    """Notification preferences response."""
    daily_dasha_enabled: bool
    period_change_enabled: bool
    advisor_messages_enabled: bool
    
    class Config:
        from_attributes = True
