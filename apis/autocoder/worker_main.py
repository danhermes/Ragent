import logging
import os
from datetime import datetime
from agent.worker_agent import WorkerAgent

def setup_logging():
    """Set up logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create a timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/worker_{timestamp}.log"
    
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

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("Starting worker process")
    
    try:
        # Initialize worker agent
        agent_name = "Agent_Worker_001"
        logger.info(f"Initializing worker agent: {agent_name}")
        agent = WorkerAgent(name=agent_name)
        logger.debug(f"Worker agent initialized with name: {agent.name}")
        
        # Define and run task
        task = (
            "Write a Python script that fetches current weather data for a list of cities "
            "using a public weather API and stores the results in a JSON file."
        )
        logger.debug(f"Task defined: {task}")
        
        logger.info("Starting task execution")
        agent.run_task(task)
        logger.info("Task execution completed successfully")
        
    except Exception as e:
        logger.error(f"Error in worker process: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Worker process finished")
