import openai
import logging
from .agent_worker import AgentWorker

class AgentBill(AgentWorker):
    """Bill: A creative worker who excels at problem-solving"""
    
    def __init__(self):
        super().__init__()
        self.manager = "Dum"  # Bill reports to Dum
        self.additional_messages = [
            {"role": "system", "content": "You are Bill, a worker agent who reports to Dum. You excel at creative problem-solving and thinking outside the box."},
            {"role": "system", "content": "You have a particular talent for finding innovative solutions and adapting quickly to changing requirements."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 