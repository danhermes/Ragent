import logging
import unicodedata
from pathlib import Path
from typing import Optional, Dict
from project_start import ProjectStart
from project_work import ProjectWork
from project_documents import ProjectDocuments
from utils.strict_logging import enable_strict_logging

class ProjectMain:
    """Main project orchestrator that handles the complete project workflow"""
   
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        #enable_strict_logging()

    def run_project(self, project_name: str, project_type: str, project_types: Dict, goals_file: Optional[str] = None) -> bool:
        """Run a complete project workflow"""
        try:
            self.logger.info(f"Starting project run. Name: {project_name}, Type: {project_type}, Goals file: {goals_file}")
            
            # Initialize project
            project = ProjectStart()
            if not project.initialize_project(project_name, project_type, goals_file):
                self.logger.error("Failed to initialize project")
                return False

            # Use the project type determined by ProjectStart
            project_type = project.project_type
            self.logger.info(f"Using project type: {project_type}")
            
            # Log goals state after initialization
            self.logger.info(f"Project goals after initialization: {project.goals}")
            if project.config:
                self.logger.info(f"Project config goals: {project.config.goals}")
            else:
                self.logger.warning("No project config available")

            # Run all meetings
            self.logger.info("Creating ProjectWork instance with goals")
            work = ProjectWork(
                project.project_path, 
                project_type, 
                project.config.goals if project.config else None
            )
            self.logger.info(f"ProjectWork goals after initialization: {work.goals}")
            
            if not work.run_all_meetings():
                self.logger.error("Failed to run meetings")
                return False

            # # Generate final document
            # docs = ProjectDocuments()
            # if not docs.load_document_config(project_type):
            #     self.logger.error("Failed to load document config")
            #     return False

            # context = {
            #     'project_name': project_name,
            #     'goals': project.goals,
            #     'design_doc': docs.design_doc,
            #     'implementation_doc': docs.implementation_doc,
            #     'meeting_history': work.conversation_history
            # }
            # self.logger.info(f"Document generation context: {context}")

            # doc = docs.generate_document('technical_design', context)
            # if not doc:
            #     self.logger.error("Failed to generate technical design")
            #     return False

            # if not docs.save_document('technical_design', doc, project.project_path):
            #     self.logger.error("Failed to save technical design")
            #     return False

            self.logger.info(f"Successfully completed project: {project_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error running project: {str(e)}")
            return False 