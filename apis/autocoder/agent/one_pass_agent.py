import logging
from typing import Optional
from .code_writer import CodeWriter
#from .prompts import get_code_generation_prompt

logger = logging.getLogger(__name__)

class OnePassAgent:
    """Agent responsible for generating code based on tasks"""
    
    def __init__(self, name: str):
        """Initialize the worker agent
        
        Args:
            name: Name of the agent
        """
        logger.debug(f"Initializing WorkerAgent: {name}")
        self.name = name
        logger.info(f"WorkerAgent {name} initialized")
    
    def run_task(self, task: str) -> Optional[str]:
        """Run the given task and generate code
        
        Args:
            task: Task description
            
        Returns:
            Optional[str]: Generated code if successful, None otherwise
        """
        logger.info(f"WorkerAgent {self.name} starting task: {task}")
        
        try:           
            logger.debug("Generating  code")
            code = CodeWriter.generate_code(task)
            logger.debug(f"Generated code length: {len(code)}")
                     
            return code
            
        except Exception as e:
            logger.error(f"Error in task execution: {str(e)}", exc_info=True)
            return None
        finally:
            logger.info(f"WorkerAgent {self.name} completed task")
