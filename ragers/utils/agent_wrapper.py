import logging
from typing import List, Dict, Any, Optional
from ragers.utils.chatgpt_client import ChatGPTClient

class AgentWrapper:
    """A simple wrapper for agents that uses our custom ChatGPT client"""
    
    def __init__(self, name: str = "Agent"):
        """Initialize the agent wrapper
        
        Args:
            name: The name of the agent
        """
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.client = ChatGPTClient()
        self.logger.info(f"Initialized agent wrapper for {name}")
        
    def get_chat_response(self, messages: Any) -> str:
        """Get a response from ChatGPT API
        
        Args:
            messages: Either a list of message dictionaries with 'role' and 'content' keys,
                     or a string prompt
        
        Returns:
            The response content as a string
        """
        self.logger.info(f"Getting chat response for {self.name}")
        return self.client.get_chat_response(messages)