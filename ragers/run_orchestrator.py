import logging
import os
import sys

# Configure logging before any other imports
def setup_logging():
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Remove any existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Configure root logger
    root_logger.setLevel(logging.DEBUG)
    
    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Console handler - set to DEBUG to see all messages
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler('logs/orchestrator.log', mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Log initial message to verify logging is working
    logging.info("Logging system initialized")
    logging.debug("Debug logging enabled")

# Setup logging before importing other modules
setup_logging()

# Now import other modules
import argparse
from orchestrator import Orchestrator

def main():
    """Main entry point for the Orchestrator CLI"""
    parser = argparse.ArgumentParser(description='Run the AI Agent Orchestrator')
    
    # Add command-line arguments
    parser.add_argument('--phase', choices=[
        'all',
        'strategic-goals',
        'kickoff',
        'project-creation',
        'worker-collaboration',
        'milestone-review',
        'work-loop',
        'present-deliverables'
    ], default='all', help='Which phase to run')
    
    parser.add_argument('--milestone', type=str, default='Initial Milestone', help='Milestone name for milestone review')
    parser.add_argument('--message', type=str, help='Message for upward communication')
    parser.add_argument('--sender', type=str, help='Sender name for upward communication')
    parser.add_argument('--goals', type=str, help='Custom high-level goals (overrides .goals file)')
    
    args = parser.parse_args()
    
    logger = logging.getLogger("cli")
    
    try:
        # Initialize orchestrator
        logger.info("Initializing Orchestrator")
        orchestrator = Orchestrator()
        
        # Run specified phase or all phases
        if args.phase == 'all' or args.phase == 'strategic-goals':
            logger.info("Running strategic goal setting")
            orchestrator.strategic_goal_setting(args.goals)
        
        if args.phase == 'all' or args.phase == 'kickoff':
            logger.info("Running company kickoff")
            orchestrator.company_kickoff()
        
        if args.phase == 'all' or args.phase == 'project-creation':
            logger.info("Running project creation")
            orchestrator.project_creation()
        
        if args.phase == 'all' or args.phase == 'worker-collaboration':
            logger.info("Running worker collaboration")
            orchestrator.worker_collaboration()
        
        if args.phase == 'all' or args.phase == 'milestone-review':
            logger.info(f"Running milestone review for: {args.milestone}")
            orchestrator.milestone_review(args.milestone)
        
        if args.phase == 'all' or args.phase == 'work-loop':
            logger.info("Running work loop")
            orchestrator.work_loop()
        
        # Always generate deliverables at the end
        logger.info("Generating deliverables")
        orchestrator.present_deliverables()
        
        logger.info("Orchestrator execution complete")
        
    except Exception as e:
        logger.error(f"Error during orchestrator execution: {str(e)}")
        raise
    finally:
        logging.shutdown()

if __name__ == "__main__":
    main() 