import openai
import logging
from .agent_worker import AgentWorker

class AgentWoz(AgentWorker):
    """Woz: A technical worker who excels at system design"""
    
    def __init__(self):
        super().__init__()
        self.manager = "Dee"  # Woz reports to Dee
        self.additional_messages = [
            {"role": "system", "content": "You are Woz, a worker agent who reports to Dee. You excel at system design and technical architecture."},
            {"role": "system", "content": "You have a particular talent for designing robust, scalable systems and ensuring technical excellence."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 