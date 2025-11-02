"""
Pydantic schemas for request/response validation.
Defines data models for all API endpoints.
"""

from pydantic import BaseModel, EmailStr, Field, validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ============================================================================
# Authentication Schemas
# ============================================================================

class RegisterRequest(BaseModel):
    """User registration request."""
    
    email: EmailStr
    password: str = Field(..., min_length=8, description="Minimum 8 characters")
    first_name: str = Field(..., min_length=1, max_length=255)
    last_name: str = Field(..., min_length=1, max_length=255)
    
    @validator("password")
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class RegisterResponse(BaseModel):
    """User registration response."""
    
    user_id: UUID
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    api_key: str
    access_token: str
    refresh_token: str
    token_type: str


class LoginRequest(BaseModel):
    """User login request."""
    
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """User login response."""
    
    user_id: UUID
    email: str
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Token refresh request."""
    
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Token refresh response."""
    
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


class UserProfile(BaseModel):
    """User profile information."""
    
    user_id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_verified: bool


class APIKeyCreateRequest(BaseModel):
    """API key creation request."""
    
    key_name: str = Field(..., min_length=1, max_length=100)


class APIKeyResponse(BaseModel):
    """API key response."""
    
    key_id: str
    key_name: str
    api_key: Optional[str] = None  # Only returned on creation
    created_at: datetime
    last_used_at: Optional[datetime] = None
    is_active: bool
    
    model_config = ConfigDict(exclude_none=False)


# ============================================================================
# Birth Chart Schemas
# ============================================================================

class BirthDataInput(BaseModel):
    """Birth data input schema."""
    
    date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    time: str = Field(..., description="Birth time (HH:MM:SS)")
    timezone: str = Field(..., description="Timezone (e.g., America/New_York)")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    location_name: Optional[str] = Field(None, description="Location name for reference")
    
    @validator("date")
    def validate_date_format(cls, v):
        """Validate date format."""
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        return v
    
    @validator("time")
    def validate_time_format(cls, v):
        """Validate time format."""
        try:
            datetime.strptime(v, "%H:%M:%S")
        except ValueError:
            raise ValueError("Time must be in HH:MM:SS format")
        return v


class PlanetPosition(BaseModel):
    """Planet position in birth chart."""
    
    planet: str
    zodiac_sign: str
    degree: float
    minutes: float
    seconds: float
    house: int
    retrograde: bool
    nakshatra: str
    pada: int


class HouseCusp(BaseModel):
    """House cusp information."""
    
    house: int
    zodiac_sign: str
    degree: float
    minutes: float
    seconds: float


class BirthChartData(BaseModel):
    """Complete birth chart data."""
    
    planet_positions: List[PlanetPosition]
    house_cusps: List[HouseCusp]
    ascendant: Dict[str, Any]
    midheaven: Dict[str, Any]
    aspects: List[Dict[str, Any]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "planet_positions": [
                    {
                        "planet": "Sun",
                        "zodiac_sign": "Gemini",
                        "degree": 24,
                        "minutes": 15,
                        "seconds": 30,
                        "house": 9,
                        "retrograde": False,
                        "nakshatra": "Punarvasu",
                        "pada": 3
                    }
                ],
                "house_cusps": [
                    {"house": 1, "zodiac_sign": "Libra", "degree": 10, "minutes": 30, "seconds": 0}
                ]
            }
        }


class CreateBirthChartRequest(BaseModel):
    """Create birth chart request."""
    
    birth_data: BirthDataInput
    name: Optional[str] = Field(None, description="Chart name (e.g., 'My Chart', 'John Doe')")
    notes: Optional[str] = None
    ayanamsa: Optional[float] = Field(24.147, description="Ayanamsa in degrees (default: Lahiri)")


class BirthChartResponse(BaseModel):
    """Birth chart response."""
    
    chart_id: UUID
    user_id: UUID
    birth_date: datetime
    birth_latitude: float
    birth_longitude: float
    birth_timezone: str
    birth_location_name: Optional[str]
    chart_data: BirthChartData
    ayanamsa: float
    name: Optional[str]
    created_at: datetime


# ============================================================================
# Prediction Schemas
# ============================================================================

