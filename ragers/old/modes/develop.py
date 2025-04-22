import os
import sys
from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime
import re
import yaml

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels to root
sys.path.insert(0, parent_dir)

from .base import BaseMode

class DevelopMode(BaseMode):
    """Mode for technical design and development planning"""
    
    def __init__(self):
        super().__init__("develop")
        self.template_dir = Path("ragers/templates/code")
        self.load_config()
        self.load_prompts()
        
    def load_config(self):
        """Load configuration from code_mode.yaml"""
        config_path = self.template_dir / "code_mode.yaml"
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            self.logger.info("Successfully loaded code_mode.yaml")
        except Exception as e:
            self.logger.error(f"Failed to load code_mode.yaml: {e}")
            raise
            
    def load_prompts(self):
        """Load prompts from prompts.yaml"""
        prompt_path = self.template_dir / "code_prompts.yaml"
        try:
            with open(prompt_path, 'r') as f:
                self.prompts = yaml.safe_load(f)['prompts']
            self.logger.info("Successfully loaded code_prompts.yaml")
        except Exception as e:
            self.logger.error(f"Failed to load code_prompts.yaml: {e}")
            raise
            
    def get_meeting_attendees(self, phase: str) -> List[str]:
        """Get the required attendees for a meeting phase"""
        attending = self.config['templates']['meetings'].get(phase, {}).get('attending', '')
        if "Entire Team" in attending:
            return ["Supervisor", "Managers", "Workers"]
        return [role.strip() for role in attending.split(',')]
        
    def get_meeting_doc(self, phase: str) -> str:
        """Get the document template for a meeting phase"""
        return self.config['templates']['meetings'].get(phase + '_doc', '')
        
    def run_meeting(self, orchestrator: Any) -> None:
        """Run development planning meeting focusing on technical design"""
        # Log mode banner
        banner = "\n" + "=" * 80 + "\n"
        banner += "DEVELOP MODE\n"
        banner += "=" * 80 + "\n"
        self.logger.info(banner)
        print(banner)
        
        self.logger.info("Starting development planning meeting")
        
        # Run each meeting phase in sequence
        for phase in self.config['phases']:
            self.logger.info(f"Starting {phase} meeting")
            
            # Get meeting configuration
            prompt = self.prompts[phase]
            attendees = self.get_meeting_attendees(phase)
            doc_template = self.get_meeting_doc(phase)
            
            # Initialize meeting context
            meeting_context = {
                'goals': orchestrator.goals,
                'history': orchestrator._format_conversation_history(),
                'rag_data': orchestrator.RAG_data,
                'phase': phase
            }
            
            # Get responses from each required attendee
            for role in attendees:
                if role == "Supervisor":
                    response = orchestrator.supervisor.get_chat_response(
                        prompt['template'].format(**meeting_context)
                    )
                    orchestrator._log_conversation(phase, "supervisor", response)
                    meeting_context['supervisor_response'] = response
                    
                elif role == "Managers":
                    for manager_name, manager in orchestrator.managers.items():
                        response = manager.get_chat_response(
                            prompt['template'].format(**meeting_context)
                        )
                        orchestrator._log_conversation(phase, f"manager_{manager_name}", response)
                        meeting_context['manager_response'] = response
                        
                elif role == "Workers":
                    for worker_name, worker in orchestrator.workers.items():
                        response = worker.get_chat_response(
                            prompt['template'].format(**meeting_context)
                        )
                        orchestrator._log_conversation(phase, f"worker_{worker_name}", response)
                        meeting_context['worker_response'] = response
            
            # Generate meeting document if template exists
            if doc_template:
                self._generate_meeting_doc(phase, doc_template, meeting_context, orchestrator)
                
    def _generate_meeting_doc(self, phase: str, template_name: str, context: Dict[str, Any], orchestrator: Any):
        """Generate meeting documentation"""
        template_path = self.template_dir / template_name
        doc_path = orchestrator.project_path / 'meetings' / f"{phase}_doc.md"
        
        try:
            # Load template
            with open(template_path, 'r') as f:
                template_content = f.read()
                
            # Format template with meeting content
            doc_content = template_content.format(**context)
            
            # Write document
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(doc_content)
                
            self.logger.info(f"Generated meeting document: {doc_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate meeting document: {e}")
            
    def generate_deliverable(self, orchestrator: Any) -> Path:
        """Generate technical design document"""
        self.logger.info("Generating technical design document")
        
        # Create timestamped deliverable file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deliverable_file = self.deliverables_dir / f"technical_design_{timestamp}.md"
        
        # Load technical design template
        template_path = self.template_dir / self.config['templates']['technical_design']
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Gather content from all meeting phases
        content = {
            'goals': orchestrator.goals,
            'history': orchestrator._format_conversation_history()
        }
        for phase in self.config['phases']:
            content[phase] = self._extract_section(orchestrator, phase)
        
        # Write deliverable content
        with open(deliverable_file, 'w', encoding='utf-8') as f:
            f.write(template_content.format(**content))
            
        # Review and condense the document
        reviewed_file = self.review_deliverable(deliverable_file, orchestrator)
        return reviewed_file
        
    def review_deliverable(self, original_file: Path, orchestrator: Any) -> Path:
        """Review and condense the technical design document using ChatGPT"""
        self.logger.info("Reviewing and condensing technical design document")
        
        # Read the original document
        with open(original_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
            
        # Create prompt for ChatGPT
        review_prompt = f"""You are a technical documentation expert. Your task is to review and improve this technical design document while strictly following these rules:

CRITICAL RULES (DO NOT VIOLATE THESE):
1. DO NOT remove or modify ANY code blocks, technical specifications, or implementation details
2. DO NOT remove or modify ANY class structures, method signatures, or variable definitions
3. DO NOT remove or modify ANY API endpoints, data structures, or technical requirements
4. DO NOT remove or modify ANY configuration settings or environment variables
5. DO NOT remove or modify ANY testing strategies or verification steps

IMPROVEMENT GUIDELINES:
1. Keep all high-level section names intact
2. Condense and improve the prose, particularly in the latter half of the document
3. Remove redundant explanations while maintaining technical accuracy
4. Merge sections only if it improves readability without losing detail
5. Focus on making the document more concise and readable while keeping it thorough
6. Maintain the same markdown formatting
7. Preserve all bullet points and numbered lists
8. Keep all technical terminology and domain-specific language

VALIDATION REQUIREMENTS:
1. The condensed document must contain ALL code blocks from the original
2. The condensed document must contain ALL technical specifications from the original
3. The condensed document must contain ALL implementation details from the original
4. The condensed document must maintain the same technical depth and accuracy

Here is the document to review:
{original_content}

IMPORTANT: Before providing the condensed version, verify that it meets all CRITICAL RULES and VALIDATION REQUIREMENTS. If you cannot meet these requirements, return the original document unchanged."""
        
        # Get condensed version from ChatGPT
        condensed_content = orchestrator.supervisor.get_chat_response(review_prompt)
        
        # Validate that key technical content is preserved
        original_code_blocks = set(re.findall(r'```.*?```', original_content, re.DOTALL))
        condensed_code_blocks = set(re.findall(r'```.*?```', condensed_content, re.DOTALL))
        
        if not original_code_blocks.issubset(condensed_code_blocks):
            self.logger.warning("Condensed document is missing code blocks from original. Using original document.")
            condensed_content = original_content
            
        # Create new filename for condensed version
        condensed_file = original_file.parent / f"technical_design_reviewed_{original_file.stem.split('_')[-1]}.md"
        
        # Write condensed version
        with open(condensed_file, 'w', encoding='utf-8') as f:
            f.write(condensed_content)
            
        self.logger.info(f"Condensed document saved to: {condensed_file}")
        return condensed_file
        
    def _extract_section(self, orchestrator: Any, section_name: str) -> str:
        """Extract a specific section from conversation history"""
        self.logger.info(f"Extracting section: {section_name}")
        self.logger.info(f"Conversation history length: {len(orchestrator.conversation_history)}")
        
        section_content = []
        for msg in orchestrator.conversation_history:
            self.logger.info(f"Checking message with phase: {msg.get('phase', 'NO PHASE')}")
            if msg.get('phase') == section_name:
                self.logger.info(f"Found matching message with role: {msg['role']}")
                section_content.append(f"### {msg['role']}\n\n{msg['content']}\n")
        
        result = "\n".join(section_content)
        self.logger.info(f"Extracted content length: {len(result)}")
        self.logger.info(f"Extracted content: {result[:200]}...")  # Log first 200 chars
        
        return result 