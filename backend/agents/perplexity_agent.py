"""
Perplexity-powered LangChain agent for astrological interpretations.

Uses Perplexity's sonar-small model via LangChain's ChatOpenAI interface.
"""

from typing import Dict, List, Any, Optional
import logging
from langchain_community.chat_models import ChatPerplexity
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from .base_agent import BaseInterpretationAgent
from .tools import ALL_TOOLS

logger = logging.getLogger(__name__)


# Agent prompt template
PERPLEXITY_AGENT_PROMPT = """You are an expert astrological interpreter with access to tools.

You have access to the following tools:
{tools}

Tool Names: {tool_names}

Your task is to generate insightful, personalized astrological interpretations.

When interpreting:
1. Use tools to gather necessary chart data and astrological information
2. Synthesize information from multiple sources
3. Provide warm, compassionate, and actionable guidance
4. Be specific and avoid generic statements
5. Consider both Western and Vedic astrological traditions

Current conversation:
{chat_history}

User Query: {input}

Thought: {agent_scratchpad}
"""


class PerplexityInterpretationAgent(BaseInterpretationAgent):
    """
    LangChain agent using Perplexity's sonar-small model.

    Features:
    - ReAct-style reasoning
    - Tool calling for chart data access
    - Conversation memory
    - Budget tracking
    - Cost-effective ($0.0001/call)
    """

    def __init__(
        self,
        api_key: str,
        model: str = "sonar-small",
        temperature: float = 0.7,
        max_iterations: int = 5,
        monthly_budget: float = 5.0,
        verbose: bool = False,
    ):
        """
        Initialize Perplexity interpretation agent.

        Args:
            api_key: Perplexity API key
            model: Model name (default: sonar-small)
            temperature: LLM temperature
            max_iterations: Max agent iterations
            monthly_budget: Monthly budget in dollars
            verbose: Enable verbose logging
        """
        super().__init__(
            agent_name="PerplexityInterpretationAgent",
            description="Expert astrological interpreter using Perplexity sonar-small",
            temperature=temperature,
            max_iterations=max_iterations,
            verbose=verbose,
        )

        self.api_key = api_key
        self.model = model
        self.monthly_budget = monthly_budget

        # Initialize LangChain components
        self.llm = ChatPerplexity(
            api_key=api_key,
            model=model,
            temperature=temperature,
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

        self.tools = ALL_TOOLS

        # Create prompt
        self.prompt = PromptTemplate(
            template=PERPLEXITY_AGENT_PROMPT,
            input_variables=["input", "chat_history", "agent_scratchpad"],
            partial_variables={
                "tools": self._format_tools(),
                "tool_names": ", ".join([t.name for t in self.tools]),
            },
        )

        # Create agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt,
        )

        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            max_iterations=max_iterations,
            verbose=verbose,
            handle_parsing_errors=True,
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

            # Add chart data to context
            if chart_data:
                self.add_to_memory("current_chart", chart_data)

            # Build input
            agent_input = {
                "input": query,
            }

            # Invoke agent
            result = self.agent_executor.invoke(agent_input)

            # Extract output
            interpretation = result.get("output", "")

            # Update metrics (approximate cost)
            tokens_used = len(interpretation.split()) * 1.3  # Rough estimate
            cost = (tokens_used / 1000) * 0.0001  # sonar-small pricing
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
                "quality": 0.85,
                "strategy": "perplexity_agent",
                "agent_name": self.agent_name,
                "budget_remaining": max(0, self.monthly_budget - self.total_cost),
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
        return self.tools

    def _format_tools(self) -> str:
        """Format tools for prompt."""
        tool_strings = []
        for tool in self.tools:
            tool_strings.append(f"- {tool.name}: {tool.description}")
        return "\n".join(tool_strings)

    def is_budget_available(self) -> bool:
        """Check if budget is available."""
        return self.total_cost < self.monthly_budget

    def get_budget_info(self) -> Dict[str, Any]:
        """Get budget information."""
        return {
            "total_budget": self.monthly_budget,
            "used": self.total_cost,
            "remaining": max(0, self.monthly_budget - self.total_cost),
            "percentage_used": (
                (self.total_cost / self.monthly_budget) * 100
                if self.monthly_budget > 0
                else 0
            ),
        }
