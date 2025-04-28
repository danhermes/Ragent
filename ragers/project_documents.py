import os
import sys
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from helpers.safe_formatter import formatter

@dataclass
class DocumentConfig:
    """Document configuration loaded from YAML"""
    templates: Dict[str, Any]
    output_files: List[str]
    completion_criteria: List[str]
    meeting_rules: Dict[str, Any]

class ProjectDocuments:
    """Handles document generation and management"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config: Optional[DocumentConfig] = None
        self.templates: Dict[str, str] = {}
        self.project_path: Optional[Path] = None
        self.project_type: Optional[str] = None
        self.design_doc = None
        self.implementation_doc = None
        
    def load_document_config(self, project_type: str) -> bool:
        """Load document configuration from YAML"""
        try:
            self.project_type = project_type
            module_dir = Path(__file__).parent
            config_path = module_dir / "templates" / project_type / f"{project_type}_mode.yaml"
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                
            # Convert to strongly typed config
            self.config = DocumentConfig(
                templates=yaml_config['templates'],
                output_files=yaml_config['output_files'],
                completion_criteria=yaml_config['completion_criteria'],
                meeting_rules=yaml_config['meeting_rules']
            )
            self.templates = self.config.templates
            self.logger.info(f"Loaded document configuration for {project_type} project type")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load document config: {str(e)}")
            return False

    def generate_document(self, doc_type: str, context: Dict[str, Any]) -> Optional[str]:
        """Generate a document using the specified template"""
        try:
            self.logger.info(f"Generating {doc_type} document...")
            if not self.config:
                raise ValueError("Document configuration not loaded")
                
            template_file = self.templates.get(doc_type)
            if not template_file:
                raise ValueError(f"No template found for document type: {doc_type}")
                
            template_path = Path(f"templates/{self.project_type}/{template_file}")
            if not template_path.exists():
                raise FileNotFoundError(f"Template file not found: {template_path}")
                
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
                
            # Add default values for common variables if not in context
            default_context = {
                'project_name': self.project_path.name if self.project_path else 'project',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'time': datetime.now().strftime('%H:%M:%S')
            }
            
            # Merge default context with provided context
            full_context = {**default_context, **context}
                
            # Format template with context
            document = formatter.safe_format(template, full_context)
            
            self.logger.info(f"Generated {doc_type} document: {document}")
            if doc_type == 'code_design_meeting':
                self.design_doc = document
            elif doc_type == 'code_implementation_meeting':
                self.implementation_doc = document

            return document
        
        except Exception as e:
            self.logger.error(f"Failed to generate document: {str(e)}")
            return None

    def save_document(self, doc_type: str, content: str, project_path: Path) -> bool:
        """Save document to file"""
        try:
            doc_path = project_path / "deliverables" / f"{doc_type}.md"
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"Saved {doc_type} document")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save document: {str(e)}")
            return False

    def validate_document_completion(self, doc_type: str, content: str) -> bool:
        """Validate that a document meets completion criteria"""
        try:
            if not self.config:
                raise ValueError("Document configuration not loaded")
                
            criteria = self.config.completion_criteria.get(doc_type, [])
            if not criteria:
                self.logger.warning(f"No completion criteria specified for {doc_type}")
                return True
                
            for criterion in criteria:
                if criterion not in content:
                    self.logger.error(f"Document missing required criterion: {criterion}")
                    return False
                    
            self.logger.info(f"Document {doc_type} meets all completion criteria")
            return True
        except Exception as e:
            self.logger.error(f"Failed to validate document completion: {str(e)}")
            return False

    def generate_meeting_document(self, phase: str, meeting_content: Dict[str, Any]) -> Optional[Path]:
        """Generate document for a specific meeting phase"""
        try:
            # Get document template
            doc_template = self.config.templates['meetings'].get(f"{phase}_doc")
            if not doc_template:
                raise ValueError(f"No document template found for {phase}")
                
            # Load template
            template_path = Path(f"templates/{self.project_type}/{doc_template}")
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
                
            # Create document directory
            doc_dir = self.meetings_dir / phase / 'docs'
            doc_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate document
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            doc_path = doc_dir / f"{phase}_doc_{timestamp}.md"
            
            with open(doc_path, 'w', encoding='utf-8') as f:
                # Format template with meeting content
                formatted_content = formatter.safe_format(template_content, meeting_content)
                f.write(formatted_content)
                
            self.logger.info(f"Generated meeting document: {doc_path}")
            return doc_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate meeting document for {phase}: {str(e)}")
            return None
            
    def generate_deliverable(self, deliverable_name: str, content: Dict[str, Any]) -> Optional[Path]:
        """Generate a project deliverable"""
        try:
            if deliverable_name not in self.config.output_files:
                raise ValueError(f"Unknown deliverable: {deliverable_name}")
                
            # Create deliverables directory
            self.deliverables_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate deliverable
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            deliverable_path = self.deliverables_dir / f"{deliverable_name}_{timestamp}"
            
            with open(deliverable_path, 'w', encoding='utf-8') as f:
                if deliverable_name.endswith('.md'):
                    # Format markdown template
                    template_path = Path(f"templates/{self.project_type}/{deliverable_name}")
                    with open(template_path, 'r', encoding='utf-8') as t:
                        template_content = t.read()
                    formatted_content = formatter.safe_format(template_content, content)
                    f.write(formatted_content)
                else:
                    # Write raw content for non-markdown files
                    f.write(str(content))
                    
            self.logger.info(f"Generated deliverable: {deliverable_path}")
            return deliverable_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate deliverable {deliverable_name}: {str(e)}")
            return None
            
    def generate_all_deliverables(self, content: Dict[str, Any]) -> Dict[str, Path]:
        """Generate all required deliverables"""
        deliverables = {}
        
        for deliverable in self.config.output_files:
            path = self.generate_deliverable(deliverable, content)
            if path:
                deliverables[deliverable] = path
            else:
                self.logger.warning(f"Failed to generate {deliverable}")
                
        return deliverables
        
    def validate_deliverables(self) -> bool:
        """Validate that all required deliverables exist"""
        missing = []
        
        for deliverable in self.config.output_files:
            # Check if any file matching the deliverable name exists
            if not any(self.deliverables_dir.glob(f"{deliverable}*")):
                missing.append(deliverable)
                
        if missing:
            self.logger.warning(f"Missing deliverables: {', '.join(missing)}")
            return False
            
        self.logger.info("All required deliverables present")
        return True
        
    def check_completion_criteria(self) -> bool:
        """Check if all completion criteria are met"""
        # Basic criteria checks
        criteria_met = {
            "All meetings completed": self._check_meetings_complete(),
            "All deliverables present": self.validate_deliverables(),
            "Technical design reviewed": self._check_technical_review(),
            "Tests passing": self._check_tests_passing()
        }
        
        # Log status of each criterion
        for criterion, met in criteria_met.items():
            if met:
                self.logger.info(f"✓ {criterion}")
            else:
                self.logger.warning(f"✗ {criterion}")
                
        return all(criteria_met.values())
        
    def _check_meetings_complete(self) -> bool:
        """Check if all required meetings have documentation"""
        for phase in self.config.phases:
            docs_dir = self.meetings_dir / phase / 'docs'
            if not docs_dir.exists() or not any(docs_dir.iterdir()):
                return False
        return True
        
    def _check_technical_review(self) -> bool:
        """Check if technical design has been reviewed"""
        review_dir = self.meetings_dir / 'phase_4_review' / 'docs'
        return review_dir.exists() and any(review_dir.iterdir())
        
    def _check_tests_passing(self) -> bool:
        """Check if all tests are passing"""
        # This would integrate with your testing framework
        # For now, just check if test files exist
        return any(self.deliverables_dir.glob("test_*.py")) 