import openai
import logging
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class AgentType(Enum):
    TEXT = "text"
    CODE = "code"

class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def transcribe_audio(self, file_path):
        """Transcribe audio file to text using OpenAI's Whisper model."""
        with open(file_path, "rb") as audio_file:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": "Please transcribe this audio."}
                ],
                audio=audio_file
            )
        return response['choices'][0]['message']['content']

    def text_to_speech(self, text: str, output_file: str) -> str:
        """Convert text to speech using OpenAI's TTS"""
        if self.agent_type == AgentType.TEXT:
            return text
            
        try:
            response = openai.audio.speech.create(
                model="tts-1",
                voice="ash",
                input=text
            )
            
            # Save the audio response
            with open(output_file, 'wb') as f:
                response.stream_to_file(output_file)
            
            return output_file
        except Exception as e:
            logging.error(f"Error converting text to speech: {str(e)}")
            return None

    def get_chat_response(self, text: str) -> str:
        """Get a response from the agent"""
        # For testing, return a simple response based on the agent type
        if self.agent_type == AgentType.TEXT:
            return f"I am {self.__class__.__name__} and I received your message: {text}"
        else:
            return f"Code agent {self.__class__.__name__} received: {text}" 