"""
Cached Perplexity Service with Redis Integration
Extends PerplexityLLMService with cost-saving cache layer
"""

import os
import json
import hashlib
import redis
from typing import Dict, Any, Optional
from datetime import timedelta
import logging

from backend.services.perplexity_llm_service import PerplexityLLMService

logger = logging.getLogger(__name__)


class CachedPerplexityService(PerplexityLLMService):
    """
    Perplexity LLM Service with Redis caching
    
    Caching strategy:
    - 30-day TTL for interpretations
    - Target 60-70% cache hit rate
    - Saves API costs on repeated queries
    """
    
    CACHE_TTL = 2592000  # 30 days in seconds
    CACHE_PREFIX = "interp:"
    
    def __init__(
        self,
        api_key: str,
        redis_url: str = "redis://localhost:6379",
        monthly_budget: float = 5.0,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 1024,
        timeout: int = 30,
        cache_ttl: int = CACHE_TTL,
    ):
        """
        Initialize Cached Perplexity Service
        
        Args:
            api_key: Perplexity API key
            redis_url: Redis connection URL
            monthly_budget: Monthly budget in dollars
            temperature: Model temperature (0-1)
            top_p: Top-p sampling parameter
            max_tokens: Maximum tokens in response
            timeout: Request timeout in seconds
            cache_ttl: Cache TTL in seconds (default 30 days)
        """
        super().__init__(
            api_key=api_key,
            monthly_budget=monthly_budget,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        
        # Redis setup
        try:
            self.redis_client = redis.from_url(redis_url)
            self.redis_client.ping()
            self.cache_available = True
            logger.info("Redis cache initialized")
        except Exception as e:
            self.cache_available = False
            self.redis_client = None
            logger.warning(f"Redis cache unavailable: {str(e)}")
        
        self.cache_ttl = cache_ttl
        
        # Cache statistics
        self.cache_hits = 0
        self.cache_misses = 0
    
    def generate_interpretation(
        self,
        chart_data: Dict[str, Any],
        interpretation_type: str,
        context: Optional[str] = None,
        max_tokens: Optional[int] = None,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """
        Generate interpretation with caching
        
        Args:
            chart_data: Chart data dict
            interpretation_type: Type of interpretation
            context: Additional context
            max_tokens: Override max tokens
            use_cache: Whether to use cache
            
        Returns:
            Dict with interpretation and metadata
        """
        # Check cache if enabled
        if use_cache and self.cache_available:
            cache_key = self._generate_cache_key(chart_data, interpretation_type, context)
            cached_result = self._get_from_cache(cache_key)
            
            if cached_result:
                self.cache_hits += 1
                cached_result["from_cache"] = True
                cached_result["cache_hits"] = self.cache_hits
                logger.info(f"Cache hit for {interpretation_type}")
                return cached_result
            
            self.cache_misses += 1
        
        # Generate fresh interpretation
        result = super().generate_interpretation(
            chart_data,
            interpretation_type,
            context,
            max_tokens,
        )
        
        # Cache the result if successful
        if use_cache and self.cache_available and not result.get("error"):
            cache_key = self._generate_cache_key(chart_data, interpretation_type, context)
            self._set_in_cache(cache_key, result)
        
        result["from_cache"] = False
        result["cache_stats"] = self.get_cache_stats()
        
        return result
    
    def _generate_cache_key(
        self,
        chart_data: Dict[str, Any],
        interpretation_type: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Generate cache key from chart data and parameters
        
        Args:
            chart_data: Chart data dict
            interpretation_type: Type of interpretation
            context: Additional context
            
        Returns:
            Cache key string
        """
        # Create deterministic key from inputs
        key_data = {
            "sun": chart_data.get("sun", ""),
            "moon": chart_data.get("moon", ""),
            "ascendant": chart_data.get("ascendant", ""),
            "type": interpretation_type,
            "context": context or "",
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        key_hash = hashlib.sha256(key_string.encode()).hexdigest()
        
        return f"{self.CACHE_PREFIX}{key_hash}"
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve value from Redis cache
        
        Args:
            cache_key: Cache key
            
        Returns:
            Cached value or None
        """
        try:
            cached_value = self.redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
        except Exception as e:
            logger.warning(f"Cache retrieval error: {str(e)}")
        
        return None
    
    def _set_in_cache(
        self,
        cache_key: str,
        value: Dict[str, Any],
    ) -> bool:
        """
        Store value in Redis cache
        
        Args:
            cache_key: Cache key
            value: Value to cache
            
        Returns:
            Success status
        """
        try:
            # Remove transient fields before caching
            cache_value = {k: v for k, v in value.items() if k not in ["from_cache", "cache_stats"]}
            
            self.redis_client.setex(
                cache_key,
                self.cache_ttl,
                json.dumps(cache_value),
            )
            return True
        except Exception as e:
            logger.warning(f"Cache storage error: {str(e)}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Dict with cache stats
        """
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "total_requests": total_requests,
            "hit_rate_percentage": hit_rate,
            "available": self.cache_available,
        }
    
    def clear_cache(self, pattern: Optional[str] = None) -> int:
        """
        Clear cache entries
        
        Args:
            pattern: Optional pattern to match keys (default: all interp keys)
            
        Returns:
            Number of keys deleted
        """
        if not self.cache_available:
            return 0
        
        try:
            pattern = pattern or f"{self.CACHE_PREFIX}*"
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
            return 0
    
    def reset_cache_stats(self) -> None:
        """Reset cache statistics"""
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info("Cache statistics reset")


# Initialization helper
def create_cached_perplexity_service() -> CachedPerplexityService:
    """Factory function to create cached service from environment variables"""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable not set")
    
    return CachedPerplexityService(
        api_key=api_key,
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
        monthly_budget=float(os.getenv("MONTHLY_BUDGET", "5.0")),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        top_p=float(os.getenv("TOP_P", "0.9")),
        max_tokens=int(os.getenv("MAX_TOKENS", "1024")),
        timeout=int(os.getenv("TIMEOUT", "30")),
        cache_ttl=int(os.getenv("CACHE_TTL", str(CachedPerplexityService.CACHE_TTL))),
    )
