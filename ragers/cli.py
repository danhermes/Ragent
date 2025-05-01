import argparse
import logging
import yaml
from pathlib import Path
from typing import Optional
import os
from datetime import datetime
from main import ProjectMain

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

def load_project_types() -> dict:
    """Load project types from configuration"""
    try:
        module_dir = Path(__file__).parent
        config_path = module_dir / "templates" / "project_types.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Failed to load project types: {str(e)}")
        return {}

def find_goal_files(goal_file: str = None) -> list:
    """Find goal files either from command line or default directory"""
    if goal_file:
        goal_path = Path(goal_file)
        if not goal_path.exists():
            logger.error(f"Goal file not found: {goal_path}")
            return []
        return [goal_path]
    else:
        module_dir = Path(__file__).parent
        goal_dir = module_dir / "goal"
        if not goal_dir.exists():
            logger.error(f"Goal directory not found: {goal_dir}")
            return []
        return list(goal_dir.glob("*.goal"))

def get_project_name_from_goal(goal_file: Path) -> str:
    """Extract project name from goal file name"""
    return goal_file.stem

def validate_project_type(project_type: str, project_types: dict) -> bool:
    """Validate that the project type is supported"""
    if project_type not in project_types['project_types']:
        logger.error(f"Invalid project type: {project_type}")
        valid_types = ", ".join(project_types['project_types'].keys())
        logger.error(f"Valid project types are: {valid_types}")
        return False
    return True

def main():
    # Load project types
    project_types = load_project_types()
    if not project_types:
        logger.error("Failed to load project types configuration")
        exit(1)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run a complete project workflow')
    parser.add_argument('--goal', help='Path to goal file')
    parser.add_argument('--type', help='Project type (default: code)')
    
    args = parser.parse_args()
    
    # Find goal files
    goal_files = find_goal_files(args.goal)
    if not goal_files:
        logger.error("No goal files found")
        exit(1)

    # Create project main instance
    project_main = ProjectMain()

    # Process each goal file
    for goal_file in goal_files:
        project_name = get_project_name_from_goal(goal_file)
        logger.info(f"Processing project from goal file: {project_name}")

        success = project_main.run_project(project_name, args.type, project_types, goal_file)
        
        if not success:
            logger.error(f"Failed to process project: {project_name}")
            continue

if __name__ == '__main__':
    main() 