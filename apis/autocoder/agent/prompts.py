import logging

logger = logging.getLogger(__name__)

def get_code_generation_prompt(task: str) -> str:
    """Generate a prompt for code generation based on the task
    
    Args:
        task: The task description
        
    Returns:
        str: The generated prompt
    """
    logger.debug(f"Generating prompt for task: {task}")
    
    prompt = f"""
You are an expert Python programmer. Your task is to write code that:
{task}

IMPORTANT: The code MUST be structured in a testable way following these rules:
1. Break down functionality into pure functions with clear inputs and outputs
2. Each function should have a single responsibility
3. Functions should return values rather than just printing or modifying global state
4. Use type hints for all function parameters and return values
5. Add docstrings to all functions explaining their purpose, parameters, and return values
6. Handle errors by returning None or raising exceptions rather than printing errors
7. Keep the main execution logic in an if __name__ == '__main__' block
8. Make functions accept parameters rather than using hardcoded values
9. Avoid global variables - pass data between functions as parameters
10. Make the code modular and reusable
11. Add _main_ function to the code to execute the methods in the order they are defined.

Please provide:
1. A complete, well-documented Python script following the testable structure rules above
2. Include all necessary imports
3. Add proper error handling with returns/exceptions
4. Include docstrings for all functions
5. Follow PEP 8 style guidelines
6. Omit commentary on the code, just write runnable code. No commentary before or after the code, either. No run instructions.
7. Strip first and last lines of code if they are just ```python and ```.
8. Code must be immediately runnable, without additional action required from the developer or user. 
9. If services are required, they must be free and require neither API keys nor user input, and must be readily available to anyone without a login or account.

Example structure:
def function_name(param1: str, param2: int) -> Optional[Dict]:
    '''Function description
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
    '''
    try:
        # Function logic here
        return result
    except Exception as e:
        return None

if __name__ == '__main__':
    # Main execution logic here
    result = function_name("test", 123)
"""
    
    logger.debug(f"Generated prompt length: {len(prompt)}")
    return prompt

