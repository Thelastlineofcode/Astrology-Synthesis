import pytest
import pytest_asyncio
from httpx import AsyncClient
from backend.main import app
from backend.config.database import Base
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
Base.metadata.create_all(bind=engine)

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "full_name": "Test User", "password": "password123"}
    )
    assert response.status_code in [200, 201]
    assert "test@example.com" in response.text

@pytest.mark.asyncio
async def test_login(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "test2@example.com", "full_name": "Test User 2", "password": "password123"}
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "test2@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
