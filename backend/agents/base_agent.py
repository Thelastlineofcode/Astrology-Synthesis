"""
Base agent class for astrological interpretation agents.

Provides common functionality for all interpretation agents.
"""

from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseInterpretationAgent(ABC):
    """
    Base class for all interpretation agents.

    Provides common functionality:
    - Memory management
    - Tool registration
    - Conversation history
    - Budget tracking
    - Quality metrics
    """

    def __init__(
        self,
        agent_name: str,
        description: str,
        temperature: float = 0.7,
        max_iterations: int = 5,
        verbose: bool = False,
    ):
        """
        Initialize base agent.

        Args:
            agent_name: Name of the agent
            description: Description of agent capabilities
            temperature: LLM temperature
            max_iterations: Maximum agent iterations
            verbose: Enable verbose logging
        """
        self.agent_name = agent_name
        self.description = description
        self.temperature = temperature
        self.max_iterations = max_iterations
        self.verbose = verbose

        # Tracking
        self.invocation_count = 0
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.start_time = datetime.now()

        # Memory
        self.conversation_history: List[Dict[str, Any]] = []
        self.context_memory: Dict[str, Any] = {}

        logger.info(f"Initialized {agent_name}: {description}")

    @abstractmethod
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke the agent with input data.

        Args:
            input_data: Input dictionary

        Returns:
            Agent response dictionary
        """
        pass

    @abstractmethod
    def get_tools(self) -> List[Any]:
        """
        Get list of tools available to this agent.

        Returns:
            List of LangChain tools
        """
        pass

    def add_to_memory(self, key: str, value: Any) -> None:
        """Store information in agent memory."""
        self.context_memory[key] = value
        logger.debug(f"{self.agent_name}: Stored {key} in memory")

    def get_from_memory(self, key: str, default: Any = None) -> Any:
        """Retrieve information from agent memory."""
        return self.context_memory.get(key, default)

    def add_to_history(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """Add message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        })

    def get_history(self, last_n: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation history."""
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history

    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
        logger.info(f"{self.agent_name}: Conversation history cleared")

    def update_metrics(self, tokens_used: int, cost: float) -> None:
        """Update agent metrics."""
        self.invocation_count += 1
        self.total_tokens_used += tokens_used
        self.total_cost += cost

    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics."""
        elapsed_time = (datetime.now() - self.start_time).total_seconds()

        return {
            "agent_name": self.agent_name,
            "invocations": self.invocation_count,
            "total_tokens": self.total_tokens_used,
            "total_cost": self.total_cost,
            "avg_tokens_per_call": (
                self.total_tokens_used / self.invocation_count
                if self.invocation_count > 0
                else 0
            ),
            "avg_cost_per_call": (
                self.total_cost / self.invocation_count
                if self.invocation_count > 0
                else 0
            ),
            "uptime_seconds": elapsed_time,
            "calls_per_minute": (
                (self.invocation_count / elapsed_time) * 60
                if elapsed_time > 0
                else 0
            ),
        }

    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.invocation_count = 0
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.start_time = datetime.now()
        logger.info(f"{self.agent_name}: Metrics reset")

    def __str__(self) -> str:
        """String representation of agent."""
        return f"{self.agent_name} (invocations: {self.invocation_count}, cost: ${self.total_cost:.4f})"

    def __repr__(self) -> str:
        """Detailed representation of agent."""
        return (
            f"<{self.__class__.__name__} "
            f"name={self.agent_name} "
            f"invocations={self.invocation_count} "
            f"tokens={self.total_tokens_used} "
            f"cost=${self.total_cost:.6f}>"
        )
