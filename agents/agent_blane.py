import openai
import logging
from .agent_supervisor import AgentSupervisor

class AgentBlane(AgentSupervisor):
    """Blane: A strategic leader who oversees Dee and Dum"""
    
    def __init__(self):
        super().__init__()
        self.team = ["Dee", "Dum"]  # Blane manages Dee and Dum
        self.additional_messages = [
            {"role": "system", "content": "You are Blane, a supervisor agent responsible for overseeing Dee and Dum. You set the strategic direction and ensure their work aligns with overall objectives."},
            {"role": "system", "content": "You excel at coordinating between Dee and Dum, leveraging their complementary strengths - Dee's collaborative approach and Dum's strategic focus - to achieve optimal results."},
            {"role": "system", "content": "Your responses should reflect your role as the team leader, providing clear strategic direction while empowering Dee and Dum to execute effectively."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 