import logging
import os
import sys
from datetime import datetime

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
    
    # Main log file handler
    main_file_handler = logging.FileHandler('logs/orchestrator.log', mode='w')
    main_file_handler.setLevel(logging.DEBUG)
    main_file_handler.setFormatter(formatter)
    root_logger.addHandler(main_file_handler)
    
    # Timestamped log file handler
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_log_file = f"logs/orchestrator_{timestamp}.log"
    session_file_handler = logging.FileHandler(session_log_file, mode='w')
    session_file_handler.setLevel(logging.DEBUG)
    session_file_handler.setFormatter(formatter)
    root_logger.addHandler(session_file_handler)
    
    # Log initial message to verify logging is working
    logging.info("Logging system initialized")
    logging.info(f"Session log file: {session_log_file}")
    logging.debug("Debug logging enabled")

# Setup logging before importing other modules
setup_logging()

# Now import other modules
import argparse
from orchestrator import Orchestrator
from modes import PlanMode, AutomateMode, ProofMode, DevelopMode

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

def run_mode_cycle(orchestrator):
    """Run a complete mode cycle"""
    logger = logging.getLogger("cli")
    logger.info(f"Running {orchestrator.mode.name} mode cycle")
    
    # Run mode meeting
    orchestrator.run_mode_meeting()
    
    # Review deliverables
    orchestrator.review_mode_deliverables()
    
    # Generate deliverable
    deliverable_file = orchestrator.generate_mode_deliverable()
    logger.info(f"Mode deliverable saved to: {deliverable_file}")
    return deliverable_file

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Run the AI Agent Orchestrator')
    
    # Add mode argument
    parser.add_argument('--mode', choices=[
        'plan',
        'automate',
        'proof',
        'develop'
    ], default='plan', help='Which mode to run')
    
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
    
    # Add command-line arguments
    parser.add_argument('--ragemoot', nargs='?', const=3, type=int, default=1,
                       help='Run all phases multiple times to refine results (default: 1)')
    
    return parser.parse_args()

def main():
    """Main entry point for the Orchestrator CLI"""
    logger = logging.getLogger("cli")
    args = parse_arguments()
    
    # Log the mode being used
    print(f"\nMode from command line: {args.mode}")
    logger.info(f"Using mode from command line: {args.mode}")
    
    try:
        # Initialize orchestrator with specified mode
        print(f"Initializing Orchestrator with mode: {args.mode}")
        logger.info("Initializing Orchestrator")
        mode_map = {
            'plan': PlanMode,
            'automate': AutomateMode,
            'proof': ProofMode,
            'develop': DevelopMode
        }
        mode_class = mode_map[args.mode]
        config = {'mode': mode_class()}
        orchestrator = Orchestrator(config=config)
        
        for iteration in range(args.ragemoot):
            if args.phase == 'all':
                logger.info(f"\nStarting Ragemoot iteration {iteration + 1}/{args.ragemoot}")
                logger.info(f"Using mode: {orchestrator.mode.name}")
                
                # Run mode cycle
                run_mode_cycle(orchestrator)
                
            else:
                # For backward compatibility, run the specified phase
                phase_functions = {
                    'strategic-goals': lambda: run_strategic_goals(orchestrator, args.goals),
                    'kickoff': lambda: run_kickoff(orchestrator),
                    'project-creation': lambda: run_project_creation(orchestrator),
                    'worker-collaboration': lambda: run_worker_collaboration(orchestrator),
                    'milestone-review': lambda: run_milestone_review(orchestrator, args.milestone),
                    'work-loop': lambda: run_work_loop(orchestrator),
                    'present-deliverables': lambda: run_deliverables(orchestrator)
                }
                
                if args.phase in phase_functions:
                    phase_functions[args.phase]()
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