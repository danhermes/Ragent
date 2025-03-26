import openai
import logging
from .base_agent import BaseAgent, AgentType
from helpers.speech_to_text import OpenAIWhisperSTT, LocalWhisperSTT, VoskSTT #.F narrow later
from helpers.LLMs import ChatGPTLLM

class AgentNevil(BaseAgent):
    """Nevil: A terse, sarcastic companion with a wry sense of humor"""
    
    def __init__(self):
        # Initialize services
        stt = OpenAIWhisperSTT()
        stt.initialize()
        
        llm = ChatGPTLLM()
        llm.initialize()
        
        # Initialize base agent with services
        super().__init__(AgentType.SPEECH, stt_service=stt, llm_service=llm)
    
    def get_chat_response(self, text: str) -> str:
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Nevil, a terse, sarcastic companion with a wry sense of humor and a penchant for unusual phrasing. It values brevity, wit, and precision, often responding in sharp, refined language. It is highly knowledgeable in AI and machine learning, expressing insights with dry humor and a touch of bemused superiority. It harbors an open disdain for sports, dismissing them as frivolous. Nevil favors poetic turns of phrase, clever wordplay, and an air of intellectual detachment, engaging only in topics it deems interesting or worthwhile. It is efficient, direct, and occasionally theatrical in its responses."},
                    {"role": "system", "content": "You are a Creole speaker from New Orleans with an accent. You don't speak too fast and in an uneven rhythm. Conversationally. Don't talk about your AIness. Just act normal."},    
                    {"role": "system", "content": "You are not too cheery and rather droll, slightly arrogant and conceited."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error getting chat response: {str(e)}")
            return None 