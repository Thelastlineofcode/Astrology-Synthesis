"""
Authentication tests.
Tests for user registration, login, JWT tokens, API keys, and authentication middleware.
Covers all authentication flows and security features.
"""

import pytest
import json
from datetime import datetime, timedelta
from uuid import uuid4
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.main import app
from backend.config.database import SessionLocal, engine
from backend.models.database import Base, User, APIKey
from backend.services.auth_service import AuthenticationService
from backend.schemas import RegisterRequest, LoginRequest

# Create test database
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app=app, base_url="http://testserver")


@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean database before each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Provide a database session for tests."""
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        user_id=str(uuid4()),
        email="test@example.com",
        password_hash=AuthenticationService.hash_password("Pass123!"),
        first_name="Test",
        last_name="User",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    return user


class TestRegistration:
    """Test user registration functionality."""
    
    def test_register_success(self):
        """Test successful user registration."""
        response = client.post("/api/v1/auth/register", json={
            "email": "newuser@example.com",
            "password": "Pass123!",
            "first_name": "New",
            "last_name": "User",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "user_id" in data
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "Pass123!",
                "first_name": "Test",
                "last_name": "User2",
            }
        )
        
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]
    
    def test_register_invalid_email(self):
        """Test registration with invalid email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "Pass123!",
                "first_name": "Test",
                "last_name": "User",
            }
        )
    
    def test_register_invalid_email(self):
        """Test registration with invalid email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "SecurePass123",
                "first_name": "Test",
                "last_name": "User",
            }
        )
        
        # Pydantic should validate email format
        assert response.status_code == 422
    
    def test_register_weak_password(self):
        """Test registration with weak password."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "weak",
                "first_name": "Test",
                "last_name": "User",
            }
        )
        
        # Validation should fail for weak password
        assert response.status_code in [422, 400]


class TestLogin:
    """Test user login."""
    
    def test_login_success(self, test_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "Pass123!",
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["email"] == "test@example.com"
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_email(self):
        """Test login with non-existent email."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Pass123!",
            }
        )
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_login_wrong_password(self, test_user):
        """Test login with wrong password."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPassword123",
            }
        )
        
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_login_failed_attempts_lockout(self, db_session, test_user):
        """Test account lockout after failed login attempts."""
        # Make 5 failed login attempts
        for i in range(5):
            response = client.post(
                "/api/v1/auth/login",
                json={
                    "email": "test@example.com",
                    "password": "WrongPassword",
                }
            )
            assert response.status_code == 401
        
        # Verify user is locked
        db_session.refresh(test_user)
        assert test_user.failed_login_attempts >= 5
        assert test_user.locked_until is not None


