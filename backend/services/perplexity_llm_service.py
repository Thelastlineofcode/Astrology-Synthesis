"""
Perplexity LLM Service for Phase 5
Provides cost-effective LLM-powered interpretations using Perplexity sonar-small
"""

import os
import json
import time
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class PerplexityLLMService:
    """
    Service for generating interpretations using Perplexity API (sonar-small)
    
    Pricing:
    - Input: $0.0001 per 1K tokens (~$0.00000001 per token)
    - Output: $0.0003 per 1K tokens (~$0.0000003 per token)
    - Per call estimate: ~$0.00001 (100 input + 50 output tokens)
    - Monthly capacity: 47,000+ interpretations on $5 budget
    """
    
    MODEL = "sonar-small"
    BASE_URL = "https://api.perplexity.ai"
    
    # Pricing per 1M tokens
    PRICING = {
        "input": 0.0001,      # $0.0001 per 1K tokens
        "output": 0.0003,     # $0.0003 per 1K tokens
    }
    
    def __init__(
        self,
        api_key: str,
        monthly_budget: float = 5.0,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 1024,
        timeout: int = 30,
    ):
        """
        Initialize Perplexity LLM Service
        
        Args:
            api_key: Perplexity API key
            monthly_budget: Monthly budget in dollars
            temperature: Model temperature (0-1)
            top_p: Top-p sampling parameter
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
        """
        if not api_key:
            raise ValueError("PERPLEXITY_API_KEY is required")
        
        self.api_key = api_key
        self.monthly_budget = monthly_budget
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.timeout = timeout
        
        # Tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0
        self.start_time = datetime.now()
        
        logger.info(
            f"PerplexityLLMService initialized with "
            f"model={self.MODEL}, budget=${monthly_budget}/month"
        )
    
    def generate_interpretation(
        self,
        chart_data: Dict[str, Any],
        interpretation_type: str,
        context: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate interpretation using Perplexity API
        
        Args:
            chart_data: Chart data dict with sun, moon, ascendant, etc.
            interpretation_type: Type of interpretation (sun, moon, etc.)
            context: Additional context for interpretation
            max_tokens: Override max tokens for this call
            
        Returns:
            Dict with interpretation, cost, tokens, and metadata
        """
        try:
            # Build prompt
            prompt = self._build_prompt(chart_data, interpretation_type, context)
            
            # Check budget before API call
            budget_status = self.get_budget_remaining()
            if budget_status["cost_remaining"] <= 0:
                logger.warning("Monthly budget exhausted")
                return {
                    "error": "Budget exhausted",
                    "strategy": "budget_exhausted",
                    "cost": 0.0,
                }
            
            # Make API request with retry logic
            response = self._call_perplexity_api(
                prompt,
                max_tokens or self.max_tokens,
            )
            
            if response.get("error"):
                logger.error(f"API error: {response['error']}")
                return response
            
            # Extract data
            interpretation = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            input_tokens = response.get("usage", {}).get("prompt_tokens", 0)
            output_tokens = response.get("usage", {}).get("completion_tokens", 0)
            
            # Calculate cost
            cost = self._calculate_cost(input_tokens, output_tokens)
            
            # Update tracking
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            self.total_cost += cost
            self.call_count += 1
            
            logger.info(
                f"Generated {interpretation_type} interpretation: "
                f"tokens={input_tokens + output_tokens}, cost=${cost:.6f}"
            )
            
            return {
                "interpretation": interpretation,
                "type": interpretation_type,
                "model": self.MODEL,
                "cost": cost,
                "tokens": {
                    "input": input_tokens,
                    "output": output_tokens,
                    "total": input_tokens + output_tokens,
                },
                "budget": budget_status,
                "quality": 0.85,  # LLM strategy quality score
                "strategy": "llm",
            }
            
        except Exception as e:
            logger.error(f"Error generating interpretation: {str(e)}")
            return {
                "error": str(e),
                "type": interpretation_type,
                "cost": 0.0,
                "strategy": "llm_error",
            }
    
    def _build_prompt(
        self,
        chart_data: Dict[str, Any],
        interpretation_type: str,
        context: Optional[str] = None,
    ) -> str:
        """Build interpretation prompt"""
        base_prompt = f"""You are an expert astrologer providing {interpretation_type} sign interpretations.

Chart Data:
- Sun: {chart_data.get('sun', 'Unknown')}
- Moon: {chart_data.get('moon', 'Unknown')}
- Ascendant: {chart_data.get('ascendant', 'Unknown')}
- Birth Time: {chart_data.get('time_of_birth', 'Unknown')}
- Location: {chart_data.get('location', 'Unknown')}

Provide a detailed, personalized {interpretation_type} sign interpretation that:
1. Explains key characteristics
2. Discusses planetary influences
3. Provides guidance for daily life
4. Is warm, insightful, and non-judgmental

Context: {context or 'General interpretation requested'}

Keep the response concise but meaningful (200-400 words)."""
        
        return base_prompt
    
    def _call_perplexity_api(
        self,
        prompt: str,
        max_tokens: int,
        retries: int = 3,
    ) -> Dict[str, Any]:
        """
        Call Perplexity API with retry logic
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response
            retries: Number of retries on timeout
            
        Returns:
            API response dict
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": max_tokens,
        }
        
        for attempt in range(retries):
            try:
                response = requests.post(
                    f"{self.BASE_URL}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.timeout,
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limited
                    wait_time = (2 ** attempt) * 5  # Exponential backoff
                    logger.warning(f"Rate limited, retrying in {wait_time}s")
                    time.sleep(wait_time)
                else:
                    return {
                        "error": f"API error: {response.status_code}",
                        "status": response.status_code,
                    }
                    
            except requests.Timeout:
                if attempt < retries - 1:
                    logger.warning(f"Timeout on attempt {attempt + 1}, retrying...")
                    time.sleep(2 ** attempt)
                else:
                    return {"error": "Request timeout after retries"}
            except Exception as e:
                return {"error": f"Request error: {str(e)}"}
        
        return {"error": "All retries exhausted"}
    
    def _calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """
        Calculate cost for a single call
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost in dollars
        """
        # Cost per token: divide per-1K pricing by 1000
        input_cost = (input_tokens * self.PRICING["input"]) / 1000
        output_cost = (output_tokens * self.PRICING["output"]) / 1000
        return input_cost + output_cost
    
    def get_budget_remaining(self) -> Dict[str, Any]:
        """
        Get remaining budget information
        
        Returns:
            Dict with budget, usage, and remaining info
        """
        elapsed_time = datetime.now() - self.start_time
        days_elapsed = elapsed_time.days + (elapsed_time.seconds / 86400)
        
        # Estimate remaining budget
        if days_elapsed > 0:
            daily_burn_rate = self.total_cost / days_elapsed
            estimated_monthly_cost = daily_burn_rate * 30
        else:
            estimated_monthly_cost = 0.0
        
        return {
            "total": self.monthly_budget,
            "used": self.total_cost,
            "cost_remaining": max(0, self.monthly_budget - self.total_cost),
            "percentage_used": (self.total_cost / self.monthly_budget * 100) if self.monthly_budget > 0 else 0,
            "estimated_monthly": estimated_monthly_cost,
            "calls": self.call_count,
            "tokens": {
                "input": self.total_input_tokens,
                "output": self.total_output_tokens,
                "total": self.total_input_tokens + self.total_output_tokens,
            },
            "alert": self.total_cost / self.monthly_budget > 0.80 if self.monthly_budget > 0 else False,
        }
    
    def is_available(self) -> bool:
        """Check if service is available (budget remaining)"""
        budget = self.get_budget_remaining()
        # Use epsilon for floating point comparison (need at least $0.01 remaining)
        return budget["cost_remaining"] > 0.009  # Slightly less than 0.01 to handle float precision
    
    def reset_budget_tracking(self) -> None:
        """Reset budget tracking for new month"""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0
        self.start_time = datetime.now()
        logger.info("Budget tracking reset for new period")


# Initialization helper
def create_perplexity_service() -> PerplexityLLMService:
    """Factory function to create service from environment variables"""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable not set")
    
    return PerplexityLLMService(
        api_key=api_key,
        monthly_budget=float(os.getenv("MONTHLY_BUDGET", "5.0")),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        top_p=float(os.getenv("TOP_P", "0.9")),
        max_tokens=int(os.getenv("MAX_TOKENS", "1024")),
        timeout=int(os.getenv("TIMEOUT", "30")),
    )
