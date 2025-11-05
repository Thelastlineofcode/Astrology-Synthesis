"""
Basic tests for authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns correct response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Mula Dasha Timer API"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_signup_missing_fields():
    """Test signup with missing fields returns 422."""
    response = client.post("/api/v1/auth/signup", json={})
    assert response.status_code == 422


def test_signup_invalid_email():
    """Test signup with invalid email."""
    response = client.post("/api/v1/auth/signup", json={
        "email": "invalid-email",
        "password": "password123"
    })
    assert response.status_code == 422


def test_signup_short_password():
    """Test signup with too short password."""
    response = client.post("/api/v1/auth/signup", json={
        "email": "test@example.com",
        "password": "short"
    })
    assert response.status_code == 422


# Note: Full integration tests would require database setup
# These are basic smoke tests to verify endpoints are wired correctly
