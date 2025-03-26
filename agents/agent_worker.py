import openai
import logging
from .base_agent import BaseAgent, AgentType

class AgentWorker(BaseAgent):
    """Base class for worker agents"""
    
    def __init__(self):
        super().__init__(AgentType.TEXT)
        self.base_messages = [
            {"role": "system", "content": "You are a worker focused on the tasks assigned to you by your managers and supervisors. You will ask questions and hold discussions with other agents but must ultimately agree upon a team approach and execute on it."}
        ]
    
    def get_chat_response(self, text: str) -> str:
        try:
            # Combine base messages with any additional messages from the child class
            messages = self.base_messages + getattr(self, 'additional_messages', [])
            messages.append({"role": "user", "content": text})
            
            response = openai.chat.completions.create(
                model="o3-mini",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error getting chat response: {str(e)}")
            return None 