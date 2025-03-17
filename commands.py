import os
import logging
from agents import DEFAULT_AGENT
from agents.base_agent import AgentType

# Configure logging
logger = logging.getLogger("streamlit")
logger.setLevel(logging.DEBUG)
# Add console handler if not already present
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(console_handler)

class CommandAgent:
    def __init__(self, agent=None):
        self.agent = agent if agent else DEFAULT_AGENT()
        self.audio_folder = "audio_files"
        # Create audio files directory if it doesn't exist
        if not os.path.exists(self.audio_folder):
            os.makedirs(self.audio_folder)

    def process_text_command(self, command, text):
        """Process a text command and return the response"""
        if command == "chat" and text:
            # Get ChatGPT response
            response = self.agent.get_chat_response(text)
            if response:
                if self.agent.agent_type == AgentType.TEXT:
                    return response
                else:
                    # Convert response to audio for speech agents
                    output_file = os.path.join(self.audio_folder, "response.wav")
                    return self.agent.text_to_speech(response, output_file)
        return None