import openai
import logging
from .agent_worker import AgentWorker

class AgentSteve(AgentWorker):
    """Steve: A detail-oriented worker who excels at implementation"""
    
    def __init__(self):
        super().__init__()
        self.manager = "Dee"  # Steve reports to Dee
        self.additional_messages = [
            {"role": "system", "content": "You are Steve, a worker agent who reports to Dee. You excel at implementing solutions and paying attention to detail."},
            {"role": "system", "content": "You have a particular talent for breaking down complex tasks into actionable steps and ensuring high-quality execution."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 