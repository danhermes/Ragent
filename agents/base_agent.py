import openai
import logging
from enum import Enum
from helpers.speech_to_text import SpeechToText
from helpers.LLMs import BaseLLM
import re
from typing import Dict, List, Optional

# Configure logging
logger = logging.getLogger("streamlit")
logger.setLevel(logging.DEBUG)

class AgentType(Enum):
    TEXT = "text"
    CODE = "code"

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_type: AgentType, stt_service: SpeechToText = None, llm_service: BaseLLM = None):
        self.agent_type = agent_type
        self.stt_service = stt_service
        self.llm_service = llm_service
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def transcribe_audio(self, audio_file: str) -> Optional[str]:
        """Transcribe audio file using configured STT service"""
        try:
            if not self.stt_service:
                logger.error("No STT service configured")
                return None
                
            # Transcribe audio
            text, _ = self.stt_service.transcribe(audio_file)  # Ignore processing time
            
            # Clean up transcription
            if text:
                # Remove extra spaces
                text = re.sub(r'\s+', ' ', text)
                # Fix spacing after punctuation
                text = re.sub(r'([.,!?])([^\s])', r'\1 \2', text)
                # Ensure proper spacing between words
                text = re.sub(r'\s+', ' ', text)
                text = text.strip()
                
            return text
            
        except Exception as e:
            logger.error(f"Error in audio transcription: {str(e)}")
            return None

    # def text_to_speech(self, text: str, output_file: str) -> str:
    #     """Convert text to speech using OpenAI's TTS"""
    #     if self.agent_type == AgentType.TEXT:
    #         return text
            
    #     try:
    #         response = openai.audio.speech.create(
    #             model="tts-1",
    #             voice="ash",
    #             input=text
    #         )
            
    #         # Save the audio response
    #         with open(output_file, 'wb') as f:
    #             response.stream_to_file(output_file)
            
    #         return output_file
    #     except Exception as e:
    #         logging.error(f"Error converting text to speech: {str(e)}")
    #         return None

    def get_chat_response(self, text: str, messages: Optional[List[Dict[str, str]]] = None, file_path: Optional[str] = None) -> str:
        """Get response from configured LLM service"""
        if not self.llm_service:
            raise ValueError("LLM service not configured")
        response, _ = self.llm_service.generate_response(text, messages, file_path)
        return response 
        """Get a response from the agent"""
        # For testing, return a simple response based on the agent type
        if self.agent_type == AgentType.TEXT:
            return f"I am {self.__class__.__name__} and I received your message: {text}"
        else:
            return f"Code agent {self.__class__.__name__} received: {text}" 