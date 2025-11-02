"""
Authentication API endpoints - redirects to auth_endpoints for full implementation.
"""

from .auth_endpoints import router

__all__ = ["router"]



@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(register_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    - **email**: User email address (must be unique)
    - **password**: Password (min 8 characters, must include uppercase and digit)
    - **first_name**: User's first name
    - **last_name**: User's last name
    """
    try:
        user = AuthenticationService.register_user(db, register_data)
        
        # Generate initial API key
        raw_api_key, _ = AuthenticationService.generate_api_key()
        
        return RegisterResponse(
            user_id=user.user_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
            api_key=raw_api_key,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and receive JWT tokens.
    
    - **email**: User email address
    - **password**: User password
    
    Returns access and refresh tokens for API authentication.
    """
    try:
        user = AuthenticationService.login_user(db, login_data)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        
        access_token, refresh_token = AuthenticationService.generate_tokens(user.user_id)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,  # 30 minutes in seconds
            token_type="Bearer",
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(request: RefreshTokenRequest):
    """
    Refresh an expired access token.
    
    - **refresh_token**: Valid refresh token from login
    
    Returns new access token.
    """
    try:
        payload = AuthenticationService.verify_token(request.refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        
        user_id = payload.get("user_id")
        access_token, _ = AuthenticationService.generate_tokens(user_id)
        
        return RefreshTokenResponse(
            access_token=access_token,
            expires_in=30 * 60,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed",
        )


# Dependency to get current user from token
async def get_current_user(
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """
    Dependency to extract and verify current user from JWT token.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authentication scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    
    payload = AuthenticationService.verify_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    
    user_id = payload.get("user_id")
    user = AuthenticationService.get_user_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    return user


@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user = Depends(get_current_user)
):
    """Get current authenticated user's profile."""
    return UserProfile(
        user_id=current_user.user_id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        phone_number=current_user.phone_number,
        timezone=current_user.timezone,
        language=current_user.language,
        subscription_tier=current_user.subscription_tier,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        last_login_at=current_user.last_login_at,
    )
