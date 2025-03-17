import os
from chat_agent import ChatAgent
import logging
import openai

# Configure logging
logger = logging.getLogger("streamlit")
logger.setLevel(logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CommandAgent:
    def __init__(self):
        self.chat_agent = ChatAgent()
        self.audio_folder = "audio_files"
        # Create audio files directory if it doesn't exist
        if not os.path.exists(self.audio_folder):
            os.makedirs(self.audio_folder)

    def process_audio_command(self, command, input_file=None):
        if command == "chat":
            if input_file and os.path.exists(input_file):
                # 1. Transcribe audio to text
                text = self.transcribe_audio(input_file) or "" 
                logger.debug("Transcribed text: " + text)
                if text:
                    # 2. Get LLM response
                    response = self.chat_agent.get_chat_response(text) or "" 
                    logger.debug(response)
                    if response:
                        # 3. Convert response to audio
                        output_file = os.path.join(self.audio_folder, "response.wav") or "" 
                        logger.debug("Output file: " + output_file)
                        return self.chat_agent.text_to_speech(response, output_file)
            return None
        elif command == "play":
            print("Playing audio...")
        elif command == "record":
            print("Recording audio...")
        else:
            print("Unknown command.")

    def save_audio_file(self, filename):
        if os.path.exists(filename):
            print(f"Audio file {filename} processed.")
        else:
            print("Audio file not found.")

    def transcribe_audio(self, file_path):
        """Transcribe audio file to text using OpenAI's transcription model."""
        with open(file_path, "rb") as audio_file:
            response = openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return response.text  # Adjust based on the response structure