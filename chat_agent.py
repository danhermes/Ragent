import openai
from pathlib import Path
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class ChatAgent:
        
    def transcribe_audio(self, file_path):
        """Transcribe audio file to text using OpenAI's Whisper model."""
        with open(file_path, "rb") as audio_file:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Specify the model you want to use
                messages=[
                    {"role": "user", "content": "Please transcribe this audio."}
                ],
                audio=audio_file  # Use the audio parameter for the file
            )
        return response['choices'][0]['message']['content']  # Adjust based on the response structure

    def get_chat_response(self, text: str) -> str:
        """Get response from ChatGPT using the new OpenAI API format"""
        """.F Create local LLM to reduce latency........................."""
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

    def text_to_speech(self, text: str, output_file: str) -> str:
        """Convert text to speech using OpenAI's TTS"""
        """.F Try ElevenLabs API .........................................."""
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