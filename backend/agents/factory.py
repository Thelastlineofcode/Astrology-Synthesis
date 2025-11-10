"""
Factory functions for creating LangChain agents.

Provides convenient creation of pre-configured agents with
proper initialization and dependency injection.
"""

from typing import Optional
import os
import logging

from .perplexity_agent import PerplexityInterpretationAgent
from .interpretation_agent import InterpretationAgent
from .orchestrator_agent import HybridOrchestratorAgent

logger = logging.getLogger(__name__)


def create_interpretation_agent(
    knowledge_service: Optional[Any] = None,
    verbose: bool = False,
) -> InterpretationAgent:
    """
    Create a template-based interpretation agent.

    Args:
        knowledge_service: Knowledge base service
        verbose: Enable verbose logging

    Returns:
        Configured InterpretationAgent
    """
    logger.info("Creating InterpretationAgent")
    return InterpretationAgent(
        knowledge_service=knowledge_service,
        verbose=verbose,
    )


def create_perplexity_agent(
    api_key: Optional[str] = None,
    model: str = "sonar-small",
    temperature: float = 0.7,
    max_iterations: int = 5,
    monthly_budget: float = 5.0,
    verbose: bool = False,
) -> PerplexityInterpretationAgent:
    """
    Create a Perplexity-powered interpretation agent.

    Args:
        api_key: Perplexity API key (reads from env if None)
        model: Model name
        temperature: LLM temperature
        max_iterations: Max agent iterations
        monthly_budget: Monthly budget in dollars
        verbose: Enable verbose logging

    Returns:
        Configured PerplexityInterpretationAgent

    Raises:
        ValueError: If API key not provided and not in environment
    """
    if api_key is None:
        api_key = os.getenv("PERPLEXITY_API_KEY")

    if not api_key:
        raise ValueError(
            "PERPLEXITY_API_KEY must be provided or set in environment"
        )

    logger.info(f"Creating PerplexityInterpretationAgent with model={model}")
    return PerplexityInterpretationAgent(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_iterations=max_iterations,
        monthly_budget=monthly_budget,
        verbose=verbose,
    )


def create_orchestrator_agent(
    perplexity_api_key: Optional[str] = None,
    knowledge_service: Optional[Any] = None,
    vector_store: Optional[Any] = None,
    default_strategy: str = "auto",
    monthly_budget: float = 5.0,
    verbose: bool = False,
) -> HybridOrchestratorAgent:
    """
    Create a hybrid orchestrator agent with all sub-agents.

    Args:
        perplexity_api_key: Perplexity API key (reads from env if None)
        knowledge_service: Knowledge base service
        vector_store: FAISS vector store
        default_strategy: Default strategy (auto, llm, kb, template)
        monthly_budget: Monthly budget for LLM calls
        verbose: Enable verbose logging

    Returns:
        Configured HybridOrchestratorAgent
    """
    logger.info("Creating HybridOrchestratorAgent with all sub-agents")

    # Create sub-agents
    template_agent = create_interpretation_agent(
        knowledge_service=knowledge_service,
        verbose=verbose,
    )

    perplexity_agent = None
    if perplexity_api_key or os.getenv("PERPLEXITY_API_KEY"):
        try:
            perplexity_agent = create_perplexity_agent(
                api_key=perplexity_api_key,
                monthly_budget=monthly_budget,
                verbose=verbose,
            )
            logger.info("Perplexity agent initialized successfully")
        except Exception as e:
            logger.warning(f"Could not initialize Perplexity agent: {str(e)}")

    # Create orchestrator
    orchestrator = HybridOrchestratorAgent(
        perplexity_agent=perplexity_agent,
        template_agent=template_agent,
        vector_store=vector_store,
        default_strategy=default_strategy,
        verbose=verbose,
    )

    logger.info("HybridOrchestratorAgent created successfully")
    return orchestrator


def create_default_orchestrator(verbose: bool = False) -> HybridOrchestratorAgent:
    """
    Create orchestrator with default configuration from environment.

    Reads configuration from environment variables:
    - PERPLEXITY_API_KEY: Perplexity API key
    - MONTHLY_BUDGET: Monthly LLM budget (default: 5.0)
    - DEFAULT_STRATEGY: Default strategy (default: auto)

    Args:
        verbose: Enable verbose logging

    Returns:
        Configured orchestrator agent
    """
    return create_orchestrator_agent(
        perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
        monthly_budget=float(os.getenv("MONTHLY_BUDGET", "5.0")),
        default_strategy=os.getenv("DEFAULT_STRATEGY", "auto"),
        verbose=verbose,
    )


# Convenience aliases
create_agent = create_interpretation_agent
create_llm_agent = create_perplexity_agent
create_orchestrator = create_orchestrator_agent
