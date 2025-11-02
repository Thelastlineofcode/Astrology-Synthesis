"""
Unit tests for Perplexity LLM Service (Phase 5)
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock

from backend.services.perplexity_llm_service import PerplexityLLMService


@pytest.fixture
def mock_api_key():
    """Mock API key"""
    return "test-api-key-12345"


@pytest.fixture
def service(mock_api_key):
    """Create test service"""
    return PerplexityLLMService(
        api_key=mock_api_key,
        monthly_budget=5.0,
        temperature=0.7,
        top_p=0.9,
        max_tokens=512,
        timeout=30,
    )


def test_init_with_valid_key(mock_api_key):
    """Test initialization with valid API key"""
    service = PerplexityLLMService(api_key=mock_api_key)
    assert service.api_key == mock_api_key
    assert service.monthly_budget == 5.0
    assert service.MODEL == "sonar-small"


def test_init_without_key_raises():
    """Test initialization without API key raises error"""
    with pytest.raises(ValueError, match="PERPLEXITY_API_KEY is required"):
        PerplexityLLMService(api_key="")


def test_cost_calculation(service):
    """Test cost calculation accuracy"""
    # 100 input tokens, 50 output tokens
    cost = service._calculate_cost(100, 50)
    
    # Expected: (100 * 0.0001 / 1000) + (50 * 0.0003 / 1000)
    expected = (100 * 0.0001 + 50 * 0.0003) / 1000
    
    assert abs(cost - expected) < 0.0000001


def test_budget_tracking(service):
    """Test budget tracking"""
    initial_budget = service.get_budget_remaining()
    
    assert initial_budget["total"] == 5.0
    assert initial_budget["used"] == 0.0
    assert initial_budget["cost_remaining"] == 5.0
    assert initial_budget["calls"] == 0


def test_budget_remaining_calculation(service):
    """Test budget remaining calculation"""
    # Simulate some usage
    service.total_cost = 1.50
    service.call_count = 100
    
    budget = service.get_budget_remaining()
    
    assert budget["used"] == 1.50
    assert abs(budget["cost_remaining"] - 3.50) < 0.001
    assert budget["calls"] == 100
    assert abs(budget["percentage_used"] - 30.0) < 0.1


def test_is_available(service):
    """Test is_available check"""
    assert service.is_available() is True
    
    # Exhaust budget
    service.total_cost = 5.0
    assert service.is_available() is False
    
    # Partial budget left
    service.total_cost = 4.99
    assert service.is_available() is True


def test_reset_budget_tracking(service):
    """Test budget tracking reset"""
    # Simulate usage
    service.total_cost = 2.0
    service.call_count = 50
    service.total_input_tokens = 1000
    service.total_output_tokens = 500
    
    # Reset
    service.reset_budget_tracking()
    
    assert service.total_cost == 0.0
    assert service.call_count == 0
    assert service.total_input_tokens == 0
    assert service.total_output_tokens == 0


def test_build_prompt(service):
    """Test prompt building"""
    chart_data = {
        "sun": "Leo",
        "moon": "Scorpio",
        "ascendant": "Libra",
        "time_of_birth": "14:30",
        "location": "New York",
    }
    
    prompt = service._build_prompt(chart_data, "sun", "General interpretation")
    
    assert "Leo" in prompt
    assert "Scorpio" in prompt
    assert "Libra" in prompt
    assert "sun" in prompt.lower()
    assert "14:30" in prompt
    assert "New York" in prompt


@patch('requests.post')
def test_generate_interpretation_success(mock_post, service):
    """Test successful interpretation generation"""
    # Mock API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {"content": "Test interpretation"}
        }],
        "usage": {
            "prompt_tokens": 100,
            "completion_tokens": 50,
        }
    }
    mock_post.return_value = mock_response
    
    chart_data = {"sun": "Leo"}
    result = service.generate_interpretation(chart_data, "sun")
    
    assert "error" not in result
    assert result["interpretation"] == "Test interpretation"
    assert result["model"] == "sonar-small"
    assert result["cost"] > 0


@patch('requests.post')
def test_generate_interpretation_api_error(mock_post, service):
    """Test interpretation with API error"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response
    
    chart_data = {"sun": "Leo"}
    result = service.generate_interpretation(chart_data, "sun")
    
    assert result.get("error")


def test_generate_interpretation_budget_exhausted(service):
    """Test interpretation when budget exhausted"""
    service.total_cost = 5.0  # Exhaust budget
    
    chart_data = {"sun": "Leo"}
    result = service.generate_interpretation(chart_data, "sun")
    
    assert result.get("error") == "Budget exhausted"
    assert result.get("strategy") == "budget_exhausted"


@patch('requests.post')
def test_retry_on_timeout(mock_post, service):
    """Test retry logic on timeout"""
    import requests
    
    # First call raises timeout, second succeeds
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Success"}}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50},
    }
    
    mock_post.side_effect = [
        requests.Timeout(),
        mock_response,
    ]
    
    result = service._call_perplexity_api("test", 512, retries=3)
    
    # Should succeed on second attempt
    assert "error" not in result
    assert mock_post.call_count == 2


def test_pricing_constants(service):
    """Test pricing constants are correct"""
    assert service.PRICING["input"] == 0.0001
    assert service.PRICING["output"] == 0.0003
    assert service.MODEL == "sonar-small"


def test_tokens_tracking(service):
    """Test token tracking"""
    service.total_input_tokens = 1000
    service.total_output_tokens = 500
    
    budget = service.get_budget_remaining()
    
    assert budget["tokens"]["input"] == 1000
    assert budget["tokens"]["output"] == 500
    assert budget["tokens"]["total"] == 1500


def test_budget_alert(service):
    """Test budget alert threshold"""
    # Use 75% of budget
    service.total_cost = 3.75
    budget = service.get_budget_remaining()
    assert budget["alert"] is False
    
    # Use 85% of budget (>80%)
    service.total_cost = 4.25
    budget = service.get_budget_remaining()
    assert budget["alert"] is True
