import os
import sys
import logging
import os
from datetime import datetime
import openai
from typing import Optional
import time

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from utils.file_ops import save_code, clean_code_block
from agent.prompts import RolePrompt, VALID_ROLES, get_code_generation_prompt
from config import OPENAI_API_KEY

class CodeWriter:
    """Handles code file operations"""
    
    def __init__(self, role: str = "python_dev", test_layer=None):
        self.logger = logging.getLogger(__name__)
        """Initialize the code writer       
        Args:
            role: The role to use for code generation. Must be one of: python_dev, n8n_dev, writer, proofreader, dev_writer
            test_layer: Optional test layer for testing
        """
        if role not in VALID_ROLES:
            raise ValueError(f"Invalid role: {role}. Must be one of: {', '.join(VALID_ROLES)}")
            
        self.role = role
        self.test_layer = test_layer
        self.logger.debug("Initializing CodeWriter")
        self.output_dir = "generated_code"
        os.makedirs(self.output_dir, exist_ok=True)
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.logger.debug(f"[CodeWriter] Initializing role: {self.role}")
        self._roleprompt = RolePrompt.get_instance(self.role, test_layer=self.test_layer)
        self.logger.info(f"CodeWriter initialized with role: {role}")

    def _is_content_generation_task(self, task: str) -> bool:
        """Determine if the task is about content generation
        
        Args:
            task: The task description
            
        Returns:
            bool: True if this is a content generation task
        """
        content_keywords = ["book", "chapter", "story", "narrative", "content", "write", "author"]
        task_lower = task.lower()
        return any(keyword in task_lower for keyword in content_keywords)

    def save_code(self, code: str) -> str:
        """Save the generated code to a file
        
        Args:
            code: Code to save
            
        Returns:
            str: Path to the saved file
        """
        self.logger.info("Saving generated code")
        self.logger.debug(f"Code length: {len(code)}")
    
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_code_{timestamp}.py"
            filepath = os.path.join(self.output_dir, filename)
            
            self.logger.debug(f"Saving code to: {filepath}")
            
            # Save the code
            with open(filepath, "w") as f:
                f.write(code)
            
            self.logger.info(f"Code saved successfully to {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error saving code: {str(e)}", exc_info=True)
            raise

    def _call_openai_api(self, prompt: str, max_retries: int = 3, retry_delay: int = 1) -> Optional[str]:
        """Call OpenAI API to generate code or content with retry logic
        
        Args:
            prompt: The prompt to send to OpenAI
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            
        Returns:
            Optional[str]: The generated content or None if all retries fail
            
        Raises:
            Exception: If all retry attempts fail
        """
        self.logger.debug(f"Calling OpenAI API with role: {self._roleprompt.name}")
        
        for attempt in range(max_retries):
            try:
                # Call OpenAI API with role-specific parameters
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": self._roleprompt.system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self._roleprompt.temperature,
                    max_tokens=self._roleprompt.max_tokens
                )
                
                # Extract the generated content
                content = response.choices[0].message.content
                self.logger.debug(f"Generated content length: {len(content)}")
                
                return content
                
            except openai.RateLimitError as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"Rate limit hit, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    self.logger.error("Rate limit error after all retries", exc_info=True)
                    raise
                    
            except openai.APIError as e:
                if attempt < max_retries - 1:
                    self.logger.warning(f"API error, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    self.logger.error("API error after all retries", exc_info=True)
                    raise
                    
            except Exception as e:
                self.logger.error(f"Unexpected error calling OpenAI API: {str(e)}", exc_info=True)
                raise

    def generate_code(self, task: str) -> str:
        """Generate code or content using OpenAI API
        
        Args:
            task: Description of the task
            
        Returns:
            str: Generated code or content
            
        Raises:
            Exception: If content generation fails
        """
        self.logger.info(f"Generating content for task: {task}")
        try:
            # Generate the prompt
            prompt = get_code_generation_prompt(task, self.test_layer)
            self.logger.debug(f"Generated prompt length: {len(prompt)}")
            
            # Call OpenAI API with role-specific parameters
            content = self._call_openai_api(prompt)
            if content is None:
                raise Exception("Failed to generate content after all retries")
                
            content = clean_code_block(content)
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating content: {str(e)}", exc_info=True)
            raise
