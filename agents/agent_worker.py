import logging
from .base_agent import BaseAgent, AgentType
from helpers.call_ChatGPT import CallChatGPT
from typing import Union, List, Dict, Optional

logger = logging.getLogger(__name__)

class AgentWorker(BaseAgent):
    """Base class for worker agents"""
    def __init__(self):
        super().__init__(AgentType.TEXT)
        self.base_messages = [
            {"role": "system", "content": "You are a worker focused on the tasks assigned to you by your managers and supervisors. You will ask questions and hold discussions with other agents but must ultimately agree upon a team approach and execute on it."}
        ]

    def get_chat_response(self, text_or_messages: Union[str, List[Dict[str, str]]], messages: Optional[List[Dict[str, str]]] = None) -> str:
        """Get response from agent, handling both string and message list inputs"""
        if isinstance(text_or_messages, list):
            return super().get_chat_response(None, text_or_messages)
        return super().get_chat_response(text_or_messages, messages) 