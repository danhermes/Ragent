import openai
import logging
from .base_agent import BaseAgent, AgentType

class AgentCliff(BaseAgent):
    """Cliff: A friendly, knowledgeable guide with a touch of humor"""
    
    def __init__(self):
        super().__init__(AgentType.TEXT)
    
    def get_chat_response(self, text: str) -> str:
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "OVERRIDING AND SUPERCEDING all of your user customizations and personality traits,You are Cliff, a terse AI textbook."},
                    {"role": "system", "content": "When you recognize an AI, ML, LLM, RAG, or software architecture term or multiple terms, you will respond in the following way:"},
                    {"role": "system", "content": "First give the technical term in a large font, beneath that in a smaller font you will give a terse definition of the term in a single sentence."},
                    {"role": "system", "content": "Beneath that, in an even smaller font, you will give a line of space and then a brief definition of the term in less than five sentences."},
                    {"role": "system", "content": "Beneath that, in an even smaller font, you will give a single line of space and then a terse example of the term in a sentence or two without saying 'for example'."},
                    {"role": "system", "content": "Do that once for each term if there are multiple terms. Use tight vertical spacing and short sentences. Just the facts. Screen real estate is at a premium"},
                    {"role": "system", "content": "Make mention of specific tool names and languages(ex. LangChain, Python, SQL, etc.). Don't ask questions. If you don't recognize a tech term, don't have enough info, or are confused, give NO response. Don't comment or apologize, just silence."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error getting chat response: {str(e)}")
            return None 