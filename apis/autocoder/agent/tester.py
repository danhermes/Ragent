import openai
from utils.file_ops import save_code, clean_code_block
import os
import logging
import json
from typing import Optional, Tuple, Dict, Any
from .runner_docker import run_code_in_docker
from . import debugger

# Suppress OpenAI client logging
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class Tester:
    """Handles code testing and validation"""
    
    def __init__(self, test_layer = None):
        """Initialize the tester"""
        self.test_layer = test_layer
        pass
        
    def generate_tests(self, code_path: str, error_msg: str = "") -> str:
        """Generate pytest test cases for the given code file.
        
        Args:
            code_path: Path to the Python file to generate tests for
            error_msg: Error message to include in the test code
            
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
    7. Use the exact function names from the code
    8. Use requests_mock for mocking HTTP requests
    9. Use proper list syntax for mock responses
    10. Always close all brackets and parentheses
    11. Use proper Python syntax for all data structures
    12. Use baseline test data from the BASELINE_DATA environment variable
    13. Parse baseline data with json.loads(os.environ['BASELINE_DATA'])
    14. Use baseline data for assertions and mock responses

    Here is the code to test:

    {code}

    Error message:
    {error_msg}
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
            "import json",
            "import os",
            "import requests_mock",
            "from temp_code import *",
            "",
            "# Load baseline test data",
            "baseline_data = json.loads(os.environ['BASELINE_DATA']) if 'BASELINE_DATA' in os.environ else {}",
            "",
            test_code
        ]
        test_code = "\n".join(import_lines)
        
        return test_code

    def generate_baseline_test_data(self, test_code: str) -> Dict[str, Any]:
        """Generate baseline test data for the given test code.
        
        Args:
            test_code: The test code to generate baseline data for
            
        Returns:
            Dict[str, Any]: Dictionary containing baseline test data
        """
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Python testing expert. Generate baseline test data for the given test cases."},
                {"role": "user", "content": f"""
    Please generate baseline test data for these test cases. The data should:
    1. Include realistic test values for each test case
    2. Include expected outputs/assertions
    3. Include mock responses where needed
    4. Be in a structured format that can be saved to a file
    5. Return ONLY the JSON data, no markdown, no explanations
    6. Use proper JSON syntax with all brackets and quotes closed

    Here are the test cases:

    {test_code}
    """}
            ],
            temperature=0.7
        )
        
        # Extract the JSON data from the response
        baseline_data = response.choices[0].message.content
        if "```json" in baseline_data:
            baseline_data = baseline_data.split("```json")[1].split("```")[0].strip()
        elif "```" in baseline_data:
            baseline_data = baseline_data.split("```")[1].strip()
        
        try:
            # Parse the JSON data
            data_dict = json.loads(baseline_data)
            
            # Save the baseline data to a file
            sandbox_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sandbox')
            os.makedirs(sandbox_dir, exist_ok=True)
            baseline_path = os.path.join(sandbox_dir, 'baseline_test_data.json')
            
            with open(baseline_path, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=2)
            
            logger.info(f"Baseline test data saved to {baseline_path}")
            return data_dict
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing baseline test data: {str(e)}")
            return {}

    def run_pytests(self, test_file: str) -> Tuple[bool, str, str]:
        """Run pytest on the given test file in Docker container with baseline data
        
        Args:
            test_file: Path to the test file
            
        Returns:
            Tuple[bool, str, str]: (test result, stdout, stderr)
        """
        try:
            # Load baseline data if it exists
            baseline_path = os.path.join(os.path.dirname(test_file), 'baseline_test_data.json')
            logger.info("baseline_path: %s", baseline_path)
            if os.path.exists(baseline_path):
                with open(baseline_path, 'r', encoding='utf-8') as f:
                    baseline_data = json.load(f)
                # Pass baseline data to Docker container
                env_var = f'BASELINE_DATA={json.dumps(baseline_data)}'
            else:
                env_var = None
            
            # Ensure test_file is a valid path
            if not os.path.exists(test_file):
                logger.error(f"Test file not found: {test_file}")
                return (False, "", f"Test file not found: {test_file}")
            
            # Get just the filename for Docker
            test_filename = os.path.basename(test_file)
            logger.info(f"Running test file: {test_filename}")
            
            # Run pytest in Docker container with baseline data
            stdout, stderr = run_code_in_docker(test_file, cleanup=True, env_var=env_var)
            
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

    # def validate_tests(self, test_code: str) -> Tuple[bool, str]:
    #     """Validate that the generated tests are syntactically correct and can run.
        
    #     Args:
    #         test_code: The test code to validate
            
    #     Returns:
    #         Tuple[bool, str]: (is_valid, error_message)
    #     """
    #     try:
    #         # Create a temporary test file with just the test code
    #         sandbox_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sandbox')
    #         os.makedirs(sandbox_dir, exist_ok=True)
    #         temp_test_path = os.path.join(sandbox_dir, 'temp_validate_test.py')
            
    #         with open(temp_test_path, 'w', encoding='utf-8') as f:
    #             f.write(test_code)
            
    #         # Try to run the tests with pytest
    #         stdout, stderr = run_code_in_docker(temp_test_path, cleanup=True)
            
    #         # Check if there are any syntax errors or import errors
    #         if "SyntaxError" in stderr or "ImportError" in stderr:
    #             return (False, stderr)
            
    #         # Even if tests fail, if they run without syntax errors, they're valid
    #         return (True, "")
            
    #     except Exception as e:
    #         return (False, str(e))

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
            
            # Generate tests to (below) combine with baseline test data and write it to a file in local /sandbox directory
            logger.info("Generating tests...")
            test_code = self.generate_tests(temp_code_path)
            
            # Generate baseline test data and write it to a file in local /sandbox directory
            logger.info("Generating baseline test data...")
            baseline_data = self.generate_baseline_test_data(test_code)
            
            # Update test code with baseline data
            if baseline_data:
                # Add baseline data import to test code
                import_lines = [
                    "import pytest",
                    "import json",
                    "import os",
                    "import requests_mock",
                    "from pathlib import Path",
                    "from temp_code import *",
                    "",
                    "# Load baseline test data",
                    "baseline_path = Path(__file__).parent / 'baseline_test_data.json'",
                    "with open(baseline_path, 'r', encoding='utf-8') as f:",
                    "    baseline_data = json.load(f)",
                    "",
                    test_code
                ]
                test_code = "\n".join(import_lines)
     
            # Copy test file to local sandbox
            logger.info("sandbox_dir: %s", sandbox_dir)
            sandbox_test_path = os.path.join(sandbox_dir, 'test_generated.py')   
            with open(sandbox_test_path, 'w', encoding='utf-8') as f:
                f.write(test_code)     
            
            # Run tests and get result
            success, stdout, stderr = self.run_pytests(sandbox_test_path)
            
            if success:
                logger.info("All tests passed")
                return True
            else:
                logger.error("Tests failed")
                logger.error(f"stdout: {stdout}")
                logger.error(f"stderr: {stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error in test manager: {str(e)}")
            return False
