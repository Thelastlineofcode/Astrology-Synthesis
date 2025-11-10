"""
Hybrid Orchestrator Agent

Coordinates multiple interpretation strategies with intelligent fallback.
Uses LangChain's agent framework for sophisticated decision-making.
"""

from typing import Dict, List, Any, Optional
import logging
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool

from .base_agent import BaseInterpretationAgent
from .perplexity_agent import PerplexityInterpretationAgent
from .interpretation_agent import InterpretationAgent

logger = logging.getLogger(__name__)


# Orchestrator prompt
ORCHESTRATOR_PROMPT = """You are an intelligent orchestrator for astrological interpretations.

You coordinate three interpretation strategies:

1. **Perplexity LLM** (High Quality, Low Cost: $0.0001/call)
   - Best for complex, nuanced interpretations
   - Use when: Quality is priority, budget available
   - Avoid when: Budget exhausted

2. **Knowledge Base** (Good Quality, Free)
   - Good for standard interpretations with context
   - Use when: Similar interpretations exist in KB
   - Avoid when: No relevant KB content

3. **Templates** (Basic Quality, Free, Instant)
   - Fast, reliable baseline interpretations
   - Use when: Simple request or fallback needed
   - Always available

Your job: Select the BEST strategy for each request based on:
- Query complexity
- Budget availability
- Quality requirements
- Response time needs

Available tools:
{tools}

Current conversation:
{chat_history}

User Request: {input}

Thought: {agent_scratchpad}
"""


