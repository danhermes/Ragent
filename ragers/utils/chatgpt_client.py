import os
import logging
import json
import requests
from typing import List, Dict, Any, Optional

class ChatGPTClient:
    """Simple ChatGPT API client that doesn't depend on audio functionality"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            self.logger.warning("OPENAI_API_KEY not found in environment variables")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4"  # Default model
        
    def set_model(self, model: str):
        """Set the model to use for completions"""
        self.model = model
        
    def get_chat_response(self, messages: List[Dict[str, str]]) -> str:
        """Get a response from ChatGPT API
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
                     Example: [{"role": "system", "content": "You are a helpful assistant"},
                               {"role": "user", "content": "Hello, world!"}]
        
        Returns:
            The response content as a string
        """
        if not self.api_key:
            self.logger.error("Cannot call ChatGPT API: No API key provided")
            return "Error: No API key provided"
            
        # Ensure messages is in the correct format
        if isinstance(messages, str):
            # If a string is provided, convert it to a proper message format
            messages = [{"role": "user", "content": messages}]
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                data=json.dumps(data)
            )
            response.raise_for_status()
            
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"].strip()
            else:
                self.logger.error(f"Unexpected API response format: {response_data}")
                return "Error: Unexpected API response format"
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return f"Error: API request failed - {str(e)}"
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse API response: {str(e)}")
            return f"Error: Failed to parse API response - {str(e)}"
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return f"Error: Unexpected error - {str(e)}"