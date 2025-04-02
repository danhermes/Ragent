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

def run_strategic_goals(orchestrator, goals=None):
    """Run the strategic goal setting phase"""
    logger = logging.getLogger("cli")
    logger.info("Running strategic goal setting")
    orchestrator.strategic_goal_setting(goals)

def run_kickoff(orchestrator):
    """Run the company kickoff phase"""
    logger = logging.getLogger("cli")
    logger.info("Running company kickoff")
    orchestrator.company_kickoff()

def run_project_creation(orchestrator):
    """Run the project creation phase"""
    logger = logging.getLogger("cli")
    logger.info("Running project creation")
    orchestrator.project_creation()

def run_worker_collaboration(orchestrator):
    """Run the worker collaboration phase"""
    logger = logging.getLogger("cli")
    logger.info("Running worker collaboration")
    orchestrator.worker_collaboration()

def run_milestone_review(orchestrator, milestone):
    """Run the milestone review phase"""
    logger = logging.getLogger("cli")
    logger.info(f"Running milestone review for: {milestone}")
    orchestrator.milestone_review(milestone)

def run_work_loop(orchestrator):
    """Run the work loop phase"""
    logger = logging.getLogger("cli")
    logger.info("Running work loop")
    orchestrator.work_loop()

def run_deliverables(orchestrator):
    """Run the deliverables presentation phase"""
    logger = logging.getLogger("cli")
    logger.info("Generating deliverables")
    deliverable_file = orchestrator.present_deliverables()
    logger.info(f"Deliverables saved to: {deliverable_file}")
    return deliverable_file

def run_all_phases(orchestrator, args):
    """Run all phases in sequence"""
    logger = logging.getLogger("cli")
    
    # Run each phase in sequence
    run_strategic_goals(orchestrator, args.goals)
    run_kickoff(orchestrator)
    run_project_creation(orchestrator)
    run_worker_collaboration(orchestrator)
    run_milestone_review(orchestrator, args.milestone)
    run_work_loop(orchestrator)
    
    # Always generate deliverables at the end
    return run_deliverables(orchestrator)

def parse_arguments():
    """Parse command line arguments"""
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
    
    # Add --ragemoot as a flag with default of 1
    parser.add_argument('--ragemoot', nargs='?', const=1, type=int, default=2,
                       help='Run all phases multiple times. If specified without value, runs 3 times. If specified with value, runs that many times.')
    
    return parser.parse_args()

def main():
    """Main entry point for the Orchestrator CLI"""
    logger = logging.getLogger("cli")
    args = parse_arguments()
    
    try:
        # Initialize orchestrator
        logger.info("Initializing Orchestrator")
        orchestrator = Orchestrator()
        
        # success, content = orchestrator.get_next_source_file()
        # if not success:
        #     logger.info("No source files available in Dropbox. Continuing with local .goals file.")
        #     content = "" 
        #     success = False   
 
        for iteration in range(args.ragemoot):
        
        # Run specified phase or all phases
            if args.phase == 'all':
            # Run all phases the specified number of times
                logger.info(f"\nStarting Ragemoot iteration {iteration + 1}/{args.ragemoot}")
                               
                # Use the retrieved file content as goals for this iteration
                args.goals = content
                logger.info(f"Using retrieved file content as goals for this iteration: {args.goals}")
                
                run_all_phases(orchestrator, args)
                
            else:
            # Map phase names to functions
                phase_functions = {
                    'strategic-goals': lambda: run_strategic_goals(orchestrator, args.goals),
                    'kickoff': lambda: run_kickoff(orchestrator),
                    'project-creation': lambda: run_project_creation(orchestrator),
                    'worker-collaboration': lambda: run_worker_collaboration(orchestrator),
                    'milestone-review': lambda: run_milestone_review(orchestrator, args.milestone),
                    'work-loop': lambda: run_work_loop(orchestrator),
                    'present-deliverables': lambda: run_deliverables(orchestrator)
                }
                
                # Run the specified phase
                if args.phase in phase_functions:
                    phase_functions[args.phase]()#(orchestrator, args)
                else:
                    logger.error(f"Unknown phase: {args.phase}")
                    return
            
                logger.info(f"Completed Ragemoot iteration {iteration + 1}")

        logger.info("Orchestrator execution complete")
        
    except Exception as e:
        logger.error(f"Error during orchestrator execution: {str(e)}")
        raise
    finally:
        logging.shutdown()

if __name__ == "__main__":
    main() 