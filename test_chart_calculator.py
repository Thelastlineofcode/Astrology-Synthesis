"""
Comprehensive test suite for the FastAPI Chart Calculator endpoints.
Tests birth chart generation, retrieval, and listing with real astronomical data.
"""

import pytest
import json
from datetime import datetime, timedelta
from uuid import UUID
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_client():
    """Create test client with FastAPI app."""
    from backend.main import app
    from backend.config.database import get_db
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create tables
    from backend.models.database import Base
    Base.metadata.create_all(bind=engine)
    
    return TestClient(app)


@pytest.fixture(scope="function")
def auth_headers(test_client):
    """Register user and get JWT token for authenticated requests."""
    # Register
    register_response = test_client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123",
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert register_response.status_code == 201
    
    # Login
    login_response = test_client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPassword123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}


class TestBirthChartGeneration:
    """Test birth chart generation endpoint."""
    
    def test_create_birth_chart_success(self, test_client, auth_headers):
        """Test successful birth chart creation."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "location_name": "New York"
            },
            "name": "My Birth Chart",
            "notes": "Test chart"
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        
        # Verify response structure
        assert "chart_id" in data
        assert "user_id" in data
        assert data["birth_location_name"] == "New York"
        assert data["name"] == "My Birth Chart"
        
        # Verify chart data exists
        assert "chart_data" in data
        chart_data = data["chart_data"]
        assert "planet_positions" in chart_data
        assert "house_cusps" in chart_data
        assert "ascendant" in chart_data
        
        print(f"✅ Birth chart created: {data['chart_id']}")
        return data["chart_id"]
    
    def test_create_birth_chart_invalid_date(self, test_client, auth_headers):
        """Test birth chart creation with invalid date format."""
        birth_data = {
            "birth_data": {
                "date": "invalid-date",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        print("✅ Invalid date format rejected")
    
    def test_create_birth_chart_invalid_time(self, test_client, auth_headers):
        """Test birth chart creation with invalid time format."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "invalid-time",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        assert response.status_code == 400
        print("✅ Invalid time format rejected")
    
    def test_create_birth_chart_invalid_latitude(self, test_client, auth_headers):
        """Test birth chart with invalid latitude (outside -90 to 90)."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 95.0,  # Invalid: > 90
                "longitude": -74.0060,
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
        print("✅ Invalid latitude rejected")
    
    def test_create_birth_chart_invalid_longitude(self, test_client, auth_headers):
        """Test birth chart with invalid longitude (outside -180 to 180)."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": 185.0,  # Invalid: > 180
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
        print("✅ Invalid longitude rejected")
    
    def test_create_birth_chart_missing_required_fields(self, test_client, auth_headers):
        """Test birth chart creation missing required fields."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                # Missing: time, timezone, latitude, longitude
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
        print("✅ Missing required fields rejected")
    
    def test_create_birth_chart_unauthorized(self, test_client):
        """Test that birth chart creation requires authentication."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data
        )
        
        assert response.status_code == 401  # Unauthorized
        print("✅ Unauthorized request rejected")


class TestBirthChartRetrieval:
    """Test birth chart retrieval endpoint."""
    
    def test_get_birth_chart_success(self, test_client, auth_headers):
        """Test successful birth chart retrieval."""
        # First, create a chart
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            },
            "name": "Test Chart"
        }
        
        create_response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        assert create_response.status_code == 201
        chart_id = create_response.json()["chart_id"]
        
        # Now retrieve it
        response = test_client.get(
            f"/api/v1/chart/{chart_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["chart_id"] == chart_id
        assert data["name"] == "Test Chart"
        print(f"✅ Chart retrieved: {chart_id}")
    
    def test_get_birth_chart_not_found(self, test_client, auth_headers):
        """Test retrieving non-existent chart."""
        fake_chart_id = "550e8400-e29b-41d4-a716-446655440000"
        
        response = test_client.get(
            f"/api/v1/chart/{fake_chart_id}",
            headers=auth_headers
        )
        
        assert response.status_code == 404
        print("✅ Non-existent chart returns 404")
    
    def test_get_birth_chart_unauthorized(self, test_client):
        """Test that chart retrieval requires authentication."""
        response = test_client.get("/api/v1/chart/550e8400-e29b-41d4-a716-446655440000")
        
        assert response.status_code == 401
        print("✅ Unauthorized chart retrieval rejected")
    
    def test_get_birth_chart_wrong_user(self, test_client, auth_headers):
        """Test that users can only see their own charts."""
        # Create chart as first user
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }
        
        create_response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        chart_id = create_response.json()["chart_id"]
        
        # Create second user
        test_client.post(
            "/api/v1/auth/register",
            json={
                "email": "user2@example.com",
                "password": "Password123",
                "first_name": "User",
                "last_name": "Two"
            }
        )
        
        login_response = test_client.post(
            "/api/v1/auth/login",
            json={
                "email": "user2@example.com",
                "password": "Password123"
            }
        )
        other_token = login_response.json()["access_token"]
        other_headers = {"Authorization": f"Bearer {other_token}"}
        
        # Try to access first user's chart with second user
        response = test_client.get(
            f"/api/v1/chart/{chart_id}",
            headers=other_headers
        )
        
        assert response.status_code == 404  # Chart not found for this user
        print("✅ User cannot access other user's charts")


