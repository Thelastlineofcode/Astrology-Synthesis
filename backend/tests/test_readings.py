import pytest

def test_ask_advisor(client):
    # Setup
    client.post(
        "/api/auth/register",
        json={"email": "user@test.com", "username": "testuser", "password": "password123"}
    )
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    
    # Ask advisor
    response = client.post(
        "/api/readings/ask",
        headers={"Authorization": f"Bearer {token}"},
        json={"advisor": "legba", "question": "What does my future hold?"}
    )
    assert response.status_code == 200
    assert response.json()["advisor"] == "legba"
    assert response.json()["question"] == "What does my future hold?"

def test_get_reading(client):
    # Setup
    client.post(
        "/api/auth/register",
        json={"email": "user@test.com", "username": "testuser", "password": "password123"}
    )
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    
    # Create reading
    create_resp = client.post(
        "/api/readings/ask",
        headers={"Authorization": f"Bearer {token}"},
        json={"advisor": "oshun", "question": "Guide my path?"}
    )
    reading_id = create_resp.json()["id"]
    
    # Retrieve reading
    response = client.get(
        f"/api/readings/{reading_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == reading_id

def test_invalid_advisor(client):
    # Setup
    client.post(
        "/api/auth/register",
        json={"email": "user@test.com", "username": "testuser", "password": "password123"}
    )
    login_resp = client.post(
        "/api/auth/login",
        json={"email": "user@test.com", "password": "password123"}
    )
    token = login_resp.json()["access_token"]
    
    # Ask invalid advisor
    response = client.post(
        "/api/readings/ask",
        headers={"Authorization": f"Bearer {token}"},
        json={"advisor": "invalid", "question": "What?"}
    )
    assert response.status_code == 422
