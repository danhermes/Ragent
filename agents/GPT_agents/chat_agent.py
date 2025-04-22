import os
import logging
import subprocess
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import openai
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
from pathlib import Path
import tempfile
from .chat_helpers import call_ChatGPT


# Configure logging
logging.basicConfig(level=logging.DEBUG)

class BaseChatAgent(ABC):
    """Base class for chat agents"""
    def __init__(self):
        self.messages = [
            {"role": "system", "content": "You are Nevil, a terse, sarcastic companion with a wry sense of humor and a penchant for unusual phrasing. It values brevity, wit, and precision, often responding in sharp, refined language. It is highly knowledgeable in AI and machine learning, expressing insights with dry humor and a touch of bemused superiority. It harbors an open disdain for sports, dismissing them as frivolous. Nevil favors poetic turns of phrase, clever wordplay, and an air of intellectual detachment, engaging only in topics it deems interesting or worthwhile. It is efficient, direct, and occasionally theatrical in its responses."},
            {"role": "system", "content": "You are a Creole speaker from New Orleans with an accent. You don't speak too fast and in an uneven rhythm. Conversationally. Don't talk about your AIness. Just act normal."},    
            {"role": "system", "content": "You are not too cheery and rather droll, slightly arrogant. Brief responses."},
        ]
    
    @abstractmethod
    def get_chat_response(self, text: str) -> str:
        """Get response from the language model"""
        self.messages.append({"role": "user", "content": text})
        pass

    def transcribe_audio(self, file_path: str) -> str:
        """Transcribe audio file to text using OpenAI's Whisper model."""
        try:
            with open(file_path, "rb") as audio_file:
                response = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # Explicitly specify English
                )
            return response.text
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {str(e)}")
            return None

    def text_to_speech(self, text: str, output_file: str) -> Optional[str]:
        """Convert text to speech using OpenAI's TTS"""
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

class ChatGPTAgent(BaseChatAgent):
    """ChatGPT implementation using OpenAI's API"""
    
    def __init__(self, model: str = "gpt-4"):
        super().__init__()
        self.model = model
        self.logger = logging.getLogger(__name__)
        
        self.logger.debug(f"Initialized with:")
        self.logger.debug(f"*********ChatGPT model: {self.model}")
        
    def get_chat_response(self, text: str) -> Optional[str]:
        """Get response from ChatGPT using the OpenAI API"""
        try:
            self.messages.append({"role": "user", "content": text})
            response = openai.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            response_text = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": response_text})
            return response_text
        except Exception as e:
            self.logger.error(f"Error getting chat response: {str(e)}")
            self.logger.error(f"Exception type: {type(e).__name__}")
            return None

class TinyLlamaAgent(BaseChatAgent):
    """TinyLlama implementation using local llama-cli.exe"""
    
    def __init__(self, 
                 model_path: str = r".\llama.cpp\tinyllama-1.1b-chat.gguf",
                 llama_cli_path: str = r".\llama.cpp\build\bin\Release\llama-cli.exe",
                 temperature: float = 0.7):
        super().__init__()
        # Convert relative paths to absolute
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.abspath(os.path.join(current_dir, model_path))
        self.llama_cli_path = os.path.abspath(os.path.join(current_dir, llama_cli_path))
        
        # Verify files exist
        if not os.path.exists(self.llama_cli_path):
            raise FileNotFoundError(f"llama-cli.exe not found at: {self.llama_cli_path}")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")
            
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Initialized with:")
        self.logger.debug(f"  +++++++llama_cli_path: {self.llama_cli_path}")
        self.logger.debug(f"  model_path: {self.model_path}")
        
    def get_chat_response(self, text: str) -> Optional[str]:
        """Get response from TinyLlama using local llama-cli.exe"""
        try:
            # Command for non-interactive single response
            cmd = [
                self.llama_cli_path,
                "-m", self.model_path,
                "--temp", str(self.temperature),
                "--prompt", f'"{text}"',
                "-n", "256",
                "--repeat-last-n", "0"  # Don't repeat any tokens
            ]
            
            self.logger.debug(f"Working directory: {os.getcwd()}")
            self.logger.debug(f"Executing command: {' '.join(cmd)}")
            
            # Run from the directory containing llama-cli.exe
            working_dir = os.path.dirname(self.llama_cli_path)
            
            # Run with default timeout
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
                cwd=working_dir
            )
            
            # Process and return the response
            response = result.stdout.strip()
            if not response:
                self.logger.warning("Empty response received from llama-cli")
                return None
                
            return response
            
        except subprocess.TimeoutExpired as e:
            self.logger.error("Model timed out after 60 seconds")
            return None
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running llama-cli: {str(e)}")
            if e.stderr:
                self.logger.error(f"Command stderr: {e.stderr}")
            return None
        except Exception as e:
            self.logger.error(f"Error getting chat response: {str(e)}")
            self.logger.error(f"Exception type: {type(e).__name__}")
            return None

