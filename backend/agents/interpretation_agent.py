"""
Template-based interpretation agent with knowledge base integration.

This agent uses templates and knowledge base lookups for fast,
cost-free interpretations with fallback to LLM when needed.
"""

from typing import Dict, List, Any, Optional
import logging
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.llms.fake import FakeListLLM

from .base_agent import BaseInterpretationAgent
from .tools import CORE_TOOLS, KNOWLEDGE_TOOLS

logger = logging.getLogger(__name__)


# Interpretation templates
INTERPRETATION_TEMPLATES = {
    "sun_sign": "Your Sun in {sign} represents your core identity and life force. {detailed_interpretation}",
    "moon_sign": "Your Moon in {sign} governs your emotions and inner world. {detailed_interpretation}",
    "ascendant": "Your Ascendant in {sign} is the mask you present to the world. {detailed_interpretation}",
    "nakshatra": "Your birth nakshatra {nakshatra} (pada {pada}) holds deep Vedic significance. {detailed_interpretation}",
}


class InterpretationAgent(BaseInterpretationAgent):
    """
    Template and knowledge-based interpretation agent.

    Features:
    - Template-based interpretations (instant, $0)
    - Knowledge base lookups via tools
    - Fallback to simple LLM for synthesis
    - Zero cost for basic interpretations
    """

    def __init__(
        self,
        knowledge_service: Optional[Any] = None,
        verbose: bool = False,
    ):
        """
        Initialize interpretation agent.

        Args:
            knowledge_service: Knowledge base service
            verbose: Enable verbose logging
        """
        super().__init__(
            agent_name="TemplateInterpretationAgent",
            description="Fast template-based interpreter with KB integration",
            temperature=0.0,
            max_iterations=3,
            verbose=verbose,
        )

        self.knowledge_service = knowledge_service
        self.templates = INTERPRETATION_TEMPLATES

        # Use fake LLM for zero-cost template filling
        # In production, could use a small local model
        self.llm = FakeListLLM(
            responses=[
                "Based on the chart data, here is your interpretation...",
                "The planetary positions suggest...",
                "This placement indicates...",
            ]
        )

        self.tools = CORE_TOOLS + KNOWLEDGE_TOOLS

        logger.info(f"Initialized {self.agent_name}")

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate interpretation using templates and knowledge base.

        Args:
            input_data: Input with 'type', 'chart_data', etc.

        Returns:
            Interpretation dictionary
        """
        try:
            interpretation_type = input_data.get("type", "general")
            chart_data = input_data.get("chart_data", {})

            # Use template if available
            if interpretation_type in self.templates:
                interpretation = self._generate_from_template(
                    interpretation_type,
                    chart_data,
                )
            else:
                # Fallback to general interpretation
                interpretation = self._generate_general_interpretation(chart_data)

            # Update metrics (no cost for templates)
            self.update_metrics(tokens_used=0, cost=0.0)

            # Add to history
            self.add_to_history("user", f"Generate {interpretation_type} interpretation")
            self.add_to_history("assistant", interpretation)

            return {
                "interpretation": interpretation,
                "type": interpretation_type,
                "model": "template",
                "cost": 0.0,
                "tokens": 0,
                "quality": 0.70,
                "strategy": "template",
                "agent_name": self.agent_name,
                "source": "template",
            }

        except Exception as e:
            logger.error(f"Error in {self.agent_name}.invoke: {str(e)}")
            return {
                "error": str(e),
                "strategy": "template_error",
                "agent_name": self.agent_name,
            }

    def _generate_from_template(
        self,
        interpretation_type: str,
        chart_data: Dict[str, Any],
    ) -> str:
        """Generate interpretation from template."""
        template = self.templates.get(interpretation_type, "")

        # Extract relevant data
        if interpretation_type == "sun_sign":
            sign = chart_data.get("sun_sign", "Unknown")
            detailed = self._get_detailed_interpretation(f"Sun in {sign}")
            return template.format(sign=sign, detailed_interpretation=detailed)

        elif interpretation_type == "moon_sign":
            sign = chart_data.get("moon_sign", "Unknown")
            detailed = self._get_detailed_interpretation(f"Moon in {sign}")
            return template.format(sign=sign, detailed_interpretation=detailed)

        elif interpretation_type == "ascendant":
            sign = chart_data.get("ascendant", "Unknown")
            detailed = self._get_detailed_interpretation(f"Ascendant in {sign}")
            return template.format(sign=sign, detailed_interpretation=detailed)

        elif interpretation_type == "nakshatra":
            nakshatra = chart_data.get("nakshatra", "Unknown")
            pada = chart_data.get("pada", 1)
            detailed = self._get_detailed_interpretation(f"{nakshatra} nakshatra")
            return template.format(
                nakshatra=nakshatra,
                pada=pada,
                detailed_interpretation=detailed,
            )

        return f"Interpretation for {interpretation_type} based on chart data."

    def _get_detailed_interpretation(self, query: str) -> str:
        """Get detailed interpretation from knowledge base."""
        try:
            # TODO: Implement actual knowledge base lookup
            # For now, return placeholder
            return f"This placement brings unique energies and opportunities for growth."
        except Exception as e:
            logger.warning(f"KB lookup failed: {str(e)}")
            return "This placement has significant astrological meaning."

    def _generate_general_interpretation(self, chart_data: Dict[str, Any]) -> str:
        """Generate general interpretation."""
        sun = chart_data.get("sun_sign", "Unknown")
        moon = chart_data.get("moon_sign", "Unknown")
        asc = chart_data.get("ascendant", "Unknown")

        return (
            f"Your astrological signature shows Sun in {sun}, "
            f"Moon in {moon}, and Ascendant in {asc}. "
            f"This unique combination shapes your personality, emotions, and life path."
        )

    def get_tools(self) -> List[Any]:
        """Get list of tools."""
        return self.tools

    def add_template(self, template_id: str, template_text: str) -> None:
        """Add a custom template."""
        self.templates[template_id] = template_text
        logger.info(f"Added template: {template_id}")
