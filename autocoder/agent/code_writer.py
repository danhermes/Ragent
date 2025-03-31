import logging
import os
from datetime import datetime
import openai
from utils.file_ops import save_code, clean_code_block
from .prompts import get_code_generation_prompt

logger = logging.getLogger(__name__)

class CodeWriter:
    """Handles code file operations"""
    
    def __init__(self):
        """Initialize the code writer"""
        logger.debug("Initializing CodeWriter")
        self.output_dir = "generated_code"
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info("CodeWriter initialized")

    def save_code(self, code: str) -> str:
        """Save the generated code to a file
        
        Args:
            code: Code to save
            
        Returns:
            str: Path to the saved file
        """
        logger.info("Saving generated code")
        logger.debug(f"Code length: {len(code)}")
    
        #    file_path = save_code(code, "autocoder_agent/generated_code/autocodefile1.py")
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_code_{timestamp}.py"
            filepath = os.path.join(self.output_dir, filename)
            
            logger.debug(f"Saving code to: {filepath}")
            
            # Save the code
            with open(filepath, "w") as f: # Todo: Use save_code function
                f.write(code)
            
            logger.info(f"Code saved successfully to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving code: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def _call_openai_api(prompt: str) -> str:
        """Call OpenAI API to generate code
        
        Args:
            prompt: The prompt to send to OpenAI
            
        Returns:
            str: The generated code
            
        Raises:
            Exception: If the API call fails
        """
        logger.debug("Calling OpenAI API")
        
        try:
            # Create the client
            client = openai.OpenAI()
            
            # Call OpenAI API with new format
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert Python programmer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the generated code
            code = response.choices[0].message.content
            logger.debug(f"Generated code length: {len(code)}")
            
            return code
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def generate_code(task_description: str) -> str:
        """Generate code using OpenAI API
        
        Args:
            task_description: Description of the task
            
        Returns:
            str: Generated code
        """
        logger.info(f"Generating code for task: {task_description}")
        
        try:
            # Generate the prompt
            prompt = get_code_generation_prompt(task_description)
            logger.debug(f"Generated prompt length: {len(prompt)}")
            
            # Call OpenAI API
            code = CodeWriter._call_openai_api(prompt)
            code = clean_code_block(code)
            
            return code
            
        except Exception as e:
            logger.error(f"Error generating code: {str(e)}", exc_info=True)
            raise