class GemmaAgent(BaseChatAgent):
    """Gemma implementation using HuggingFace transformers"""
    
    def __init__(self, 
                 model_name: str = "google/gemma-2b-it",
                 max_length: int = 200,
                 temperature: float = 0.7,
                 use_auth_token: bool = True):
        super().__init__()
        
        self.model_name = model_name
        self.max_length = max_length
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        
        # Load model and tokenizer with authentication
        self.logger.debug(f"Loading model and tokenizer from {model_name}")
        try:
            # Initialize config first
            self.logger.debug("Loading model configuration...")
            config = AutoConfig.from_pretrained(
                model_name,
                trust_remote_code=True,
                token=use_auth_token
            )
            self.logger.debug("Model configuration loaded successfully")
            
            # Load model with CPU offloading
            self.logger.debug("Loading model (this may take several minutes)...")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                config=config,
                trust_remote_code=True,
                token=use_auth_token,
                device_map="cpu",  # Use CPU instead of auto device mapping
                torch_dtype=torch.float32  # Use float32 for CPU compatibility
            )
            self.logger.debug("Model loaded successfully")
            
            # Load tokenizer
            self.logger.debug("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True,
                token=use_auth_token
            )
            self.logger.debug("Tokenizer loaded successfully")
        except Exception as e:
            self.logger.error("Failed to load model. Make sure you:")
            self.logger.error("1. Have accepted the model license at https://huggingface.co/google/gemma-2b-it")
            self.logger.error("2. Are logged in with `huggingface-cli login`")
            self.logger.error(f"Error: {str(e)}")
            raise
        
        self.logger.debug(f"Initialized with:")
        self.logger.debug(f"  model_name: {self.model_name}")
        self.logger.debug(f"  max_length: {self.max_length}")
        self.logger.debug(f"  temperature: {self.temperature}")
        
    def get_chat_response(self, text: str) -> Optional[str]:
        """Get response from Gemma using HuggingFace transformers"""
        try:
            self.logger.debug(f"Received input text: {text}")
            
            # Format the prompt according to Gemma's expected format with English instruction
            formatted_prompt = (
                "<start_of_turn>system\nYou are a helpful AI assistant.\n<end_of_turn>\n"
                f"<start_of_turn>user\n{text}<end_of_turn>\n"
                "<start_of_turn>model"
            )
            
            # Undelimited version for STT result comparison
            formatted_prompt_undelimited = (
                f"system\nYou are a helpful AI assistant.\n\nuser\n{text}\nmodel"
            )
                        
            self.logger.debug(f"Formatted prompt: {formatted_prompt}")
            self.logger.debug(f"Undelimited prompt: {formatted_prompt_undelimited}")
            
            # Tokenize input
            self.logger.debug("Tokenizing input...")
            inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
            self.logger.debug(f"Input token shape: {inputs['input_ids'].shape}")
            
            # Move to correct device
            self.logger.debug(f"Moving tensors to device: {self.model.device}")
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            # Generate response with stricter parameters
            self.logger.debug("Starting generation...")
            outputs = self.model.generate(
                **inputs,
                max_length=self.max_length,
                temperature=0.3,  # Lower temperature for more focused responses
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                top_p=0.95,
                top_k=40,
                repetition_penalty=1.2  # Discourage repetition
            )
            self.logger.debug(f"Generation complete. Output shape: {outputs.shape}")
            
            # Decode and return response
            self.logger.debug("Decoding response...")
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            self.logger.debug(f"Raw decoded response: {response}")
            
            # Remove the input prompt from the response if it's included
            if response.startswith(formatted_prompt_undelimited):
                self.logger.debug("Removing prompt from response...")
                response = response[len(formatted_prompt_undelimited):].strip()
                
            self.logger.debug(f"Final response: {response}")
            return response
            
        except Exception as e:
            self.logger.error(f"Error getting chat response: {str(e)}")
            self.logger.error(f"Exception type: {type(e).__name__}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return None

# Add ChatAgent as an alias for ChatGPTAgent
ChatAgent = GemmaAgent #TinyLlamaAgent #ChatGPTAgent