class TestBirthChartListing:
    """Test birth chart listing endpoint."""
    
    def test_list_birth_charts_empty(self, test_client, auth_headers):
        """Test listing charts when user has none."""
        response = test_client.get(
            "/api/v1/chart",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
        print("✅ Empty chart list returns empty array")
    
    def test_list_birth_charts_multiple(self, test_client, auth_headers):
        """Test listing multiple charts."""
        # Create 3 charts
        chart_ids = []
        for i in range(3):
            birth_data = {
                "birth_data": {
                    "date": "1995-06-15",
                    "time": f"{14+i}:30:00",
                    "timezone": "America/New_York",
                    "latitude": 40.7128 + (i * 0.1),
                    "longitude": -74.0060,
                },
                "name": f"Chart {i+1}"
            }
            
            response = test_client.post(
                "/api/v1/chart",
                json=birth_data,
                headers=auth_headers
            )
            assert response.status_code == 201
            chart_ids.append(response.json()["chart_id"])
        
        # List all charts
        response = test_client.get(
            "/api/v1/chart",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Verify names
        names = [chart["name"] for chart in data]
        assert "Chart 1" in names
        assert "Chart 2" in names
        assert "Chart 3" in names
        
        print(f"✅ Listed {len(data)} charts")
    
    def test_list_birth_charts_pagination(self, test_client, auth_headers):
        """Test pagination with skip and limit parameters."""
        # Create 15 charts
        for i in range(15):
            birth_data = {
                "birth_data": {
                    "date": "1995-06-15",
                    "time": "14:30:00",
                    "timezone": "America/New_York",
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                },
                "name": f"Chart {i+1}"
            }
            
            test_client.post(
                "/api/v1/chart",
                json=birth_data,
                headers=auth_headers
            )
        
        # Test skip and limit
        response = test_client.get(
            "/api/v1/chart?skip=5&limit=10",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10
        print("✅ Pagination works (skip=5, limit=10)")
        
        # Test default limit (10)
        response = test_client.get(
            "/api/v1/chart",
            headers=auth_headers
        )
        assert len(response.json()) == 10
        print("✅ Default limit is 10")
        
        # Test max limit enforcement
        response = test_client.get(
            "/api/v1/chart?limit=200",
            headers=auth_headers
        )
        data = response.json()
        assert len(data) <= 100  # Should cap at 100
        print("✅ Max limit enforced (capped at 100)")


class TestChartDataAccuracy:
    """Test accuracy of generated chart data."""
    
    def test_chart_has_all_planets(self, test_client, auth_headers):
        """Test that chart includes all planets."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        chart = response.json()
        planets = chart["chart_data"]["planet_positions"]
        
        expected_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars", 
                          "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
                          "Rahu", "Ketu"]
        
        planet_names = [p["planet"] for p in planets]
        
        for planet in expected_planets:
            assert planet in planet_names, f"Missing planet: {planet}"
        
        print(f"✅ Chart includes all {len(expected_planets)} planets")
    
    def test_chart_has_all_houses(self, test_client, auth_headers):
        """Test that chart includes all 12 houses."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        chart = response.json()
        houses = chart["chart_data"]["house_cusps"]
        
        assert len(houses) == 12, f"Expected 12 houses, got {len(houses)}"
        
        for i, house in enumerate(houses, 1):
            assert house["house"] == i
            assert "degree" in house
            assert "zodiac_sign" in house
        
        print("✅ Chart includes all 12 house cusps")
    
    def test_chart_has_aspects(self, test_client, auth_headers):
        """Test that chart includes aspect calculations."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        chart = response.json()
        aspects = chart["chart_data"]["aspects"]
        
        # Should have some aspects (at least major ones)
        assert len(aspects) > 0, "Chart has no aspects"
        
        # Each aspect should have required fields
        for aspect in aspects:
            assert "planet1" in aspect
            assert "planet2" in aspect
            assert "aspect_type" in aspect
            assert "orb" in aspect
        
        print(f"✅ Chart includes {len(aspects)} aspects")
    
    def test_planet_coordinates_valid(self, test_client, auth_headers):
        """Test that planet coordinates are valid."""
        birth_data = {
            "birth_data": {
                "date": "1995-06-15",
                "time": "14:30:00",
                "timezone": "America/New_York",
                "latitude": 40.7128,
                "longitude": -74.0060,
            }
        }
        
        response = test_client.post(
            "/api/v1/chart",
            json=birth_data,
            headers=auth_headers
        )
        
        chart = response.json()
        planets = chart["chart_data"]["planet_positions"]
        
        for planet in planets:
            # Degree should be 0-360
            assert 0 <= planet["degree"] <= 360, f"Invalid degree: {planet['degree']}"
            
            # Minutes should be 0-60
            assert 0 <= planet["minutes"] <= 60, f"Invalid minutes: {planet['minutes']}"
            
            # Seconds should be 0-60
            assert 0 <= planet["seconds"] <= 60, f"Invalid seconds: {planet['seconds']}"
            
            # House should be 1-12
            assert 1 <= planet["house"] <= 12, f"Invalid house: {planet['house']}"
            
            # Zodiac sign should be valid
            valid_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            assert planet["zodiac_sign"] in valid_signs, f"Invalid zodiac sign: {planet['zodiac_sign']}"
        
        print("✅ All planet coordinates are valid")


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    # Run with: pytest test_chart_calculator.py -v
    print("\n" + "="*80)
    print("CHART CALCULATOR TEST SUITE")
    print("="*80 + "\n")
    
    pytest.main([__file__, "-v", "-s"])
