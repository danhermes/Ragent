import openai
from utils.file_ops import save_code, clean_code_block
import os
import logging
from typing import Optional, Tuple
from .runner_docker import run_code_in_docker
from . import debugger

# Suppress OpenAI client logging
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class Tester:
    """Handles code testing and validation"""
    
    def __init__(self):
        """Initialize the tester"""
        pass
        
    def generate_tests(self, code_path: str) -> str:
        """Generate pytest test cases for the given code file.
        
        Args:
            code_path: Path to the Python file to generate tests for
            
        Returns:
            str: Generated test code as a string
        """
        with open(code_path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Python testing expert. Generate pytest test cases for the given code."},
                {"role": "user", "content": f"""
    Please generate pytest test cases for this code. The test file should:
    1. Include test cases for success and error scenarios
    2. Test edge cases and invalid inputs
    3. Use descriptive test names
    4. Include docstrings explaining what each test verifies
    5. Return ONLY the test code, no markdown, no explanations
    6. DO NOT include any import statements - they will be added automatically
    7. Use the exact function names from the code (fetch_weather_data, fetch_weather_data_for_cities, save_weather_data_to_json)
    8. Use requests_mock for mocking HTTP requests
    9. Use proper list syntax for mock responses, e.g. mock_responses = [{{"weather": [{{"main": "Clear"}}]}}, {{"weather": [{{"main": "Clouds"}}]}}]  # Note the closing bracket
    10. Always close all brackets and parentheses
    11. Use proper Python syntax for all data structures

    Here is the code to test:

    {code}
    """}
            ],
            temperature=0.7
        )
        
        test_code = response.choices[0].message.content
        
        # Extract just the Python code if it's wrapped in markdown code blocks
        if "```python" in test_code:
            test_code = test_code.split("```python")[1].split("```")[0].strip()
        elif "```" in test_code:
            test_code = test_code.split("```")[1].strip()
        
        # Remove any existing import statements
        lines = test_code.split('\n')
        test_code = '\n'.join(line for line in lines if not line.startswith('import ') and not line.startswith('from '))
        
        # Replace _main_() with main() in the test code
        test_code = test_code.replace('_main_()', 'main()')
        
        # Add import statements at the top
        import_lines = [
            "import pytest",
            "from requests_mock import Mocker",
            "from temp_code import *",
            "",
            test_code
        ]
        test_code = "\n".join(import_lines)
        
        return test_code

    def run_pytests(self, test_file: str) -> Tuple[bool, str, str]:
        """Run pytest on the given test file in Docker container
        Args:
            test_file: Path to the test file
        Returns:
            bool: True if tests pass, False otherwise
        """
        try:
            # Run pytest in Docker container
            stdout, stderr = run_code_in_docker(test_file, cleanup=True)
            
            # Log the test output
            logger.info("Test output:")
            logger.info(stdout)
            if stderr:
                logger.error("Test errors:")
                logger.error(stderr)
            
            # Check for test results in the output
            if "[100%]" in stdout and "FAILED" not in stdout and "ERROR" not in stdout:
                return (True, stdout, stderr)
            else:
                return (False, stdout, stderr)
                
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}")
            return (False, "", str(e))

    def test_manager(self, code: str) -> bool:
        """Run tests for the generated code in Docker container with debugging support
        
        Args:
            code: Code string to test
            
        Returns:
            bool: True if tests pass, False otherwise
        """
        try:
            # Create sandbox directory in the autocoder directory
            sandbox_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sandbox')
            os.makedirs(sandbox_dir, exist_ok=True)
            
            # Save code to temp file in sandbox
            temp_code_path = os.path.join(sandbox_dir, 'temp_code.py')
            with open(temp_code_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Generate tests
            logger.info("Generating tests...")
            test_code = self.generate_tests(temp_code_path)
            
            # Copy test file to sandbox
            sandbox_test_path = os.path.join(sandbox_dir, 'test_generated.py')
            with open(sandbox_test_path, 'w', encoding='utf-8') as f:
                f.write(test_code)
            
            # Run tests with up to 3 debugging iterations
            current_code_path = temp_code_path
            for iteration in range(4):  # 0-based: 0, 1, 2, 3
                logger.info(f"Running tests (attempt {iteration + 1} of 4)...")
                test_result, stdout, stderr = self.run_pytests(sandbox_test_path)
                if not test_result:
                    logger.error(f"Tests failed on attempt {iteration + 1} of 4")
                    if iteration < 3:  # Don't debug on last iteration (when iteration is 3)
                        logger.info("Attempting to debug and fix code...")
                        current_code_path = debugger.revise_code_with_error_context(current_code_path, stderr)
                        # Update the test file to import from the revised code
                        with open(sandbox_test_path, 'r', encoding='utf-8') as f:
                            test_content = f.read()
                        test_content = test_content.replace('from temp_code import *', f'from {os.path.splitext(os.path.basename(current_code_path))[0]} import *')
                        with open(sandbox_test_path, 'w', encoding='utf-8') as f:
                            f.write(test_content)
                else:
                    logger.info("Tests passed")
                    return True
            
            logger.error("All debugging attempts failed")
            return False
            
        except Exception as e:
            logger.error(f"Error during testing: {str(e)}")
            return False
