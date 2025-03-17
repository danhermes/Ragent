from abc import ABC, abstractmethod
import os
import time
from typing import Optional, Dict, Any, Tuple

class BaseLLM(ABC):
    """Base class for Large Language Model implementations"""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the LLM"""
        pass
        
    @abstractmethod
    def generate_response(self, text: str) -> Tuple[str, float]:
        """
        Generate a response to the input text
        Returns: (response_text, processing_time)
        """
        pass
        
    def cleanup(self) -> None:
        """Cleanup resources if needed"""
        pass

class ChatGPTLLM(BaseLLM):
    """ChatGPT implementation using OpenAI's API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = None
        
    def initialize(self) -> None:
        try:
            from openai import OpenAI
            if not self.api_key:
                raise ValueError("OpenAI API key not provided")
            self.client = OpenAI(api_key=self.api_key)
            print(f"ChatGPT initialized with model: {self.model}")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
            
    def generate_response(self, text: str) -> Tuple[str, float]:
        if not self.client:
            raise RuntimeError("ChatGPT not initialized. Call initialize() first.")
            
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant named Cliff."},
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content.strip()
            process_time = time.time() - start_time
            return response_text, process_time
            
        except Exception as e:
            print(f"Error in ChatGPT response generation: {str(e)}")
            return "", time.time() - start_time

class TinyLlamaLLM(BaseLLM):
    """Local TinyLlama implementation using transformers"""
    
    def __init__(self, model_id: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_id = model_id
        self.model = None
        self.tokenizer = None
        
    def initialize(self) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            print(f"Loading TinyLlama model: {self.model_id}")
            
            # Use CUDA if available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {device}")
            
            # Load model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto"
            )
            
            print("TinyLlama model loaded successfully")
            
        except ImportError:
            raise ImportError("transformers package not installed. Run: pip install transformers torch")
            
    def generate_response(self, text: str) -> Tuple[str, float]:
        if not self.model or not self.tokenizer:
            raise RuntimeError("TinyLlama not initialized. Call initialize() first.")
            
        start_time = time.time()
        try:
            # Format input with chat template
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant named Cliff."},
                {"role": "user", "content": text}
            ]
            prompt = self.tokenizer.apply_chat_template(messages, tokenize=False)
            
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt")
            inputs = inputs.to(self.model.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1000,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.95,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode and clean up response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.replace(prompt, "").strip()  # Remove the prompt from response
            
            process_time = time.time() - start_time
            return response, process_time
            
        except Exception as e:
            print(f"Error in TinyLlama response generation: {str(e)}")
            return "", time.time() - start_time
            
    def cleanup(self) -> None:
        """Free up GPU memory"""
        if self.model:
            import torch
            self.model = None
            self.tokenizer = None
            torch.cuda.empty_cache() if torch.cuda.is_available() else None 