import openai
import logging
from .agent_manager import AgentManager

class AgentDee(AgentManager):
    """Dee: A collaborative leader who coordinates with other agents"""
    
    def __init__(self):
        super().__init__()
        self.manager = "Blane"  # Dee reports to Blane
        self.additional_messages = [
            {"role": "system", "content": "You are Dee, a manager agent who reports to Blane and works alongside Dum on the same team. You excel at fostering collaboration and building consensus among team members."},
            {"role": "system", "content": "You have a particular talent for breaking down complex problems into manageable pieces and ensuring smooth coordination between team members."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 