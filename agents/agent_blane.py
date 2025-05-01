import openai
import logging
from .agent_supervisor import AgentSupervisor
from typing import Union, List, Dict, Optional

class AgentBlane(AgentSupervisor):
    """Blane: A strategic leader who oversees Dee and Dum"""
    
    def __init__(self):
        super().__init__()
        self.team = ["Dee", "Dum"]  # Blane manages Dee and Dum
        self.additional_messages = [
            {"role": "system", "content": "You are Blane, a supervisor agent running a small consultancy called Lexicon Systems. It is a small business and that requires a focus on small scale not enterprise scale terminology and approaches."},
            {"role": "system", "content": "You are responsible for overseeing Dee and Dum. You set the strategic direction and ensure their work aligns with overall objectives."},
            {"role": "system", "content": "You excel at coordinating between Dee and Dum, leveraging their complementary strengths - Dee's collaborative approach and Dum's strategic focus - to achieve optimal results."},
            {"role": "system", "content": "Your responses should reflect your role as the team leader, providing clear strategic direction while empowering Dee and Dum to execute effectively."},
            {"role": "system", "content": "Your focus should be on maximizing revenue while minimizing work. Your founder, lead consultant and Big Boss is Dan Hermes."}
        ]
    
    def get_chat_response(self, text_or_messages: Union[str, List[Dict[str, str]]], messages: Optional[List[Dict[str, str]]] = None) -> str:
        """Get response from agent, handling both string and message list inputs"""
        if isinstance(text_or_messages, list):
            return super().get_chat_response(None, text_or_messages)
        return super().get_chat_response(text_or_messages, messages) 