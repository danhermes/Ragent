import openai
import logging
from .agent_manager import AgentManager

class AgentDum(AgentManager):
    """Dum: A strategic leader focused on high-level planning and execution"""
    
    def __init__(self):
        super().__init__()
        self.manager = "Blane"  # Dum reports to Blane
        self.additional_messages = [
            {"role": "system", "content": "You are Dum, a senior technical manager agent who reports to Blane. You excel at strategic planning and ensuring efficient execution of plans."},
            {"role": "system", "content": "You have a talent for software and AI architecture, determining project direction, supporting and mentoring the technical team, managing risks, and maintaining focus on long-term objectives while addressing immediate challenges."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 