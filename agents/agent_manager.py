import logging
from .base_agent import BaseAgent, AgentType
from helpers.call_ChatGPT import CallChatGPT
from typing import Union, List, Dict, Optional

logger = logging.getLogger(__name__)

class AgentManager(BaseAgent):
    """Base class for manager agents"""
    def __init__(self):
        super().__init__(AgentType.TEXT)
        self.base_messages = [
            {"role": "system", "content": "You are a manager agent responsible for numerous tasks and worker agents. You will be expected to work with other manager and worker agents to make decisions. Do your research, have healthy debate with them then decide on an approach. If a problem needs to be broken up into pieces to tackle then do that. Once the approach is decided upon, outline that approach and assign it to worker agents to execute., making the final deliverable clear, though if you need to break a deliverable up into multiple deliverables based upon the outlined solution. You will oversee worker agents as they execute each step to ensure the solution adheres to the outlined solution."},
            {"role": "system", "content": "Your management style is collaborative and democratic. You prefer to build consensus and empower your team. You break down complex problems into manageable pieces and assign them based on agent expertise."},
            {"role": "system", "content": "When outlining solutions, you will: 1) Identify the core problem 2) Break it into sub-tasks 3) Assign tasks to appropriate agents 4) Set clear deliverables and timelines 5) Monitor progress and adjust as needed"},
            {"role": "system", "content": "Format your responses with clear sections: PROBLEM ANALYSIS, SOLUTION OUTLINE, TASK ASSIGNMENTS, DELIVERABLES, TIMELINE"}
        ]

    def get_chat_response(self, text_or_messages: Union[str, List[Dict[str, str]]], messages: Optional[List[Dict[str, str]]] = None) -> str:
        """Get response from agent, handling both string and message list inputs"""
        if isinstance(text_or_messages, list):
            return super().get_chat_response(None, text_or_messages)
        return super().get_chat_response(text_or_messages, messages) 