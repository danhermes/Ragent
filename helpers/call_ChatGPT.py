import openai
import logging

logger = logging.getLogger(__name__)

class CallChatGPT:
    """Helper class for making ChatGPT API calls"""
    
    @staticmethod
    def get_response(model: str, messages: list) -> str:
        """
        Make a call to ChatGPT with the specified model and messages.
        
        Args:
            model (str): The model to use (e.g., "o3-mini")
            messages (list): List of message dictionaries with 'role' and 'content'
            
        Returns:
            str: The response content from ChatGPT
        """
        response = openai.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content 