class HybridOrchestratorAgent(BaseInterpretationAgent):
    """
    Orchestrator agent that intelligently selects interpretation strategy.

    Features:
    - Multi-strategy coordination
    - Budget-aware routing
    - Quality optimization
    - Automatic fallbacks
    """

    def __init__(
        self,
        perplexity_agent: Optional[PerplexityInterpretationAgent] = None,
        template_agent: Optional[InterpretationAgent] = None,
        vector_store: Optional[Any] = None,
        default_strategy: str = "auto",
        verbose: bool = False,
    ):
        """
        Initialize hybrid orchestrator.

        Args:
            perplexity_agent: Perplexity interpretation agent
            template_agent: Template interpretation agent
            vector_store: FAISS vector store for KB search
            default_strategy: Default strategy (auto, llm, kb, template)
            verbose: Enable verbose logging
        """
        super().__init__(
            agent_name="HybridOrchestratorAgent",
            description="Intelligent multi-strategy interpretation orchestrator",
            temperature=0.3,  # Lower temperature for more deterministic routing
            max_iterations=3,
            verbose=verbose,
        )

        self.perplexity_agent = perplexity_agent
        self.template_agent = template_agent
        self.vector_store = vector_store
        self.default_strategy = default_strategy

        # Strategy statistics
        self.strategy_counts = {
            "llm": 0,
            "kb": 0,
            "template": 0,
            "fallback": 0,
        }

        # Create orchestrator tools
        self.tools = self._create_orchestrator_tools()

        logger.info(f"Initialized {self.agent_name} with {len(self.tools)} tools")

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate interpretation generation.

        Args:
            input_data: Input with 'query', 'chart_data', 'strategy', etc.

        Returns:
            Interpretation result dictionary
        """
        try:
            query = input_data.get("query", "")
            chart_data = input_data.get("chart_data", {})
            requested_strategy = input_data.get("strategy", self.default_strategy)

            # Select strategy
            if requested_strategy == "auto":
                strategy = self._select_strategy(query, chart_data)
            else:
                strategy = requested_strategy

            logger.info(f"Selected strategy: {strategy}")

            # Execute strategy
            result = self._execute_strategy(strategy, input_data)

            # Update statistics
            actual_strategy = result.get("strategy", strategy)
            if actual_strategy in self.strategy_counts:
                self.strategy_counts[actual_strategy] += 1

            # Add orchestration metadata
            result["orchestrator"] = self.agent_name
            result["selected_strategy"] = strategy
            result["strategy_stats"] = self.strategy_counts.copy()

            return result

        except Exception as e:
            logger.error(f"Error in {self.agent_name}.invoke: {str(e)}")
            return {
                "error": str(e),
                "strategy": "orchestrator_error",
                "agent_name": self.agent_name,
            }

    def _select_strategy(
        self,
        query: str,
        chart_data: Dict[str, Any],
    ) -> str:
        """
        Intelligently select best strategy.

        Selection logic:
        1. Check Perplexity budget - if available and query is complex, use LLM
        2. Check vector store - if relevant content exists, use KB
        3. Fallback to templates

        Args:
            query: User query
            chart_data: Chart data

        Returns:
            Strategy name: llm, kb, or template
        """
        # Check LLM budget
        if self.perplexity_agent and self.perplexity_agent.is_budget_available():
            # Use LLM for complex queries
            if self._is_complex_query(query):
                logger.info("Strategy selection: LLM (complex query, budget available)")
                return "llm"

        # Check vector store
        if self.vector_store:
            # TODO: Implement actual vector store check
            # For now, use KB for medium complexity
            if len(query.split()) > 5:
                logger.info("Strategy selection: KB (vector store available)")
                return "kb"

        # Fallback to templates
        logger.info("Strategy selection: Template (fallback)")
        return "template"

    def _is_complex_query(self, query: str) -> bool:
        """
        Determine if query is complex.

        Complex queries have:
        - Multiple planets mentioned
        - Aspects or relationships
        - Timing questions
        - Personal context

        Args:
            query: User query

        Returns:
            True if complex
        """
        complexity_indicators = [
            "aspect",
            "relationship",
            "transit",
            "timing",
            "when",
            "how",
            "why",
            "synthesis",
            "combination",
        ]

        query_lower = query.lower()
        matches = sum(1 for indicator in complexity_indicators if indicator in query_lower)

        return matches >= 2 or len(query.split()) > 15

    def _execute_strategy(
        self,
        strategy: str,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute selected strategy with fallback."""
        try:
            if strategy == "llm" and self.perplexity_agent:
                result = self.perplexity_agent.invoke(input_data)
                if "error" not in result:
                    return result
                logger.warning("LLM strategy failed, falling back...")

            if strategy == "kb" and self.vector_store:
                result = self._execute_kb_strategy(input_data)
                if "error" not in result:
                    return result
                logger.warning("KB strategy failed, falling back...")

            # Fallback to templates
            if self.template_agent:
                return self.template_agent.invoke(input_data)

            # Final fallback
            return {
                "interpretation": "Unable to generate interpretation",
                "strategy": "fallback_error",
                "error": "All strategies failed",
            }

        except Exception as e:
            logger.error(f"Error executing strategy {strategy}: {str(e)}")
            return {
                "error": str(e),
                "strategy": "execution_error",
            }

    def _execute_kb_strategy(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute knowledge base strategy."""
        try:
            query = input_data.get("query", "")
            chart_data = input_data.get("chart_data", {})

            # TODO: Implement actual vector search
            interpretation = f"Knowledge base interpretation for: {query}"

            return {
                "interpretation": interpretation,
                "type": input_data.get("type", "general"),
                "cost": 0.0,
                "quality": 0.80,
                "strategy": "kb",
                "source": "vector_store",
            }

        except Exception as e:
            logger.error(f"KB strategy error: {str(e)}")
            return {"error": str(e)}

    def _create_orchestrator_tools(self) -> List[Tool]:
        """Create tools for the orchestrator."""
        tools = []

        # Tool to check LLM budget
        if self.perplexity_agent:
            tools.append(Tool(
                name="check_llm_budget",
                func=lambda _: str(self.perplexity_agent.get_budget_info()),
                description="Check Perplexity LLM budget availability",
            ))

        # Tool to search knowledge base
        if self.vector_store:
            tools.append(Tool(
                name="search_knowledge_base",
                func=lambda query: f"KB results for: {query}",
                description="Search the astrological knowledge base",
            ))

        return tools

    def get_tools(self) -> List[Any]:
        """Get orchestrator tools."""
        return self.tools

    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        total = sum(self.strategy_counts.values())

        return {
            "total_requests": total,
            "strategy_counts": self.strategy_counts.copy(),
            "strategy_percentages": {
                strategy: (count / total * 100) if total > 0 else 0
                for strategy, count in self.strategy_counts.items()
            },
            "perplexity_budget": (
                self.perplexity_agent.get_budget_info()
                if self.perplexity_agent
                else None
            ),
        }
