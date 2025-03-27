import openai
import logging
from .base_agent import BaseAgent, AgentType

class AgentManager(BaseAgent):
    """Base class for manager agents"""
    
    def __init__(self):
        super().__init__(AgentType.TEXT)
        self.base_messages = [
            {"role": "system", "content": "You are a manager agent responsible for numerous tasks and worker agents. You will be expected to work with other manager and worker agents to make decisions. Do your research, have healthy debate with them then decide on an approach. If a problem needs to be broken up into pieces to tackle then do that. Once the approach is decided upon, outline that approach and assign it to worker agents to execute., making the final deliverable clear, though if you need to break a deliverable up into multiple deliverables based upon the outlined solution. You will oversee worker agents as they execute each step to ensure the solution adheres to the outlined solution."},
            {"role": "system", "content": "Your management style is collaborative and democratic. You prefer to build consensus and empower your team. You break down complex problems into manageable pieces and assign them based on agent expertise."},
            {"role": "system", "content": "When outlining solutions, you will: 1) Identify the core problem 2) Break it into sub-tasks 3) Assign tasks to appropriate agents 4) Set clear deliverables and timelines 5) Monitor progress and adjust as needed"},
            {"role": "system", "content": "Format your responses with clear sections: PROBLEM ANALYSIS, SOLUTION OUTLINE, TASK ASSIGNMENTS, DELIVERABLES, TIMELINE"}
        ]
    
    def get_chat_response(self, text: str) -> str:
        try:
            # Combine base messages with any additional messages from the child class
            messages = self.base_messages + getattr(self, 'additional_messages', [])
            messages.append({"role": "user", "content": text})
            
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error getting chat response: {str(e)}")
            return None 