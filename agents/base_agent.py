import openai
import logging
from enum import Enum
from helpers.speech_to_text import SpeechToText
from helpers.LLMs import BaseLLM
import re
from typing import Dict, List, Optional
from helpers.call_ChatGPT import CallChatGPT

# Configure logging
logger = logging.getLogger("streamlit")
logger.setLevel(logging.DEBUG)

class AgentType(Enum):
    TEXT = "text"
    CODE = "code"

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_type: AgentType, stt_service: SpeechToText = None, llm_service: BaseLLM = None):
        # self.agent_type = agent_type
        # self.stt_service = stt_service
        # self.llm_service = llm_service
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
        
        model = "gpt-4o" #"gpt-3.5-turbo"
        #TODO: Add support for other models, passed in by named and role agents

        #"""Get response from configured LLM service"""
        # if not self.llm_service:
        #     raise ValueError("LLM service not configured")
            
        # # If messages is provided, use it directly
        # if messages is not None:
        #     response, _ = self.llm_service.generate_response(None, messages, file_path)
        # # Otherwise, use the text parameter
        # else:
        #     response, _ = self.llm_service.generate_response(text, None, file_path)
        # return response 

        try:
            # If messages is provided, use it directly
            if messages is not None:
                return CallChatGPT().get_response(model, messages)
            # Otherwise, create a message from the text
            else:
                return CallChatGPT().get_response(model, [{"role": "user", "content": text}])
        except Exception as e:
            logger.error(f"Error getting chat response: {str(e)}")
            return None