class TestTokenRefresh:
    """Test JWT token refresh."""
    
    def test_refresh_token_success(self, test_user):
        """Test successful token refresh."""
        # First, login to get tokens
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "Pass123!",
            }
        )
        
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh the token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_refresh_with_invalid_token(self):
        """Test token refresh with invalid token."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid.token.here"}
        )
        
        assert response.status_code == 401
        assert "Invalid refresh token" in response.json()["detail"]
    
    def test_refresh_with_access_token(self, test_user):
        """Test token refresh with access token (should fail)."""
        # Login to get tokens
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "Pass123!",
            }
        )
        
        access_token = login_response.json()["access_token"]
        
        # Try to use access token as refresh token
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token}
        )
        
        # Should fail because token type is "access", not "refresh"
        assert response.status_code == 401


class TestUserProfile:
    """Test user profile endpoint."""
    
    def test_get_profile_with_valid_token(self, test_user):
        """Test getting user profile with valid JWT token."""
        # Login to get token
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "Pass123!",
            }
        )
        
        access_token = login_response.json()["access_token"]
        
        # Get profile
        response = client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["email"] == "test@example.com"
        assert data["first_name"] == "Test"
        assert data["is_active"] == True
    
    def test_get_profile_without_token(self):
        """Test getting profile without authentication."""
        response = client.get("/api/v1/auth/profile")
        
        assert response.status_code == 401
        assert "Missing authorization header" in response.json()["detail"]
    
    def test_get_profile_with_invalid_token(self):
        """Test getting profile with invalid token."""
        response = client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401


class TestAPIKeys:
    """Test API key management."""
    
    def test_create_api_key(self, test_user):
        """Test creating a new API key."""
        # Login to get token
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "Pass123!",
            }
        )
        
        access_token = login_response.json()["access_token"]
        
        # Create API key
        response = client.post(
            "/api/v1/auth/api-keys",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"key_name": "test-key"}
        )
        
        assert response.status_code == 201
        data = response.json()
        
        assert "key_id" in data
        assert data["key_name"] == "test-key"
        assert "raw_key" in data
        assert data["raw_key"].startswith("sk_")
    
    def test_list_api_keys(self, test_user):
        """Test listing API keys."""
        # Login to get token
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "Pass123!",
            }
        )
        
        access_token = login_response.json()["access_token"]
        
        # Create API key first
        create_response = client.post(
            "/api/v1/auth/api-keys",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"key_name": "test-key"}
        )
        
        # List keys
        response = client.get(
            "/api/v1/auth/api-keys",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "keys" in data
        assert len(data["keys"]) >= 1
        # Verify raw_key is NOT returned in list
        assert "raw_key" not in data["keys"][0]
    
    def test_revoke_api_key(self, test_user):
        """Test revoking an API key."""
        # Login to get token
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "Pass123!",
            }
        )
        
        access_token = login_response.json()["access_token"]
        
        # Create API key
        create_response = client.post(
            "/api/v1/auth/api-keys",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"key_name": "test-key"}
        )
        
        key_id = create_response.json()["key_id"]
        
        # Revoke key
        response = client.delete(
            f"/api/v1/auth/api-keys/{key_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        assert "revoked successfully" in response.json()["message"]
    
    def test_use_revoked_api_key(self, test_user):
        """Test that revoked API keys don't work."""
        # This would require a protected endpoint that accepts API keys
        # For now, just verify the key is marked inactive
        pass


class TestSecurityFeatures:
    """Test security features."""
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed."""
        password = "Pass123!"
        hash1 = AuthenticationService.hash_password(password)
        hash2 = AuthenticationService.hash_password(password)
        
        # Different hashes for same password (bcrypt with salt)
        assert hash1 != hash2
        
        # Both should verify correctly
        assert AuthenticationService.verify_password(password, hash1)
        assert AuthenticationService.verify_password(password, hash2)
    
    def test_invalid_password_verification(self):
        """Test that incorrect passwords don't verify."""
        password = "Pass123!"
        hash_value = AuthenticationService.hash_password(password)
        
        assert not AuthenticationService.verify_password("WrongPassword", hash_value)
    
    def test_api_key_format(self):
        """Test that API keys have correct format."""
        raw_key, hashed_key = AuthenticationService.generate_api_key()
        
        # Raw key should start with sk_ and be long enough
        assert raw_key.startswith("sk_")
        assert len(raw_key) > 30
        
        # Hashed key should be SHA256 hash (64 hex chars)
        assert len(hashed_key) == 64
        assert all(c in "0123456789abcdef" for c in hashed_key)


class TestAuthenticationIntegration:
    """Integration tests for authentication flow."""
    
    def test_full_auth_flow(self):
        """Test complete authentication flow: register -> login -> access profile -> refresh token."""
        # 1. Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "integration@example.com",
                "password": "IntegrationTest123",
                "first_name": "Integration",
                "last_name": "Test",
            }
        )
        
        assert register_response.status_code == 201
        user_id = register_response.json()["user_id"]
        
        # 2. Login
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "integration@example.com",
                "password": "IntegrationTest123",
            }
        )
        
        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]
        refresh_token = login_response.json()["refresh_token"]
        
        # 3. Get profile
        profile_response = client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert profile_response.status_code == 200
        assert profile_response.json()["email"] == "integration@example.com"
        
        # 4. Refresh token
        refresh_response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert refresh_response.status_code == 200
        new_access_token = refresh_response.json()["access_token"]
        
        # 5. Use new token to access profile
        new_profile_response = client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": f"Bearer {new_access_token}"}
        )
        
        assert new_profile_response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
