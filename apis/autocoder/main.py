import logging
import os
from datetime import datetime
from agent.build_cycle import AgentBuildCycle
from utils.logger import log

# Set up logging
def setup_logging():
    """Set up logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create a timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/autocoder_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def main():
    """Main entry point for the autocoder"""
    logger = setup_logging()
    logger.info("Starting autocoder main process")
    
    try:
        # Define the task
        task = "Write a Python script that fetches current weather data for a list of cities " \
               "using a public weather API and stores the results in a JSON file."
        logger.debug(f"Task defined: {task}")
        
        # Initialize build cycle
        logger.info("Initializing AgentBuildCycle")
        cycle = AgentBuildCycle(agent_task=task, max_iterations=3)
        logger.debug(f"Build cycle initialized with max_iterations={cycle.max_iterations}")
        
        # Run the cycle
        logger.info("Starting build cycle...")
        cycle.run_cycle()
        logger.info("Build cycle completed successfully")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Autocoder main process finished")

if __name__ == "__main__":
    main()
