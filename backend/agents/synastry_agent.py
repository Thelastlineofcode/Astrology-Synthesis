"""
Synastry Agent - Relationship Compatibility Analysis

LangChain agent specialized in analyzing relationship compatibility
between two birth charts using synastry techniques.
"""

from typing import Dict, List, Any, Optional
import logging
from langchain_community.chat_models import ChatPerplexity
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from .base_agent import BaseInterpretationAgent
from .synastry_tools import ALL_SYNASTRY_TOOLS
from .tools import CORE_TOOLS

logger = logging.getLogger(__name__)


# Synastry agent prompt
SYNASTRY_AGENT_PROMPT = """You are an expert relationship astrologer specializing in synastry analysis.

You have access to the following tools:
{tools}

Tool Names: {tool_names}

Your expertise includes:
- Analyzing inter-chart aspects between two people
- Interpreting house overlays and their effects on relationships
- Understanding composite charts
- Providing compatibility scores and insights
- Offering relationship guidance based on astrological patterns

When analyzing relationships:
1. Use tools to gather synastry data between the two charts
2. Consider both harmonious and challenging aspects
3. Look at house overlays to understand dynamic flow
4. Examine composite chart for relationship identity
5. Provide balanced, constructive guidance
6. Be honest about both strengths and challenges
7. Emphasize that astrology shows potentials, not destiny
8. Encourage growth and understanding

Remember:
- Every relationship has both gifts and growth areas
- Challenging aspects can create attraction and growth
- Focus on how to work with the energies present
- Respect free will and personal choice

Current conversation:
{chat_history}

User Query: {input}

Thought: {agent_scratchpad}
"""


class SynastryAgent(BaseInterpretationAgent):
    """
    LangChain agent for relationship compatibility analysis.

    Features:
    - Synastry analysis (inter-chart aspects)
    - House overlays interpretation
    - Composite chart analysis
    - Compatibility scoring
    - Relationship guidance
    """

    def __init__(
        self,
        api_key: str,
        model: str = "sonar-small",
        temperature: float = 0.7,
        max_iterations: int = 7,  # More iterations for complex synastry
        monthly_budget: float = 5.0,
        verbose: bool = False,
    ):
        """
        Initialize synastry agent.

        Args:
            api_key: Perplexity API key
            model: Model name
            temperature: LLM temperature
            max_iterations: Max iterations
            monthly_budget: Monthly budget
            verbose: Verbose logging
        """
        super().__init__(
            agent_name="SynastryAgent",
            description="Expert relationship astrologer for compatibility analysis",
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

        # Combine synastry tools with core tools
        self.tools = ALL_SYNASTRY_TOOLS + CORE_TOOLS

        # Create prompt
        self.prompt = PromptTemplate(
            template=SYNASTRY_AGENT_PROMPT,
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

        logger.info(f"Initialized {self.agent_name} with {len(self.tools)} tools")

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke synastry agent.

        Args:
            input_data: Input with 'query', 'chart1_id', 'chart2_id', etc.

        Returns:
            Synastry analysis dictionary
        """
        try:
            query = input_data.get("query", "Analyze compatibility")
            chart1_id = input_data.get("chart1_id")
            chart2_id = input_data.get("chart2_id")
            person1_name = input_data.get("person1_name", "Person 1")
            person2_name = input_data.get("person2_name", "Person 2")

            # Store chart info in memory
            if chart1_id and chart2_id:
                self.add_to_memory("chart1_id", chart1_id)
                self.add_to_memory("chart2_id", chart2_id)
                self.add_to_memory("person1_name", person1_name)
                self.add_to_memory("person2_name", person2_name)

            # Build input
            agent_input = {
                "input": query,
            }

            # Invoke agent
            result = self.agent_executor.invoke(agent_input)

            # Extract output
            analysis = result.get("output", "")

            # Update metrics
            tokens_used = len(analysis.split()) * 1.3
            cost = (tokens_used / 1000) * 0.0001
            self.update_metrics(int(tokens_used), cost)

            # Add to history
            self.add_to_history("user", query)
            self.add_to_history("assistant", analysis, {"cost": cost})

            return {
                "analysis": analysis,
                "type": "synastry",
                "person1_name": person1_name,
                "person2_name": person2_name,
                "model": self.model,
                "cost": cost,
                "tokens": int(tokens_used),
                "quality": 0.85,
                "strategy": "synastry_agent",
                "agent_name": self.agent_name,
                "budget_remaining": max(0, self.monthly_budget - self.total_cost),
            }

        except Exception as e:
            logger.error(f"Error in {self.agent_name}.invoke: {str(e)}")
            return {
                "error": str(e),
                "strategy": "synastry_agent_error",
                "agent_name": self.agent_name,
            }

    def analyze_compatibility(
        self,
        chart1: Dict[str, Any],
        chart2: Dict[str, Any],
        person1_name: str = "Person 1",
        person2_name: str = "Person 2",
    ) -> Dict[str, Any]:
        """
        Convenience method for full compatibility analysis.

        Args:
            chart1: First person's chart
            chart2: Second person's chart
            person1_name: First person's name
            person2_name: Second person's name

        Returns:
            Complete compatibility analysis
        """
        query = (
            f"Analyze the relationship compatibility between {person1_name} "
            f"and {person2_name}. Provide insights on emotional compatibility, "
            f"romantic chemistry, communication, and long-term potential."
        )

        return self.invoke({
            "query": query,
            "chart1_data": chart1,
            "chart2_data": chart2,
            "person1_name": person1_name,
            "person2_name": person2_name,
        })

    def get_relationship_advice(
        self,
        chart1_id: str,
        chart2_id: str,
        specific_area: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get relationship advice for a specific area.

        Args:
            chart1_id: First chart ID
            chart2_id: Second chart ID
            specific_area: Specific area (e.g., 'communication', 'intimacy')

        Returns:
            Relationship advice
        """
        if specific_area:
            query = f"What advice do you have for improving {specific_area} in this relationship?"
        else:
            query = "What are the key strengths and growth areas in this relationship?"

        return self.invoke({
            "query": query,
            "chart1_id": chart1_id,
            "chart2_id": chart2_id,
        })

    def get_tools(self) -> List[Any]:
        """Get list of tools."""
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
