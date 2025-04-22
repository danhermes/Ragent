import argparse
import logging
import yaml
from pathlib import Path
from project_start import ProjectStart
from project_work import ProjectWork
from project_documents import ProjectDocuments
from typing import Optional
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/cli_{timestamp}.log"

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Remove any existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

logger.info("Logging system initialized")
logger.info(f"Session log file: {log_file}")

def load_project_types() -> dict:
    """Load project types from configuration"""
    try:
        # Get the directory where this module is located
        module_dir = Path(__file__).parent
        config_path = module_dir / "templates" / "project_types.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logging.error(f"Failed to load project types: {str(e)}")
        return {}

def find_goal_files(goal_file: str = None) -> list:
    """Find goal files either from command line or default directory"""
    if goal_file:
        # Use specified goal file
        goal_path = Path(goal_file)
        if not goal_path.exists():
            logging.error(f"Goal file not found: {goal_path}")
            return []
        return [goal_path]
    else:
        # Look in default directory
        module_dir = Path(__file__).parent
        goal_dir = module_dir / "goal"
        if not goal_dir.exists():
            logging.error(f"Goal directory not found: {goal_dir}")
            return []
        return list(goal_dir.glob("*.goal"))

def get_project_name_from_goal(goal_file: Path) -> str:
    """Extract project name from goal file name"""
    return goal_file.stem

def validate_project_type(project_type: str, project_types: dict) -> bool:
    """Validate that the project type is supported"""
    if project_type not in project_types['project_types']:
        logging.error(f"Invalid project type: {project_type}")
        valid_types = ", ".join(project_types['project_types'].keys())
        logging.error(f"Valid project types are: {valid_types}")
        return False
    return True

def run_project(project_name: str, project_type: str, project_types: dict, goals_file: Optional[str] = None) -> bool:
    """Run a complete project workflow"""
    try:
        logging.info(f"Starting project run. Name: {project_name}, Type: {project_type}, Goals file: {goals_file}")
        
        # Initialize project
        project = ProjectStart()
        if not project.initialize_project(project_name, project_type, goals_file):
            logging.error("Failed to initialize project")
            return False

        # Use the project type determined by ProjectStart
        project_type = project.project_type
        logging.info(f"Using project type: {project_type}")
        
        # Log goals state after initialization
        logging.info(f"Project goals after initialization: {project.goals}")
        if project.config:
            logging.info(f"Project config goals: {project.config.goals}")
        else:
            logging.warning("No project config available")

        # Validate project type
        if not validate_project_type(project_type, project_types):
            return False

        # Run all meetings
        logging.info("Creating ProjectWork instance with goals")
        work = ProjectWork(
            project.project_path, 
            project_type, 
            project.config.goals if project.config else None
        )
        logging.info(f"ProjectWork goals after initialization: {work.goals}")
        
        if not work.run_all_meetings():
            logging.error("Failed to run meetings")
            return False

        # Generate final document
        docs = ProjectDocuments()
        if not docs.load_document_config(project_type):
            logging.error("Failed to load document config")
            return False

        context = {
            'project_name': project_name,
            'goals': project.goals,
            'design_doc': docs.design_doc,
            'implementation_doc': docs.implementation_doc,
            'meeting_history': work.conversation_history
        }
        logging.info(f"Document generation context: {context}")

        doc = docs.generate_document('technical_design', context)
        if not doc:
            logging.error("Failed to generate technical design")
            return False

        if not docs.save_document('technical_design', doc, project.project_path):
            logging.error("Failed to save technical design")
            return False

        logging.info(f"Successfully completed project: {project_name}")
        return True

    except Exception as e:
        logging.error(f"Error running project: {str(e)}")
        return False

def main():
    # Load project types
    project_types = load_project_types()
    if not project_types:
        logging.error("Failed to load project types configuration")
        exit(1)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run a complete project workflow')
    parser.add_argument('--goal', help='Path to goal file')
    parser.add_argument('--type', help='Project type (default: code)')
    
    args = parser.parse_args()
    
    # Find goal files
    goal_files = find_goal_files(args.goal)
    if not goal_files:
        logging.error("No goal files found")
        exit(1)

    # Process each goal file
    for goal_file in goal_files:
        project_name = get_project_name_from_goal(goal_file)
        logging.info(f"Processing project from goal file: {project_name}")

        success = run_project(project_name, args.type, project_types, goal_file)
        
        if not success:
            logging.error(f"Failed to process project: {project_name}")
            continue

if __name__ == '__main__':
    main() 