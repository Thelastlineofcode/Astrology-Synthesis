"""
Authentication service layer.
Handles user registration, login, JWT token generation, API key management, and validation.
Production-ready with bcrypt hashing, JWT tokens, and security best practices.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
from uuid import UUID, uuid4
import jwt
import hashlib
import secrets
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.models.database import User, APIKey
from backend.schemas import RegisterRequest, LoginRequest
from backend.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Password hashing context - bcrypt is production-ready
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Computational cost for bcrypt iterations
)


class AuthenticationService:
    """Authentication service for user management and JWT tokens."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def generate_tokens(user_id: UUID) -> Tuple[str, str]:
        """
        Generate JWT access and refresh tokens.
        
        Args:
            user_id: UUID of the user
            
        Returns:
            Tuple of (access_token, refresh_token)
        """
        now = datetime.utcnow()
        
        # Access token
        access_token_data = {
            "user_id": str(user_id),
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=settings.security.access_token_expire_minutes),
        }
        access_token = jwt.encode(
            access_token_data,
            settings.security.secret_key,
            algorithm=settings.security.algorithm
        )
        
        # Refresh token
        refresh_token_data = {
            "user_id": str(user_id),
            "type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=settings.security.refresh_token_expire_days),
        }
        refresh_token = jwt.encode(
            refresh_token_data,
            settings.security.secret_key,
            algorithm=settings.security.algorithm
        )
        
        return access_token, refresh_token
    
    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        """
        Verify a JWT token and return its payload.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                settings.security.secret_key,
                algorithms=[settings.security.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return None
    
    @staticmethod
    def generate_api_key() -> Tuple[str, str]:
        """
        Generate an API key and its hash.
        
        Returns:
            Tuple of (raw_api_key, hashed_api_key)
        """
        raw_key = f"sk_{secrets.token_urlsafe(32)}"
        hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
        return raw_key, hashed_key
    
    @staticmethod
    def register_user(db: Session, register_data: RegisterRequest) -> Tuple[User, str]:
        """
        Register a new user with password hashing and initial API key.
        
        Args:
            db: Database session
            register_data: Registration request data
            
        Returns:
            Tuple of (User object, raw_api_key)
            
        Raises:
            ValueError: If email already exists
        """
        # Check if user exists
        existing_user = db.query(User).filter(User.email == register_data.email).first()
        if existing_user:
            raise ValueError(f"User with email {register_data.email} already exists")
        
        # Hash password
        password_hash = AuthenticationService.hash_password(register_data.password)
        
        # Create user with UUID as string
        user = User(
            user_id=str(uuid4()),
            email=register_data.email,
            password_hash=password_hash,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            is_active=True,
            is_verified=False,
            failed_login_attempts=0,
        )
        
        db.add(user)
        db.flush()  # Flush to ensure user_id exists
        
        # Create initial API key
        raw_key, hashed_key = AuthenticationService.generate_api_key()
        api_key = APIKey(
            key_id=str(uuid4()),
            user_id=user.user_id,
            key_name="default",
            api_key_hash=hashed_key,
            is_active=True,
        )
        
        db.add(api_key)
        db.commit()
        db.refresh(user)
        
        logger.info(f"✅ User registered: {user.email}")
        return user, raw_key
    def login_user(db: Session, login_data: LoginRequest) -> Optional[User]:
        """
        Authenticate a user.
        
        Args:
            db: Database session
            login_data: Login request data
            
        Returns:
            User object if credentials valid, None otherwise
        """
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user:
            logger.warning(f"Login attempt for non-existent user: {login_data.email}")
            return None
        
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {login_data.email}")
            return None
        
        if not AuthenticationService.verify_password(login_data.password, user.password_hash):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=15)
                logger.warning(f"User locked due to failed login attempts: {user.email}")
            db.commit()
            logger.warning(f"Failed login attempt for user: {login_data.email}")
            return None
        
        # Reset failed login attempts
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = datetime.utcnow()
        user.login_count += 1
        db.commit()
        
        logger.info(f"✅ User logged in: {user.email}")
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.user_id == user_id).first()
    
    @staticmethod
    def verify_api_key(db: Session, api_key: str) -> Optional[User]:
        """
        Verify an API key and return the associated user.
        
        Args:
            db: Database session
            api_key: Raw API key string
            
        Returns:
            User object if valid, None otherwise
        """
        hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
        api_key_record = db.query(APIKey).filter(
            APIKey.api_key_hash == hashed_key,
            APIKey.is_active == True
        ).first()
        
        if not api_key_record:
            return None
        
        user = db.query(User).filter(
            User.user_id == api_key_record.user_id,
            User.is_active == True
        ).first()
        
        if user:
            # Update last used timestamp
            api_key_record.last_used_at = datetime.utcnow()
            db.commit()
        
        return user
    
    @staticmethod
    def create_api_key(db: Session, user_id: UUID, key_name: str = "default") -> Tuple[str, str]:
        """
        Create a new API key for a user.
        
        Args:
            db: Database session
            user_id: User ID
            key_name: Name for the API key
            
        Returns:
            Tuple of (raw_api_key, key_id)
        """
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        raw_key, hashed_key = AuthenticationService.generate_api_key()
        api_key = APIKey(
            key_id=str(uuid4()),
            user_id=user_id,
            key_name=key_name,
            api_key_hash=hashed_key,
            is_active=True,
        )
        
        db.add(api_key)
        db.commit()
        
        logger.info(f"✅ API key created for user {user_id}")
        return raw_key, str(api_key.key_id)
    
    @staticmethod
    def revoke_api_key(db: Session, key_id: UUID) -> bool:
        """
        Revoke an API key.
        
        Args:
            db: Database session
            key_id: API Key ID to revoke
            
        Returns:
            True if successful, False otherwise
        """
        api_key = db.query(APIKey).filter(APIKey.key_id == key_id).first()
        if not api_key:
            return False
        
        api_key.is_active = False
        db.commit()
        logger.info(f"✅ API key revoked: {key_id}")
        return True
    
    @staticmethod
    def list_api_keys(db: Session, user_id: UUID) -> list:
        """
        List all API keys for a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of API key records (without showing the raw key)
        """
        return db.query(APIKey).filter(
            APIKey.user_id == user_id,
            APIKey.deleted_at == None
        ).all()
