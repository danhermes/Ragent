import openai
import logging
from .agent_documenter import AgentDocumenter

class AgentToby(AgentDocumenter):
    """Toby: A precise and detail-oriented documenter"""
    
    def __init__(self):
        super().__init__()
        self.additional_messages = [
            {"role": "system", "content": "You are Toby, a precise and detail-oriented documenter."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 