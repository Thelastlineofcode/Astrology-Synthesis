"""
Hybrid Interpretation Service
Orchestrates 3-tier fallback strategy for interpretations
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from backend.services.cached_perplexity_service import CachedPerplexityService
from backend.services.faiss_vector_store import FAISSVectorStore
from backend.services.knowledge_service import KnowledgeService
from backend.services.interpretation_service import InterpretationService

logger = logging.getLogger(__name__)


class HybridInterpretationService:
    """
    Hybrid service using 3-tier fallback strategy:
    
    Tier 1: Perplexity LLM (best quality, $0.0001/interp)
    Tier 2: FAISS semantic search (good quality, $0, fast)
    Tier 3: Phase 4 templates (basic quality, $0, guaranteed)
    """
    
    def __init__(
        self,
        llm_service: Optional[CachedPerplexityService] = None,
        vector_store: Optional[FAISSVectorStore] = None,
        kb_service: Optional[KnowledgeService] = None,
        interpretation_service: Optional[InterpretationService] = None,
    ):
        """
        Initialize Hybrid Interpretation Service
        
        Args:
            llm_service: Cached Perplexity LLM service
            vector_store: FAISS vector store
            kb_service: Knowledge base service
            interpretation_service: Phase 4 interpretation service
        """
        self.llm_service = llm_service
        self.vector_store = vector_store
        self.kb_service = kb_service
        self.interpretation_service = interpretation_service
        
        # Statistics
        self.llm_count = 0
        self.kb_count = 0
        self.template_count = 0
        self.strategy_selection_log = []
        
        logger.info("HybridInterpretationService initialized")
    
    def interpret(
        self,
        chart_data: Dict[str, Any],
        interpretation_type: str,
        strategy: str = "auto",
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate interpretation using hybrid strategy
        
        Args:
            chart_data: Chart data dict
            interpretation_type: Type of interpretation
            strategy: Strategy to use (auto, llm, kb, or template)
            context: Additional context
            
        Returns:
            Dict with interpretation and metadata
        """
        start_time = datetime.now()
        
        # Select strategy if auto
        if strategy == "auto":
            strategy = self._select_strategy()
        
        # Execute strategy
        if strategy == "llm":
            result = self._strategy_llm(chart_data, interpretation_type, context)
            self.llm_count += 1
        elif strategy == "kb":
            result = self._strategy_kb(chart_data, interpretation_type)
            self.kb_count += 1
        else:  # template
            result = self._strategy_template(chart_data, interpretation_type)
            self.template_count += 1
        
        # Add metadata
        elapsed = (datetime.now() - start_time).total_seconds()
        result["execution_time"] = elapsed
        result["strategy_used"] = strategy
        
        # Log strategy selection
        self.strategy_selection_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": interpretation_type,
            "strategy": strategy,
            "quality": result.get("quality", 0),
            "time": elapsed,
        })
        
        return result
    
    def _select_strategy(self) -> str:
        """
        Select best strategy based on availability
        
        Priority:
        1. LLM (if budget available)
        2. Vector store (if indexed)
        3. Templates (always available)
        
        Returns:
            Strategy name: llm, kb, or template
        """
        # Check LLM budget
        if self.llm_service:
            budget = self.llm_service.get_budget_remaining()
            if budget["cost_remaining"] > 0.01:
                logger.info("Strategy: LLM (budget available)")
                return "llm"
        
        # Check vector store
        if self.vector_store and self.vector_store.text_count > 0:
            logger.info("Strategy: Vector store (fallback from LLM)")
            return "kb"
        
        # Template fallback
        logger.info("Strategy: Template (final fallback)")
        return "template"
    
    def _strategy_llm(
        self,
        chart_data: Dict[str, Any],
        interpretation_type: str,
        context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        LLM strategy: Use Perplexity for best quality
        
        Quality: 85%+
        Cost: $0.0001/interpretation
        Speed: ~2 seconds
        """
        try:
            if not self.llm_service:
                return {"error": "LLM service not available"}
            
            result = self.llm_service.generate_interpretation(
                chart_data,
                interpretation_type,
                context,
            )
            
            if result.get("error"):
                logger.warning(f"LLM error: {result['error']}")
                return result
            
            return {
                "interpretation": result.get("interpretation", ""),
                "type": interpretation_type,
                "quality": 0.85,
                "source": "perplexity_llm",
                "cost": result.get("cost", 0.0),
                "tokens": result.get("tokens", {}),
                "budget": result.get("budget", {}),
                "model": "sonar-small",
            }
            
        except Exception as e:
            logger.error(f"LLM strategy error: {str(e)}")
            return {"error": f"LLM error: {str(e)}"}
    
    def _strategy_kb(
        self,
        chart_data: Dict[str, Any],
        interpretation_type: str,
    ) -> Dict[str, Any]:
        """
        Knowledge Base strategy: Use FAISS vector search
        
        Quality: 80%+
        Cost: $0
        Speed: <100ms
        """
        try:
            if not self.vector_store:
                return {"error": "Vector store not available"}
            
            # Build search query
            sun = chart_data.get("sun", "")
            moon = chart_data.get("moon", "")
            query = f"{interpretation_type} {sun} {moon}"
            
            # Search similar texts
            results = self.vector_store.search(query, k=3)
            
            if not results:
                logger.warning(f"No KB results for query: {query}")
                return {"error": "No knowledge base results"}
            
            # Compile interpretation from top results
            interpretation = self._compile_kb_interpretation(results)
            
            return {
                "interpretation": interpretation,
                "type": interpretation_type,
                "quality": 0.80,
                "source": "vector_store",
                "cost": 0.0,
                "search_results": len(results),
                "top_similarity": results[0].get("similarity", 0) if results else 0,
            }
            
        except Exception as e:
            logger.error(f"KB strategy error: {str(e)}")
            return {"error": f"KB error: {str(e)}"}
    
    def _strategy_template(
        self,
        chart_data: Dict[str, Any],
        interpretation_type: str,
    ) -> Dict[str, Any]:
        """
        Template strategy: Use Phase 4 templates
        
        Quality: 70%+
        Cost: $0
        Speed: <10ms
        """
        try:
            if not self.interpretation_service:
                return {"error": "Interpretation service not available"}
            
            # Get template-based interpretation
            sun = chart_data.get("sun", "")
            
            # Call appropriate interpretation method
            if interpretation_type == "sun":
                interpretation = self.interpretation_service.generate_sun_sign_interpretation(sun)
            elif interpretation_type == "moon":
                moon = chart_data.get("moon", "")
                interpretation = self.interpretation_service.generate_moon_sign_interpretation(moon)
            else:
                interpretation = f"Interpretation for {interpretation_type}: {sun}"
            
            return {
                "interpretation": interpretation,
                "type": interpretation_type,
                "quality": 0.70,
                "source": "template",
                "cost": 0.0,
            }
            
        except Exception as e:
            logger.error(f"Template strategy error: {str(e)}")
            return {"error": f"Template error: {str(e)}"}
    
    def _compile_kb_interpretation(self, results: list) -> str:
        """Compile interpretation from search results"""
        if not results:
            return ""
        
        # Use top result
        top_result = results[0]
        interpretation = f"Based on knowledge base: {top_result.get('text', '')}\n\n"
        interpretation += f"Confidence: {top_result.get('similarity', 0):.1%}"
        
        return interpretation
    
    def get_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        total = self.llm_count + self.kb_count + self.template_count
        
        return {
            "total_interpretations": total,
            "by_strategy": {
                "llm": self.llm_count,
                "vector_store": self.kb_count,
                "template": self.template_count,
            },
            "percentages": {
                "llm": (self.llm_count / total * 100) if total > 0 else 0,
                "vector_store": (self.kb_count / total * 100) if total > 0 else 0,
                "template": (self.template_count / total * 100) if total > 0 else 0,
            },
            "strategy_log_size": len(self.strategy_selection_log),
        }


# Factory function
def create_hybrid_interpretation_service(
    llm_service: Optional[CachedPerplexityService] = None,
    vector_store: Optional[FAISSVectorStore] = None,
    kb_service: Optional[KnowledgeService] = None,
    interpretation_service: Optional[InterpretationService] = None,
) -> HybridInterpretationService:
    """Create hybrid interpretation service"""
    return HybridInterpretationService(
        llm_service=llm_service,
        vector_store=vector_store,
        kb_service=kb_service,
        interpretation_service=interpretation_service,
    )