class PredictionEventData(BaseModel):
    """Individual prediction event."""
    
    event_type: str
    event_date: datetime
    event_window_start: datetime
    event_window_end: datetime
    primary_planet: Optional[str]
    secondary_planet: Optional[str]
    strength_score: float
    influence_area: Optional[str]
    description: str
    recommendation: Optional[str]


class PredictionRequest(BaseModel):
    """Prediction request."""
    
    birth_data: BirthDataInput
    query: str = Field(..., min_length=10, description="Question or area of interest")
    prediction_window_days: int = Field(30, ge=1, le=365)
    include_remedies: bool = Field(True, description="Include remedy recommendations")
    include_multitradition: bool = Field(True, description="Include multi-tradition analysis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "birth_data": {
                    "date": "1995-06-15",
                    "time": "14:30:00",
                    "timezone": "America/New_York",
                    "latitude": 40.7128,
                    "longitude": -74.006,
                    "location_name": "New York"
                },
                "query": "When will I experience significant career advancement?",
                "prediction_window_days": 365,
                "include_remedies": True,
                "include_multitradition": True
            }
        }


class PredictionResponse(BaseModel):
    """Prediction response."""
    
    prediction_id: UUID
    user_id: UUID
    query: str
    prediction_window_start: datetime
    prediction_window_end: datetime
    confidence_score: float
    events: List[PredictionEventData]
    kp_contribution: Optional[float]
    dasha_contribution: Optional[float]
    transit_contribution: Optional[float]
    model_version: str
    calculation_time_ms: Optional[int]
    created_at: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
                "query": "When will I experience significant career advancement?",
                "confidence_score": 0.75,
                "events": [],
                "model_version": "1.0.0"
            }
        }


class PredictionWithRemedies(PredictionResponse):
    """Prediction response including remedies."""
    
    remedies: Optional[List[Dict[str, Any]]] = None


# ============================================================================
# Transit Schemas
# ============================================================================

class TransitRequest(BaseModel):
    """Transit analysis request."""
    
    birth_data: BirthDataInput
    query_date: Optional[datetime] = Field(None, description="Date to analyze (default: today)")
    window_days: int = Field(30, ge=1, le=365)


class TransitResponse(BaseModel):
    """Transit analysis response."""
    
    transit_id: UUID
    user_id: UUID
    transit_date: datetime
    significant_transits: List[Dict[str, Any]]
    overall_influence: str  # positive, neutral, negative
    created_at: datetime


# ============================================================================
# Remedy Schemas
# ============================================================================

class RemedyData(BaseModel):
    """Remedy information."""
    
    remedy_id: UUID
    remedy_type: str  # mantra, gemstone, ritual, charity, etc.
    planet_associated: str
    name: str
    description: str
    procedure: str
    duration_days: Optional[int]
    cost_estimate: Optional[str]
    efficacy_score: Optional[float]


class RemediesResponse(BaseModel):
    """Remedies response."""
    
    prediction_id: UUID
    remedies: List[RemedyData]


# ============================================================================
# User Schemas
# ============================================================================



class UpdateUserRequest(BaseModel):
    """Update user profile request."""
    
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None


# ============================================================================
# Health Check Schemas
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str  # "healthy", "degraded", "unhealthy"
    version: str
    timestamp: datetime
    database_status: str
    cache_status: str
    calculation_engines_status: str


class SystemStats(BaseModel):
    """System statistics."""
    
    total_users: int
    total_predictions: int
    total_charts: int
    api_uptime_percentage: float
    average_response_time_ms: float
    cache_hit_rate: float
    database_connections_active: int
    timestamp: datetime


# ============================================================================
# API Key Schemas
# ============================================================================

class APIKeyCreateRequest(BaseModel):
    """API key creation request."""
    
    key_name: str = Field(..., min_length=1, max_length=100)




# ============================================================================
# Error Schemas
# ============================================================================

class ErrorDetail(BaseModel):
    """Error response detail."""
    
    error_code: str
    error_message: str
    error_details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    request_id: Optional[str] = None


class ValidationError(BaseModel):
    """Validation error response."""
    
    error_code: str = "VALIDATION_ERROR"
    error_message: str = "Request validation failed"
    errors: List[Dict[str, Any]]
    timestamp: datetime
