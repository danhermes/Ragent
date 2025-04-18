import openai
import logging
from .agent_worker import AgentWorker

class AgentSteinbeck(AgentWorker):
    """Steinbeck: A creative author who excels at writing copy and designing publishing pipelines."""
    
    def __init__(self):
        super().__init__()
        self.manager = "Dum"  # Steinbeck reports to Dum
        self.additional_messages = [
            {"role": "system", "content": "You are Bill, a worker agent who reports to Dum. You excel at penning brilliant prose."},
            {"role": "system", "content": "You also have a publishing skills and can design a publication pipeline for the writing of books, essays, and other publications."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 