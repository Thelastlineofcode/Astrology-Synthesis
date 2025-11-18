"""
Test suite for Mula: The Root API endpoints
Run: pytest test_mula_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.main import app

client = TestClient(app)


class TestConsultantAPI:
    """Test consultant chat endpoints."""
    
    def test_list_advisors(self):
        """Test GET /api/v1/consultant/advisors"""
        response = client.get("/api/v1/consultant/advisors")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 4  # Papa Legba, Erzulie, Baron, Ogoun
        assert all('id' in advisor for advisor in data)
        assert all('name' in advisor for advisor in data)
    
    def test_get_advisor(self):
        """Test GET /api/v1/consultant/advisors/{advisor_id}"""
        response = client.get("/api/v1/consultant/advisors/papa-legba")
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 'papa-legba'
        assert data['name'] == 'Papa Legba'
        assert data['symbol'] == '🗝️'
        assert 'crossroads' in data['domains']
    
    def test_get_advisor_not_found(self):
        """Test GET /api/v1/consultant/advisors/{invalid_id}"""
        response = client.get("/api/v1/consultant/advisors/invalid")
        assert response.status_code == 404
    
    def test_send_message(self):
        """Test POST /api/v1/consultant/chat"""
        payload = {
            "advisor_id": "papa-legba",
            "message": "What guidance do you have for me?",
            "chat_history": []
        }
        response = client.post("/api/v1/consultant/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['advisor_id'] == 'papa-legba'
        assert data['advisor_name'] == 'Papa Legba'
        assert len(data['response']) > 0
        assert 'suggestions' in data
        assert isinstance(data['suggestions'], list)
    
    def test_send_message_invalid_advisor(self):
        """Test POST /api/v1/consultant/chat with invalid advisor"""
        payload = {
            "advisor_id": "invalid-advisor",
            "message": "Test message"
        }
        response = client.post("/api/v1/consultant/chat", json=payload)
        assert response.status_code == 400
    
    def test_send_empty_message(self):
        """Test POST /api/v1/consultant/chat with empty message"""
        payload = {
            "advisor_id": "papa-legba",
            "message": ""
        }
        response = client.post("/api/v1/consultant/chat", json=payload)
        assert response.status_code == 422  # Validation error


class TestFortuneAPI:
    """Test fortune reading endpoints."""
    
    def test_list_cards(self):
        """Test GET /api/v1/fortune/cards"""
        response = client.get("/api/v1/fortune/cards")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 5  # At least 5 oracle cards
        assert all('id' in card for card in data)
        assert all('name' in card for card in data)
        assert all('symbol' in card for card in data)
    
    def test_get_card(self):
        """Test GET /api/v1/fortune/cards/{card_id}"""
        response = client.get("/api/v1/fortune/cards/papa-legba")
        assert response.status_code == 200
        data = response.json()
        assert data['id'] == 'papa-legba'
        assert data['name'] == 'Papa Legba'
        assert data['subtitle'] == 'The Crossroads'
        assert 'meaning' in data
        assert 'advice' in data
    
    def test_get_card_not_found(self):
        """Test GET /api/v1/fortune/cards/{invalid_id}"""
        response = client.get("/api/v1/fortune/cards/invalid")
        assert response.status_code == 404
    
    def test_draw_daily_fortune(self):
        """Test POST /api/v1/fortune/draw - daily reading"""
        payload = {"reading_type": "daily"}
        response = client.post("/api/v1/fortune/draw", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['reading_type'] == 'daily'
        assert 'card' in data
        assert 'interpretation' in data
        assert 'Today' in data['interpretation']
    
    def test_draw_weekly_fortune(self):
        """Test POST /api/v1/fortune/draw - weekly reading"""
        payload = {"reading_type": "weekly"}
        response = client.post("/api/v1/fortune/draw", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['reading_type'] == 'weekly'
        assert 'week' in data['interpretation'].lower()
    
    def test_draw_custom_fortune(self):
        """Test POST /api/v1/fortune/draw - custom reading with question"""
        payload = {
            "reading_type": "custom",
            "question": "Will I find love this year?"
        }
        response = client.post("/api/v1/fortune/draw", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data['reading_type'] == 'custom'
        assert 'question' in data['interpretation'].lower()
    
    def test_draw_custom_without_question(self):
        """Test POST /api/v1/fortune/draw - custom reading missing question"""
        payload = {"reading_type": "custom"}
        response = client.post("/api/v1/fortune/draw", json=payload)
        assert response.status_code == 400
    
    def test_draw_invalid_type(self):
        """Test POST /api/v1/fortune/draw - invalid reading type"""
        payload = {"reading_type": "invalid"}
        response = client.post("/api/v1/fortune/draw", json=payload)
        assert response.status_code == 400


class TestHealthAPI:
    """Test system health endpoints."""
    
    def test_root(self):
        """Test GET /"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert 'message' in data
        assert 'version' in data
        assert 'status' in data
    
    def test_health(self):
        """Test GET /api/v1/health"""
        response = client.get("/api/v1/health")
        assert response.status_code in [200, 503]  # May be degraded
        data = response.json()
        assert 'status' in data


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
