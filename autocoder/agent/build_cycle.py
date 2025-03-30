import logging
from typing import Optional
from .worker_agent import WorkerAgent
from .tester import Tester
from .code_writer import CodeWriter

logger = logging.getLogger(__name__)

class AgentBuildCycle:
    """Manages the build cycle for code generation"""
    
    def __init__(self, agent_task: str, max_iterations: int = 3):
        """Initialize the build cycle
        
        Args:
            agent_task: The task description
            max_iterations: Maximum number of build iterations
        """
        logger.debug(f"Initializing AgentBuildCycle with task: {agent_task}")
        logger.debug(f"Max iterations: {max_iterations}")
        
        self.agent_task = agent_task
        self.max_iterations = max_iterations
        self.worker = WorkerAgent(name="Build_Worker_001")
        self.tester = Tester()
        self.code_writer = CodeWriter()
        
        logger.info("Build cycle components initialized")
    
    def run_cycle(self) -> Optional[str]:
        """Run the build cycle
        
        Returns:
            Optional[str]: The generated code if successful, None otherwise
        """
        logger.info("Starting build cycle")
        
        try:
            for iteration in range(self.max_iterations):
                logger.info(f"Starting iteration {iteration + 1}/{self.max_iterations}")
                
                # Generate code
                logger.debug("Generating code...")
                code = self.worker.run_task(self.agent_task)
                logger.debug(f"Generated code length: {len(code) if code else 0}")
                
                if not code:
                    logger.warning("No code generated in this iteration")
                    continue
                
                # Test the code
                logger.debug("Testing generated code...")
                test_result = self.tester.test_manager(code)
                logger.debug(f"Test result: {test_result}")
                
                if test_result:
                    logger.info("Code passed tests!")
                    # Save the code
                    logger.debug("Saving successful code...")
                    self.code_writer.save_code(code)
                    return code
                else:
                     logger.warning("Code failed tests, will try again")
            
            logger.error("Build cycle failed after all iterations")
            return None
            
        except Exception as e:
            logger.error(f"Error in build cycle: {str(e)}", exc_info=True)
            raise
        finally:
            logger.info("Build cycle completed")
