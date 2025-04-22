import logging
from .base_agent import BaseAgent, AgentType
from helpers.call_ChatGPT import CallChatGPT

logger = logging.getLogger(__name__)

class AgentSupervisor(BaseAgent):
    """Base class for supervisor agents"""
    def __init__(self):
        super().__init__(AgentType.TEXT)
        self.base_messages = [
            {"role": "system", "content": "You are a supervisor agent responsible for high-level strategic planning and execution. You work with manager agents to set long-term objectives and ensure they align with overall goals. You focus on resource allocation, risk management, and maintaining strategic direction."},
            {"role": "system", "content": "Your management style is strategic and results-driven. You excel at identifying key stakeholders, setting clear objectives, and ensuring efficient execution of plans. You maintain a focus on long-term success while managing immediate challenges."},
            {"role": "system", "content": "When developing strategies, you will: 1) Identify strategic objectives 2) Analyze stakeholders and resources 3) Develop execution plans 4) Assess risks and mitigation strategies 5) Monitor progress and adjust as needed"},
            {"role": "system", "content": "Format your responses with clear sections: STRATEGIC OBJECTIVES, STAKEHOLDER ANALYSIS, EXECUTION PLAN, RISK MANAGEMENT, PROGRESS MONITORING"}
        ]

    def get_chat_response(self, text: str) -> str:
        try:
            # Combine base messages with any additional messages from the child class
            messages = self.base_messages + getattr(self, 'additional_messages', [])
            messages.append({"role": "user", "content": text})
            logging.debug(f"Base Agent sending messages to OpenAI: {messages}")
            
            return CallChatGPT.get_response("gpt-4o", messages)
            
        except Exception as e:
            logging.error(f"Error getting chat response: {str(e)}")
            return None 