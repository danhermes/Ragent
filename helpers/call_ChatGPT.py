from openai import OpenAI
import logging
from typing import List, Optional, Dict, Any, Tuple
import os
import time
from openai import RateLimitError
import httpx

logger = logging.getLogger(__name__)

class CallChatGPT:
    """Helper class for making ChatGPT API calls"""
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.org_id = os.getenv("OPENAI_ORG_ID")
        # Disable OpenAI's built-in retry mechanism
        self.client = OpenAI(api_key=self.api_key, max_retries=0)
    
    def get_response(self, model: str, messages: Optional[List[Dict[str, str]]] = None, max_retries: int = 3) -> str:
        """
        Make a call to ChatGPT with the specified model and messages.
        
        Args:
            model (str): The model to use (e.g., "o3-mini")
            messages (list): List of message dictionaries with 'role' and 'content'
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            str: The response content from ChatGPT
        """
        for attempt in range(max_retries):
            try:
                if not messages:
                    logger.error("No messages provided to ChatGPT")
                    return None
                    
                # Format messages for OpenAI API
                formatted_messages = []
                for msg in messages:
                    if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                        logger.error(f"Invalid message format: {msg}")
                        continue
                        
                    # If content is already a string, use it directly
                    if isinstance(msg["content"], str):
                        formatted_messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                        logger.info(f"CHATGPT PARSED Content:\n{msg['content']}")
                    # If content is a list, extract the text
                    elif isinstance(msg["content"], list):
                        text_content = ""
                        for content_item in msg["content"]:
                            if isinstance(content_item, dict) and "text" in content_item:
                                text_content += content_item["text"]
                            elif isinstance(content_item, str):
                                text_content += content_item
                        formatted_messages.append({
                            "role": msg["role"],
                            "content": text_content
                        })
                
                if not formatted_messages:
                    logger.error("No valid messages after formatting")
                    return None
                    
                response = self.call_chatgpt_with_continuity(model=model, messages=formatted_messages)
                
                if response and response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content
                else:
                    logger.error("No valid response content received")
                    return None
                    
            # except RateLimitError as e:
            #     logger.error(f"Rate limit error: {str(e)}")
            #     return None
            except Exception as e:
                logger.error(f"Error getting chat response: {str(e)}")
                return None 
            

    def call_chatgpt_with_continuity(self, model: str, messages: List[Dict[str, str]]):
        """A resilient GPT call that avoids token and request limit crashes."""
        while True:
            try:
                # Make the call
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages
                )

                # Check live token limits after success
                #headers = dict(response.response.headers)
                #remaining_tokens = int(headers.get("x-ratelimit-remaining-tokens", 0))
                #reset_time = headers.get("x-ratelimit-reset-tokens", "0s").replace("s", "")
                #reset_seconds = float(reset_time) if reset_time else 0

                # If buffer is low, wait it out
                #if remaining_tokens < 1000:
                #    print(f"🕒 Low token buffer ({remaining_tokens}). Waiting {reset_seconds:.1f}s for refill...")
                #    time.sleep(reset_seconds)

                return response

            # except self.client.error.RateLimitError as e:
            #     # Handle 429 with retry-after
            #     retry_after = e.headers.get("retry-after", "5")
            #     wait_time = int(float(retry_after))
            #     print(f"⚠️ Rate limit hit. Retrying in {wait_time} seconds...")
            #     time.sleep(wait_time)

            except Exception as e:
                print(f"❌ Unexpected GPT error: {e}. Retrying in 5s...")
                time.sleep(5)


    def get_openai_headers(self, model="gpt-3.5-turbo") -> Dict[str, str]:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "OpenAI-Organization": self.org_id
        }

        # This is a minimal payload that won't burn many tokens
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "ping"},
                {"role": "user", "content": "ping"}
            ],
            "max_tokens": 1,
            "stream": False
        }

        try:
            response = self.client.chat.completions.with_raw_response.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Hello, world!"}
                ],
                extra_headers={"X-Stainless-Raw-Response": "true"}
            )
            response.raise_for_status()  # Raises HTTPStatusError on 4xx/5xx

            # You got a good response
            result = response.json()
            logger.info(f"Response JSON: {result}")
            return result

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error: {e}")
            logger.error(f"Status Code: {e.response.status_code}")
            logger.error(f"Response Content: {e.response.text}")
            logger.error("Headers:")
            for k, v in e.response.headers.items():
                if 'ratelimit' in k.lower() or 'retry' in k.lower():
                    logger.error(f"{k}: {v}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error in OpenAI call: {e}")
            return None
