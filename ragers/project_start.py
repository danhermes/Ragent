import os
import sys
import yaml
import logging
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from utils.document_manager import DocumentManager

@dataclass
class ProjectConfig:
    """Project configuration loaded from YAML"""
    project_type: str #not in the config file
    templates: Dict[str, Any]
    phases: List[str]
    required_roles: List[str]
    project_structure: Dict[str, Any]
    input_files: List[str]
    output_files: List[str]
    #completion_criteria: List[str]
    #meeting_rules: Dict[str, Any]
    goals: List[str]

class ProjectStart:
    """Handles project initialization and configuration loading"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config: Optional[ProjectConfig] = None
        self.goals: str = ""
        self.templates: Dict[str, str] = {}
        self.project_structure: Dict[str, Any] = {}
        self.project_path: Optional[Path] = None
        self.project_type: Optional[str] = None
        self.config_file: Optional[str] = None
        
    def determine_project_type(self, project_type: Optional[str], goals_file: Optional[str] = None) -> str:
        """Determine project type based on priority order:
        1. Constructor argument
        2. Command line argument
        3. .goals file Project Type
        4. Default "code"
        """
        self.logger.info(f"Determining project type. Input project_type: {project_type}, goals_file: {goals_file}")
        
        # 1. Constructor argument
        if project_type:
            self.logger.info(f"Using constructor argument project type: {project_type}")
            return project_type.lower()
            
        # 2. Command line argument is passed in as project_type parameter
        
        # 3. .goals file Project Type
        if goals_file:
            self.logger.info(f"Attempting to read project type from goals file: {goals_file}")
            try:
                with open(goals_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    #self.logger.debug(f"Goals file content: {content[:200]}...")  # Log first 200 chars
                    
                    # Look for Project Type section
                    if "## 🔧 Project Type" in content:
                        # Extract the type from the line after the header
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if "## 🔧 Project Type" in line and i + 1 < len(lines):
                                type_line = lines[i + 1].strip()
                                # Extract type from backticks or plain text
                                if '`' in type_line:
                                    project_type = type_line.strip('`').lower()
                                else:
                                    project_type = type_line.lower()
                                self.logger.info(f"Found project type in goals file: {project_type}")
                                return project_type
                    else:
                        self.logger.warning("Project Type section not found in goals file")
            except Exception as e:
                self.logger.error(f"Failed to read project type from goals file: {str(e)}")
                
        # 4. Default "code"
        self.logger.info("Using default project type: code")
        return "code"
        
    def load_project_config(self) -> bool:
        """Load project configuration from config file"""
        try:
            if not self.project_type:
                self.logger.error("Project type not set")
                return False
                
            # Set config file path based on project type
            module_dir = Path(__file__).parent
            self.config_file = str(module_dir / "templates" / self.project_type / f"{self.project_type}_mode.yaml")
            
            if not os.path.exists(self.config_file):
                self.logger.warning(f"Config file not found: {self.config_file}")
                return False
                
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # Validate required top-level fields
            top_level_fields = ['templates', 'phases', 'required_roles', 'project_structure']
            for field in top_level_fields:
                if field not in config:
                    self.logger.error(f"Missing top-level field: {field}")
                    return False

            # Validate nested meeting fields (e.g., for 'strategy')
            strategy = config.get('templates', {}).get('meetings', {}).get('strategy', {})
            meeting_fields = ['input_files', 'output_files']
            for field in meeting_fields:
                if field not in strategy:
                    self.logger.error(f"Missing meeting field in 'strategy': {field}")
                    return False

            # Create strongly typed config
            self.config = ProjectConfig(
                project_type=self.project_type,
                templates=config['templates'],
                phases=config['phases'],
                required_roles=config['required_roles'],
                project_structure=config['project_structure'],
                input_files=strategy['input_files'],
                output_files=strategy['output_files'],
                goals=[]
            )
            
            #self.logger.info(f"Loaded project configuration from {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load project configuration: {str(e)}")
            return False

    def load_goals(self, goals_file: Optional[str] = None) -> bool:
        """Load project goals from file"""
        try:
            self.logger.info(f"Loading goals from file: {goals_file}")
            if goals_file:
                with open(goals_file, 'r', encoding='utf-8') as f:
                    goals_content = f.read().strip()
                    # Split goals into a list and filter out template content and separators
                    goals_list = [
                        goal.strip() 
                        for goal in re.split(r'[\n;]', goals_content) 
                        if goal.strip() 
                        and not goal.startswith('#')  # Filter out headers
                        and not goal.startswith('**')  # Filter out markdown bold
                        and not goal.startswith('`')   # Filter out code blocks
                        and not goal.startswith('---') # Filter out separators
                        and not goal.startswith('Template File:')  # Filter out template info
                    ]
                    self.goals = goals_list
                    self.logger.info(f"Loaded {len(goals_list)} goals")
                    
                # Store goals in config as a list
                if self.config:
                    self.config.goals = goals_list
                    self.logger.info("Stored goals in project configuration")
                    
                # Write goals to project goals directory
                if self.project_path:
                    goal_path = self.project_path / "goals" / "goals.md"
                    goal_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(goal_path, 'w', encoding='utf-8') as f:
                        f.write("# Project Goals\n\n")
                        for goal in goals_list:
                            f.write(f"{goal}\n\n")
                    #self.logger.info(f"Wrote goals to {goal_path}")
                    
                self._log_goal(goals_content)
                self.logger.info("Successfully loaded and logged goals")
                return True
            else:
                self.logger.warning("No goals file specified")
                return False
        except Exception as e:
            self.logger.error(f"Failed to load goals: {str(e)}")
            return False

    def _log_goal(self, goal_content: str):
        """Log project goal"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        with open(log_dir / "documents.log", 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"PROJECT GOAL\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"{goal_content}\n")
            f.write(f"\n{'='*80}\n\n")
            
    # def _log_charter(self, charter_content: str):
    #     """Log project charter"""
    #     log_dir = Path("logs")
    #     log_dir.mkdir(exist_ok=True)
    #     with open(log_dir / "documents.log", 'a', encoding='utf-8') as f:
    #         f.write(f"\n{'='*80}\n")
    #         f.write(f"PROJECT CHARTER\n")
    #         f.write(f"{'='*80}\n\n")
    #         f.write(f"{charter_content}\n")
    #         f.write(f"\n{'='*80}\n\n")

    def create_project_structure(self, project_name: str) -> bool:
        """Create project directory structure based on config"""
        try:
            if not self.config:
                raise ValueError("Project configuration not loaded")
                
            # Create base project directory
            base_path = Path(self.config.project_structure['base_folder'].format(
                project_name=project_name
            ))
            base_path.mkdir(parents=True, exist_ok=True)
            
            # Create all specified subdirectories
            for subfolder in self.config.project_structure['subfolders']:
                (base_path / subfolder).mkdir(parents=True, exist_ok=True)
                
            self.project_path = base_path
            self.logger.info(f"Created project structure at {base_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to create project structure: {str(e)}")
            return False

    def validate_project_requirements(self) -> bool:
        """Validate that all required templates exist"""
        try:
            if not self.config:
                self.logger.error("Project configuration not loaded")
                raise ValueError("Project configuration not loaded")
                
            # Get the module directory
            module_dir = Path(__file__).parent
            self.logger.debug(f"Module directory: {module_dir}")
                
            # Check all template files exist
            for template_type, template_data in self.config.templates.items():
                self.logger.debug(f"Validating template: {template_type}")
                
                if template_type == 'meetings':
                    # Handle meeting templates
                    for meeting_name, meeting_config in template_data.items():
                        if isinstance(meeting_config, dict):
                            agenda_file = meeting_config.get('agenda')
                            if agenda_file:
                                template_path = module_dir / "templates" / self.project_type / agenda_file
                                self.logger.debug(f"Checking meeting agenda: {template_path}")
                                if not template_path.exists():
                                    self.logger.error(f"Missing meeting agenda: {template_path}")
                                    raise FileNotFoundError(f"Missing meeting agenda: {template_path}")
                                    
                            doc_template = meeting_config.get('doc')
                            if doc_template:
                                template_path = module_dir / "templates" / self.project_type / doc_template
                                self.logger.debug(f"Checking meeting doc template: {template_path}")
                                if not template_path.exists():
                                    self.logger.error(f"Missing meeting doc template: {template_path}")
                                    raise FileNotFoundError(f"Missing meeting doc template: {template_path}")
                else:
                    # Handle other template types
                    if isinstance(template_data, str):
                        template_path = module_dir / "templates" / self.project_type / template_data
                        self.logger.debug(f"Checking template: {template_path}")
                        if not template_path.exists():
                            self.logger.error(f"Missing template: {template_path}")
                            raise FileNotFoundError(f"Missing template: {template_path}")
                        
            self.logger.info("All required templates validated")
            return True
        except Exception as e:
            self.logger.error(f"Project validation failed: {str(e)}")
            return False

    def initialize_project(self, project_name: str, project_type: Optional[str] = None, goals_file: Optional[str] = None) -> bool:
        """Initialize a new project"""
        try:
            self.logger.info(f"Starting project initialization. Name: {project_name}, Type: {project_type}, Goals: {goals_file}")
            
            # Determine project type based on priority order
            self.project_type = self.determine_project_type(project_type, goals_file)
            self.logger.info(f"Project type determined: {self.project_type}")
            
            # Load and validate configuration
            if not self.load_project_config():
                self.logger.error("Failed to load project configuration")
                return False
                
            if not self.validate_project_requirements():
                self.logger.error("Failed to validate project requirements")
                return False
                
            # Create project structure
            if not self.create_project_structure(project_name):
                self.logger.error("Failed to create project structure")
                return False
            
            # Initialize project documents        
            self.dm = DocumentManager(self.project_path, self.project_type)
            self.dm.initialize_project_docs()
                
            # Load goals if provided
            if goals_file:
                self.logger.info(f"Loading goals from file: {goals_file}")
                if not self.load_goals(goals_file):
                    self.logger.error("Failed to load goals")
                    return False
            else:
                self.logger.warning("No goals file provided for initialization")
                    
            self.logger.info(f"Successfully initialized {self.project_type} project: {project_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Project initialization failed: {str(e)}")
            return False 