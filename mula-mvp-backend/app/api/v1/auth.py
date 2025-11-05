"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.core.auth import verify_password, get_password_hash, create_access_token
from app.models.database import User
from app.schemas.models import UserSignup, UserLogin, Token, OAuthRequest

router = APIRouter()


@router.post("/signup", response_model=Token)
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    """
    User registration with email and password.
    
    - Creates new user account
    - Hashes password with bcrypt
    - Returns JWT access token
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        name=user_data.name,
        is_active=True,
        email_verified=False
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": new_user.id})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    User login with email and password.
    
    - Validates credentials
    - Updates last_login_at timestamp
    - Returns JWT access token
    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # Generate JWT token
    access_token = create_access_token(data={"sub": user.id})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id
    )


@router.post("/google", response_model=Token)
async def google_oauth(oauth_data: OAuthRequest, db: Session = Depends(get_db)):
    """
    Google OAuth sign-in.
    
    - Verifies Google ID token
    - Creates user if first time
    - Returns JWT access token
    
    Note: Google ID token verification to be implemented with google-auth library
    """
    # TODO: Verify Google ID token
    # from google.oauth2 import id_token
    # from google.auth.transport import requests
    # 
    # try:
    #     idinfo = id_token.verify_oauth2_token(
    #         oauth_data.token, 
    #         requests.Request(), 
    #         settings.GOOGLE_CLIENT_ID
    #     )
    #     google_id = idinfo['sub']
    #     email = idinfo['email']
    # except ValueError:
    #     raise HTTPException(status_code=400, detail="Invalid Google token")
    
    # For now, placeholder implementation
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Google OAuth integration coming soon"
    )


@router.post("/apple", response_model=Token)
async def apple_oauth(oauth_data: OAuthRequest, db: Session = Depends(get_db)):
    """
    Apple Sign-In.
    
    - Verifies Apple ID token
    - Creates user if first time
    - Returns JWT access token
    
    Note: Apple ID token verification to be implemented with apple-auth library
    """
    # TODO: Verify Apple ID token
    # Similar to Google OAuth but with Apple's specific verification
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Apple Sign-In integration coming soon"
    )
