"""
Factory functions for creating LangChain agents.

Provides convenient creation of pre-configured agents with
proper initialization and dependency injection.
"""

from typing import Optional
import os
import logging

from .gemini_agent import GeminiInterpretationAgent

logger = logging.getLogger(__name__)


def create_gemini_agent(
    api_key: Optional[str] = None,
    model: str = "gemini-pro",
    temperature: float = 0.7,
    max_iterations: int = 5,
    verbose: bool = False,
) -> GeminiInterpretationAgent:
    """
    Create a Gemini-powered interpretation agent.

    Args:
        api_key: Google API key (reads from env if None)
        model: Model name (default: gemini-pro)
        temperature: LLM temperature
        max_iterations: Max agent iterations
        verbose: Enable verbose logging

    Returns:
        Configured GeminiInterpretationAgent

    Raises:
        ValueError: If API key not provided and not in environment
    """
    if api_key is None:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY must be provided or set in environment"
        )

    logger.info(f"Creating GeminiInterpretationAgent with model={model}")
    return GeminiInterpretationAgent(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_iterations=max_iterations,
        verbose=verbose,
    )


# Convenience aliases for Gemini agent
create_agent = create_gemini_agent
create_llm_agent = create_gemini_agent
