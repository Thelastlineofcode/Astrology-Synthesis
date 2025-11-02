"""
Authentication API endpoints.
Provides user registration, login, JWT token refresh, and API key management.
All endpoints include comprehensive error handling and security measures.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from uuid import UUID
from backend.config.database import get_db
from backend.services.auth_service import AuthenticationService
from backend.schemas import (
    RegisterRequest, RegisterResponse, LoginRequest, LoginResponse,
    RefreshTokenRequest, RefreshTokenResponse, UserProfile,
    APIKeyCreateRequest, APIKeyResponse
)
from backend.models.database import User, AuditLog
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ============================================================================
# DEPENDENCY INJECTION - Token Verification
# ============================================================================

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Verify JWT token and return current user.
    Can be used as dependency for protected endpoints.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, credentials = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    
    payload = AuthenticationService.verify_token(credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = UUID(payload.get("user_id"))
    user = AuthenticationService.get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    return user


def get_api_key_user(
    x_api_key: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Verify API key and return associated user.
    Alternative to JWT for programmatic access.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )
    
    user = AuthenticationService.verify_api_key(db, x_api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key",
        )
    
    return user


# ============================================================================
# REGISTRATION ENDPOINT
# ============================================================================

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="Create a new user account with email and password. Returns user profile and initial API key.",
)
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: User email (must be unique)
    - **password**: Password (min 8 chars, must include uppercase + number)
    - **first_name**: User's first name
    - **last_name**: User's last name
    """
    try:
        user, api_key = AuthenticationService.register_user(db, register_data)
        
        # Log registration
        audit = AuditLog(
            user_id=user.user_id,
            action_type="USER_REGISTERED",
            resource_type="user",
            resource_id=str(user.user_id),
        )
        db.add(audit)
        db.commit()
        
        # Generate initial tokens
        access_token, refresh_token = AuthenticationService.generate_tokens(user.user_id)
        
        return RegisterResponse(
            user_id=user.user_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
            api_key=api_key,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
    
    except ValueError as e:
        logger.warning(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Registration exception: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


# ============================================================================
# LOGIN ENDPOINT
# ============================================================================

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate with email and password. Returns JWT tokens.",
)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and get JWT tokens.
    
    - **email**: User email
    - **password**: User password
    
    Returns JWT access and refresh tokens for subsequent API calls.
    """
    user = AuthenticationService.login_user(db, login_data)
    
    if not user:
        # Log failed attempt
        audit = AuditLog(
            action_type="LOGIN_FAILED",
            resource_type="user",
            resource_id=login_data.email,
        )
        db.add(audit)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Account temporarily locked. Try again in 15 minutes.",
        )
    
    # Generate tokens
    access_token, refresh_token = AuthenticationService.generate_tokens(user.user_id)
    
    # Log successful login
    audit = AuditLog(
        user_id=user.user_id,
        action_type="LOGIN_SUCCESS",
        resource_type="user",
        resource_id=str(user.user_id),
    )
    db.add(audit)
    db.commit()
    
    return LoginResponse(
        user_id=user.user_id,
        email=user.email,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


# ============================================================================
# TOKEN REFRESH ENDPOINT
# ============================================================================

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Use refresh token to get a new access token.",
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh JWT access token using refresh token.
    
    - **refresh_token**: Valid refresh token from login or registration
    
    Returns new access and refresh tokens.
    """
    payload = AuthenticationService.verify_token(refresh_data.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = UUID(payload.get("user_id"))
    user = AuthenticationService.get_user_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # Generate new tokens
    access_token, new_refresh_token = AuthenticationService.generate_tokens(user.user_id)
    
    return RefreshTokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
    )


# ============================================================================
# USER PROFILE ENDPOINT
# ============================================================================

@router.get(
    "/profile",
    response_model=UserProfile,
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Retrieve profile information for authenticated user.",
)
async def get_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user's profile.
    
    Requires valid JWT token in Authorization header.
    """
    return UserProfile(
        user_id=current_user.user_id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


# ============================================================================
# API KEY MANAGEMENT ENDPOINTS
# ============================================================================

@router.post(
    "/api-keys",
    response_model=APIKeyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new API key",
    description="Generate a new API key for programmatic access.",
)
async def create_api_key(
    request: APIKeyCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new API key for the current user.
    
    - **key_name**: Human-readable name for this API key (e.g., "mobile-app", "integration-test")
    
    Returns the raw API key (only shown once) and key ID.
    """
    try:
        raw_key, key_id = AuthenticationService.create_api_key(
            db, current_user.user_id, request.key_name
        )
        
        # Log API key creation
        audit = AuditLog(
            user_id=current_user.user_id,
            action_type="API_KEY_CREATED",
            resource_type="api_key",
            resource_id=key_id,
        )
        db.add(audit)
        db.commit()
        
        return APIKeyResponse(
            key_id=key_id,
            key_name=request.key_name,
            raw_key=raw_key,  # Only returned once
            created_at=datetime.utcnow(),
        )
    
    except Exception as e:
        logger.error(f"API key creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create API key",
        )


@router.get(
    "/api-keys",
    status_code=status.HTTP_200_OK,
    summary="List API keys",
    description="List all API keys for the current user (without showing raw keys).",
)
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List all API keys for the current user.
    
    Raw API keys are not shown for security. You can only view the key once at creation time.
    """
    keys = AuthenticationService.list_api_keys(db, current_user.user_id)
    
    return {
        "keys": [
            {
                "key_id": str(key.key_id),
                "key_name": key.key_name,
                "is_active": key.is_active,
                "created_at": key.created_at,
                "last_used_at": key.last_used_at,
            }
            for key in keys
        ]
    }


@router.delete(
    "/api-keys/{key_id}",
    status_code=status.HTTP_200_OK,
    summary="Revoke API key",
    description="Deactivate an API key. Cannot be undone; create a new key if needed.",
)
async def revoke_api_key(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Revoke (deactivate) an API key.
    
    The key can be reactivated later but the primary use case is to cycle keys for security.
    """
    try:
        key_uuid = UUID(key_id)
        success = AuthenticationService.revoke_api_key(db, key_uuid)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found",
            )
        
        # Log revocation
        audit = AuditLog(
            user_id=current_user.user_id,
            action_type="API_KEY_REVOKED",
            resource_type="api_key",
            resource_id=key_id,
        )
        db.add(audit)
        db.commit()
        
        return {"message": "API key revoked successfully"}
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid key ID format",
        )
