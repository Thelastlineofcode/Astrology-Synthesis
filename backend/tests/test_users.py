import pytest
from app.models import User

def test_get_profile(client):
    # Register and login first
    client.post(
        "/api/auth/register",
        json={"email": "user@test.com", "username": "testuser", "password": "password123"}
    )
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    
    response = client.get(
        "/api/users/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user@test.com"

def test_get_readings_history(client):
    # Register and login
    client.post(
        "/api/auth/register",
        json={"email": "user@test.com", "username": "testuser", "password": "password123"}
    )
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    
    response = client.get(
        "/api/users/readings-history",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["total"] == 0
