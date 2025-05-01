# from ..Cliff.agent_cliff import AgentCliff
# from .agent_nevil import AgentNevil
# from .base_agent import BaseAgent, AgentType

# __all__ = ['AgentCliff', 'AgentNevil', 'BaseAgent', 'AgentType']

# # Set default agent
# DEFAULT_AGENT = AgentCliff 

from .agent_blane import AgentBlane
from .agent_dum import AgentDum
from .agent_woz import AgentWoz
from .base_agent import BaseAgent, AgentType

__all__ = ['AgentBlane', 'AgentDum', 'AgentWoz', 'BaseAgent', 'AgentType'] 