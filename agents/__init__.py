from .agent_cliff import AgentCliff
from .agent_nevil import AgentNevil
from .base_agent import BaseAgent, AgentType

__all__ = ['AgentCliff', 'AgentNevil', 'BaseAgent', 'AgentType']

# Set default agent
DEFAULT_AGENT = AgentCliff 