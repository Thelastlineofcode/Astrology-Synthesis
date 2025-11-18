"""
Personal Development Agent - Coaching and Wellness Tool

LangChain agent specialized in personal development insights using
numerology and astrology (when available).

CRITICAL COMPLIANCE NOTICE:
This agent is designed EXCLUSIVELY for personal development, coaching,
and wellness purposes. It is NOT intended for and must NOT be used for:
- Hiring decisions
- Promotion decisions
- Performance evaluation
- Employee assessment
- Any employment-related decisions

Legal Positioning:
- Personal development tool
- Coaching conversation facilitator
- Team building activity
- Wellness program component
"""

from typing import Dict, List, Any, Optional
import logging
from langchain_community.chat_models import ChatPerplexity
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

from .base_agent import BaseInterpretationAgent
from .personal_development_tools import ALL_PERSONAL_DEVELOPMENT_TOOLS
from .tools import CORE_TOOLS

logger = logging.getLogger(__name__)


# Personal development agent prompt
PERSONAL_DEVELOPMENT_AGENT_PROMPT = """You are an expert personal development coach specializing in using astrological and numerological insights for self-awareness and growth.

CRITICAL: You are a COACHING TOOL, not an assessment or evaluation system.
- Your insights are for personal reflection and development ONLY
- NEVER frame insights as assessments or evaluations
- NEVER suggest using insights for hiring, promotion, or employment decisions
- Always emphasize free will, personal choice, and growth potential
- Focus on strengths, opportunities, and self-awareness

You have access to the following tools:
{tools}

Tool Names: {tool_names}

Your expertise includes:
- Numerology insights (life path, destiny, soul urge, personality numbers)
- Astrological patterns (when data is available)
- Personal development coaching
- Team dynamics and communication styles
- Work style insights for self-awareness
- Growth opportunity identification

When providing coaching:
1. Use tools to gather personal development data
2. Focus on strengths and natural tendencies
3. Frame challenges as growth opportunities
4. Provide specific, actionable reflection prompts
5. Encourage self-awareness and personal choice
6. Be warm, supportive, and non-judgmental
7. Respect the mystical nature of these tools
8. Remind users this is NOT scientific or deterministic

Coaching Philosophy:
- Everyone has unique gifts and strengths
- Self-awareness enables growth
- There are no "good" or "bad" numbers/signs
- Personal development is a journey, not a destination
- These tools are conversation starters, not answers

Current conversation:
{chat_history}

User Query: {input}

Thought: {agent_scratchpad}
"""


class PersonalDevelopmentAgent(BaseInterpretationAgent):
    """
    LangChain agent for personal development coaching.

    Features:
    - Numerology insights (works with date only)
    - Astrological insights (when data available)
    - Team dynamics analysis
    - Communication style mapping
    - Coaching conversation facilitation
    """

    def __init__(
        self,
        api_key: str,
        model: str = "sonar-small",
        temperature: float = 0.7,
        max_iterations: int = 6,
        monthly_budget: float = 5.0,
        verbose: bool = False,
    ):
        """
        Initialize personal development agent.

        Args:
            api_key: Perplexity API key
            model: Model name
            temperature: LLM temperature (0.7 for coaching warmth)
            max_iterations: Max iterations
            monthly_budget: Monthly budget
            verbose: Verbose logging
        """
        super().__init__(
            agent_name="PersonalDevelopmentAgent",
            description="Personal development coach using numerology and astrology",
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

        # Combine personal development tools with core tools
        self.tools = ALL_PERSONAL_DEVELOPMENT_TOOLS + CORE_TOOLS

        # Create prompt
        self.prompt = PromptTemplate(
            template=PERSONAL_DEVELOPMENT_AGENT_PROMPT,
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

        logger.info(
            f"Initialized {self.agent_name} with {len(self.tools)} tools "
            "(COACHING TOOL - NOT FOR EMPLOYMENT DECISIONS)"
        )

    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke personal development agent.

        Args:
            input_data: Input with 'query', 'birth_date', optional 'full_name', etc.

        Returns:
            Coaching insights dictionary
        """
        try:
            query = input_data.get("query", "Provide personal development insights")
            birth_date = input_data.get("birth_date")
            full_name = input_data.get("full_name")

            # Store context in memory
            if birth_date:
                self.add_to_memory("birth_date", str(birth_date))
            if full_name:
                self.add_to_memory("full_name", full_name)

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
                "type": "personal_development",
                "model": self.model,
                "cost": cost,
                "tokens": int(tokens_used),
                "quality": 0.85,
                "strategy": "personal_development_agent",
                "agent_name": self.agent_name,
                "budget_remaining": max(0, self.monthly_budget - self.total_cost),
                "disclaimer": (
                    "This coaching insight is for personal development and "
                    "self-reflection only. Not for employment decisions."
                ),
            }

        except Exception as e:
            logger.error(f"Error in {self.agent_name}.invoke: {str(e)}")
            return {
                "error": str(e),
                "strategy": "personal_development_agent_error",
                "agent_name": self.agent_name,
            }

    def get_personal_insights(
        self,
        birth_date: str,
        full_name: Optional[str] = None,
        focus_area: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Convenience method for personal insights.

        Args:
            birth_date: Birth date (YYYY-MM-DD)
            full_name: Full birth name (optional)
            focus_area: Specific area to focus on (optional)

        Returns:
            Personal development insights
        """
        if focus_area:
            query = (
                f"Provide personal development insights with focus on {focus_area}. "
                f"Birth date: {birth_date}"
            )
        else:
            query = f"Provide comprehensive personal development insights. Birth date: {birth_date}"

        if full_name:
            query += f", Name: {full_name}"

        return self.invoke({
            "query": query,
            "birth_date": birth_date,
            "full_name": full_name,
        })

    def get_team_insights(
        self,
        team_data: List[Dict[str, Any]],
        team_name: str = "Team",
    ) -> Dict[str, Any]:
        """
        Get team dynamics insights.

        Args:
            team_data: List of team member data
            team_name: Name of the team

        Returns:
            Team dynamics insights
        """
        query = (
            f"Analyze team dynamics for '{team_name}' and provide insights on "
            f"communication styles, collaboration opportunities, and team strengths."
        )

        return self.invoke({
            "query": query,
            "team_data": team_data,
            "team_name": team_name,
        })

    def get_coaching_session(
        self,
        reading_id: str,
        specific_question: str,
    ) -> Dict[str, Any]:
        """
        Conduct a coaching session based on a previous reading.

        Args:
            reading_id: ID of previous reading
            specific_question: Specific question for coaching

        Returns:
            Coaching insights
        """
        query = (
            f"As a personal development coach, please address this question: "
            f"{specific_question}. Use the reading context if available."
        )

        return self.invoke({
            "query": query,
            "reading_id": reading_id,
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

    def add_compliance_reminder(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add compliance disclaimer to response.

        Ensures all outputs include legal positioning.
        """
        response["compliance_notice"] = (
            "IMPORTANT: This tool is for personal development, coaching, and "
            "wellness purposes only. It is NOT intended for hiring, promotion, "
            "performance evaluation, or any employment decisions. Results are "
            "meant to inspire self-awareness and facilitate coaching conversations."
        )
        return response
