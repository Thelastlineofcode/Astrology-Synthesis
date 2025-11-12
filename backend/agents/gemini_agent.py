"""
Gemini-powered LangChain agent for astrological interpretations.

Uses Google's Gemini (gemini-pro) model via LangChain's ChatGoogleGenerativeAI interface.
Free tier available with generous limits.
"""

from typing import Dict, List, Any, Optional
import logging
from langchain_google_genai import ChatGoogleGenerativeAI

from .base_agent import BaseInterpretationAgent

logger = logging.getLogger(__name__)


class GeminiInterpretationAgent(BaseInterpretationAgent):
    """
    Simple Gemini-powered interpretation agent.

    Features:
    - Direct LLM invocation
    - Conversation memory
    - Free tier with generous limits
    - Fast response times
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-pro",
        temperature: float = 0.7,
        max_iterations: int = 5,
        verbose: bool = False,
    ):
        """
        Initialize Gemini interpretation agent.

        Args:
            api_key: Google API key
            model: Model name (default: gemini-pro)
            temperature: LLM temperature
            max_iterations: Max agent iterations
            verbose: Enable verbose logging
        """
        super().__init__(
            agent_name="GeminiInterpretationAgent",
            description="Expert astrological interpreter using Google Gemini",
            temperature=temperature,
            max_iterations=max_iterations,
            verbose=verbose,
        )

        self.api_key = api_key
        self.model = model

        # Initialize LangChain components
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
            convert_system_message_to_human=True,  # Gemini requires this
        )

        logger.info(f"Initialized {self.agent_name} with model={model}")

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent to generate interpretation.

        Args:
            input_data: Input dictionary with 'query' and optional 'chart_data'

        Returns:
            Dictionary with 'interpretation', 'cost', 'tokens', etc.
        """
        try:
            query = input_data.get("query", "")
            chart_data = input_data.get("chart_data", {})

            # Build prompt with chart data
            prompt = f"""You are an expert astrological interpreter specializing in both Western and Vedic astrology.

Your task is to provide insightful, personalized interpretations that are:
- Warm and compassionate
- Specific and actionable
- Based on astrological principles
- Avoiding generic statements

Query: {query}

Chart Data: {chart_data if chart_data else 'None provided'}

Provide a detailed, insightful interpretation:"""

            # Invoke LLM
            response = self.llm.invoke(prompt)
            interpretation = response.content if hasattr(response, 'content') else str(response)

            # Update metrics (Gemini is free, but track tokens)
            tokens_used = len(interpretation.split()) * 1.3  # Rough estimate
            cost = 0.0  # Free tier
            self.update_metrics(int(tokens_used), cost)

            # Add to history
            self.add_to_history("user", query)
            self.add_to_history("assistant", interpretation, {"cost": cost})

            return {
                "interpretation": interpretation,
                "type": input_data.get("type", "general"),
                "model": self.model,
                "cost": cost,
                "tokens": int(tokens_used),
                "quality": 0.90,  # Gemini 1.5 is high quality
                "strategy": "gemini_agent",
                "agent_name": self.agent_name,
            }

        except Exception as e:
            logger.error(f"Error in {self.agent_name}.invoke: {str(e)}")
            return {
                "error": str(e),
                "strategy": "agent_error",
                "agent_name": self.agent_name,
            }

    def get_tools(self) -> List[Any]:
        """Get list of tools available to this agent."""
        return []
