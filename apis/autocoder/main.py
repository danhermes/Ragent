import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to Python path for proper imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

from apis.autocoder.agent.build_cycle_agent import AgentBuildCycle
from apis.autocoder.utils.logger import log

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

def read_spec_file(spec_path: str) -> str:
    """Read and parse the specification file
    
    Args:
        spec_path: Path to the .spec file
        
    Returns:
        str: The task specification
        
    Raises:
        FileNotFoundError: If spec file doesn't exist
        ValueError: If spec file is empty or invalid
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Reading spec file: {spec_path}")
    
    if not os.path.exists(spec_path):
        raise FileNotFoundError(f"Spec file not found: {spec_path}")
        
    with open(spec_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        
    if not content:
        raise ValueError("Spec file is empty")
        
    logger.info(f"Successfully read spec file. Content length: {len(content)}")
    return content

def main():
    """Main entry point for the autocoder"""
    logger = setup_logging()
    logger.info("Starting autocoder main process")
    
    try:
        # Get spec file path from environment or use default
        spec_path = os.getenv('AUTOCODER_SPEC', '.spec')
        logger.info(f"Using spec file: {spec_path}")
        
        # Read task from spec file
        task = read_spec_file(spec_path)
        logger.debug(f"Task defined: {task}")
        
        # Initialize build cycle
        logger.info("Initializing AgentBuildCycle")
        cycle = AgentBuildCycle(agent_task=task, max_iterations=3)
        logger.debug(f"Build cycle initialized with max_iterations={cycle.max_iterations}")
        
        # Run the cycle
        logger.info("Starting build cycle...")
        cycle.run_cycle()
        logger.info("Build cycle completed successfully")
        
    except FileNotFoundError as e:
        logger.error(f"Spec file error: {str(e)}")
        raise
    except ValueError as e:
        logger.error(f"Spec file content error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Autocoder main process finished")

if __name__ == "__main__":
    main()
