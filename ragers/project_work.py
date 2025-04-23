import os
import logging
import importlib
from pathlib import Path
from datetime import datetime
import string
from typing import Dict, Any, List, Optional
import yaml
from dataclasses import dataclass
from helpers.call_ChatGPT import CallChatGPT
from collections import defaultdict

@dataclass
class Meeting:
    """Meeting configuration"""
    phase: str
    template: str
    doc_template: str
    participants: List[str]

class ProjectWork:
    """Handles project meetings and team interactions"""
    
    def __init__(self, project_path: Path, project_type: str, goals: Optional[List[str]] = None):
        self.logger = logging.getLogger(__name__)
        self.project_path = project_path
        self.project_type = project_type
        self.goals = goals or []
        self.rag_data = ""
        self.charter = ""
        self.load_config()
        self.conversation_history: List[Dict[str, Any]] = []
        self.agents: Dict[str, Any] = {}
        self.initialize_team()
        
        # Set up logging directory
        self.log_dir = self.project_path / "logs"
        self.log_dir.mkdir(exist_ok=True)
        
        # Set up file handlers for different log types
        self._setup_logging()
        
        # Load document meeting prompt
        self._load_document_meeting_prompt()
        
    def _setup_logging(self):
        """Set up additional logging handlers for different log types"""
        # Main project log
        project_log = self.log_dir / "project.log"
        project_handler = logging.FileHandler(project_log)
        project_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(project_handler)
        
        # ChatGPT interactions log
        self.chatgpt_log = self.log_dir / "chatgpt_calls.log"
        self.chatgpt_handler = logging.FileHandler(self.chatgpt_log)
        self.chatgpt_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        
        # Goals and charter log
        self.docs_log = self.log_dir / "documents.log"
        self.docs_handler = logging.FileHandler(self.docs_log)
        self.docs_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        
    def _log_goal(self, goal_content: str):
        """Log project goal"""
        with open(self.docs_log, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"PROJECT GOAL\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"{goal_content}\n")
            f.write(f"\n{'='*80}\n\n")
            
    def _log_charter(self, charter_content: str):
        """Log project charter"""
        with open(self.docs_log, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"PROJECT CHARTER\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"{charter_content}\n")
            f.write(f"\n{'='*80}\n\n")
            
    def _log_chatgpt_interaction(self, role: str, prompt: str, response: str):
        """Log ChatGPT interaction with role information"""
        with open(self.chatgpt_log, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"MEETING: {self.current_phase.upper()}\n")
            f.write(f"ROLE: {role}\n")
            f.write(f"{'='*80}\n\n")
            
            f.write(f"PROMPT:\n")
            f.write(f"{'-'*40}\n")
            f.write(f"{prompt}\n\n")
            
            f.write(f"RESPONSE:\n")
            f.write(f"{'-'*40}\n")
            f.write(f"{response}\n")
            f.write(f"\n{'='*80}\n\n")
            
            # Also log to project log
            self.logger.info(f"ChatGPT interaction logged for {role} in {self.current_phase} meeting")
        
    def load_config(self):
        """Load configuration from project_type-specific YAML"""
        """ TODO v2.0Autonomous Agent: Estimate, scope and scale. Work and review, repeat. """
        """ TODO Estimate scope and scale accordingly, creating a (Project_type)_mode.yaml file"""
        """ TODO Work though project, review for completion. Completed or reestimate."""
        """ TODO Adjust charter, staff, meetings, agenda, or docs.  Rerun project until done."""
        """ TODO v2.5 Alternate project_types serially (plan, code, write, plan...)"""
        """ TODO v3.0 Multi-thread for parallel project_types"""
        """ TODO v4.0 Simultaneous project_types"""

        module_dir = Path(__file__).parent
        config_path = module_dir / "templates" / self.project_type / f"{self.project_type}_mode.yaml"
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            self.logger.info(f"Successfully loaded {self.project_type}_mode.yaml")
        except Exception as e:
            self.logger.error(f"Failed to load {self.project_type}_mode.yaml: {e}")
            raise
            
    def initialize_team(self):
        """Initialize team members based on required roles from config"""
        try:
            for role, role_config in self.config['required_roles'].items():
                name = role_config['name']
                
                # Import the corresponding agent class
                agent_module = importlib.import_module(f"agents.agent_{name.lower()}")
                agent_class = getattr(agent_module, f"Agent{name}")
                
                # Instantiate the agent with role and name
                self.agents[name] = {
                    'instance': agent_class(),
                    'role': role,
                    'name': name
                }
                self.logger.info(f"Initialized {name} as {role}")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize team: {str(e)}")
            raise
            
    def get_agents_by_role(self, role: str) -> Dict[str, Any]:
        """Get all agents of a specific role"""
        return {
            name: agent['instance'] 
            for name, agent in self.agents.items() 
            if role == agent['role']
        }
        
    def _log_conversation(self, phase: str, role: str, content: str):
        """Log conversation entry"""
        self.conversation_history.append({
            "phase": phase,
            "role": role,
            "content": content
        })
        
        # Save to meeting log file
        meeting_log_path = os.path.join(
            self.project_path,
            'meetings',
            f"{phase}.md"
        )
        
        # Create meetings directory if it doesn't exist
        os.makedirs(os.path.dirname(meeting_log_path), exist_ok=True)
        
        # Write to file, overwriting any existing content
        with open(meeting_log_path, 'w', encoding='utf-8') as f:
            f.write(f"# {phase.title()} Meeting\n\n")
            for entry in self.conversation_history:
                if entry['phase'] == phase:
                    f.write(f"## {entry['role']}\n\n{entry['content']}\n\n")
            
    def _format_conversation_history(self, limit: int = 5) -> str:
        """Format recent conversation history"""
        recent = self.conversation_history[-limit:] if self.conversation_history else []
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent])
        
    def run_meeting(self, phase: str) -> bool:
        """Run a meeting for the specified phase"""
        try:
            module_dir = Path(__file__).parent
            self.current_phase = phase  # Store current phase for logging
            if phase not in self.config['templates']['meetings']:
                raise ValueError(f"Unknown phase: {phase}")
                
            self.logger.info(f"Starting {phase} meeting")
            self.logger.info(f"Available goals for meeting: {self.goals}")
            if self.goals:
                self.logger.info("Goals content:")
                for i, goal in enumerate(self.goals, 1):
                    self.logger.info(f"Goal {i}: {goal}")
            else:
                self.logger.warning("No goals available for meeting")
            
            meeting_config = self.config['templates']['meetings'][phase]

            agenda_template = meeting_config.get('agenda')
            agenda_path = module_dir / "templates" / self.project_type / agenda_template
            with open(agenda_path, 'r', encoding='utf-8') as f:
                agenda = f.read
            
            # Load prompts from code_prompts.yaml
            prompts_path = module_dir / "templates" / self.project_type / "code_prompts.yaml"
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts_config = yaml.safe_load(f)
                
            # Get the template for this phase
            if phase not in prompts_config['prompts']:
                raise ValueError(f"No prompt template found for phase: {phase}")
            template_content = prompts_config['prompts'][phase]['template']
            
            # Get input files for the meeting
            self.logger.info(f"Meeting config for {phase}: {meeting_config}")
            input_files = self._get_meeting_input(phase, meeting_config)
            self.logger.info(f"Input files for {phase}: {input_files}")
            
            # Get responses from each participant based on roles
            for role in self._get_phase_participants(phase):
                agents = self.get_agents_by_role(role)
                for name, agent in agents.items():
                    self.logger.info(f"Processing {name} ({role}) in {phase} meeting")
                    
                    # Use stored goals
                    if not self.goals:
                        self.logger.warning("No goals found in config")
                        goals = ["No project goals specified"]
                    else:
                        goals = self.goals
                        self.logger.info(f"Using goals for {name}:")
                        for i, goal in enumerate(goals, 1):
                            self.logger.info(f"Goal {i}: {goal}")
                        
                    # Create a comprehensive context for template formatting
                    meeting_rules = prompts_config['prompts']['meeting_rules']
                    self.rag_data = self.charter
                    context = {
                        'goals': "\n".join(goals),
                        'history': self._format_conversation_history(),
                        'phase': phase,
                        'meeting_rules': meeting_rules,
                        'opening': "\n".join(meeting_rules['structure']['opening']),
                        'closing': "\n".join(meeting_rules['structure']['closing']),
                        'project_type': self.project_type,
                        'project_name': self.project_path.name,
                        'current_date': datetime.now().strftime("%Y-%m-%d"),
                        'input': meeting_config.get('input', ''),
                        'output': meeting_config.get('output', ''),
                        'length': meeting_config.get('length', ''),
                        'agenda': agenda,
                        'rag_data': self.rag_data
                    }
                    
                    # Add input files to context
                    self.logger.debug(f"Context before adding input files: {context}")
                    self.logger.debug(f"Input files to be added: {input_files}")
                    context.update(input_files)
                    self.logger.debug(f"Context after adding input files: {context}")
                    self.logger.debug(f"Template content: {template_content}")
                    
                    # Replace template placeholders with correct input file keys
                    template_content = template_content.replace('{input_file[0]}', '{input_file_0}')
                    template_content = template_content.replace('{input_file[1]}', '{input_file_1}')
                    

                    # Format the template with the context
                    prompt = ""
                    #prompt = template_content.format(**context)

                    safe_context = defaultdict(lambda: '[MISSING]', context)
                    try:
                        prompt = template_content.format_map(safe_context)
                        self.logger.debug(f"Formatted prompt: {prompt[:100]}")
                    except Exception as e:
                        self.logger.error(f"Error formatting prompt: {e}")
                        raise

                    
                    self.logger.info(f"==-------== Prompt for {name}:\n{prompt[:200]}")
                    
                    
                    response = agent.get_chat_response(prompt)


                    self.logger.info(f"=========== Response from {name}:\n{response}")
                    
                    # Log the ChatGPT interaction
                    self._log_chatgpt_interaction(f"{role}_{name}", prompt, response)
                    
                    self._log_conversation(phase, f"{role}_{name}", response)
                    
                    # Generate meeting document for all phases
                    if agenda_template:
                        # Add the response to the context for the document
                        context['response'] = response
                        self.logger.info(f"Context for document generation: {context['response']}")
                        self.logger.debug(f"Full context before document generation: {context}")
                        self._generate_meeting_doc(phase, context)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to run {phase} meeting: {str(e)}")
            self.logger.error(f"Exception type: {type(e).__name__}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            return False
            
    def _get_phase_participants(self, phase: str) -> List[str]:
        """Determine meeting participants based on phase"""
        # Get participants from config
        phase_config = self.config['templates']['meetings'].get(phase, {})
        return phase_config.get('attending', [])
        
    def _load_document_meeting_prompt(self):
        """Load document meeting prompt from config"""
        try:
            module_dir = Path(__file__).parent
            prompts_path = module_dir / "templates" / self.project_type / f"{self.project_type}_prompts.yaml"
            with open(prompts_path, 'r', encoding='utf-8') as f:
                prompts_config = yaml.safe_load(f)
                
            self.document_meeting_prompt = prompts_config['prompts']['document_meeting']
            self.logger.info("Loaded document meeting prompt")
        except Exception as e:
            self.logger.error(f"Failed to load document meeting prompt: {str(e)}")
            raise

    def _generate_meeting_doc(self, phase: str, context: dict) -> None:
        """Generate meeting document using template and response."""
        try:
            # Get meeting configuration
            meeting_config = self.config['templates']['meetings'].get(phase, {})
            if not meeting_config:
                raise ValueError(f"No meeting configuration found for phase: {phase}")
            
            # Get output file from meeting configuration
            output_file = meeting_config.get('output')
            if not output_file:
                raise ValueError(f"No output file specified for phase: {phase}")
            
            # Determine output directory based on document type
            doc_types = self.config['templates'].get('document_types', {})
            if output_file in doc_types.get('deliverables', []):
                output_dir = 'deliverables'
            elif output_file in doc_types.get('charters', []):
                output_dir = 'charters'
            elif output_file in doc_types.get('meetings', []):
                output_dir = 'meetings'
            else:
                output_dir = 'meetings'  # Default to meetings directory
            
            # Get template path
            module_dir = Path(__file__).parent
            template_path = module_dir / "templates" / self.project_type / output_file
            if not template_path.exists():
                raise FileNotFoundError(f"Template file not found: {template_path}")
            
            # Read template
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    self.logger.info(f"LOADING Template.")
                    template = f.read()
                    self.logger.info(f"LOADED----- Template:\n {repr(template[:1000])}")
                self.logger.info(f"LOADED Template length: {len(template)}")
                self.logger.info(f"LOADED Template type: {type(template)}")
                self.logger.info(f"LOADED Template:\n{template[:200]}")  ########### FAILING HERE
            except Exception as e:
                self.logger.error(f"Failed to read template file: {str(e)}")
                self.logger.error(f"Template path: {template_path}")
                raise
            
            self.logger.info(f"SHOW Template Path:\n{template_path}")
            self.logger.info(f"SHOW Template:\n{template[:1000]}...") ########### FAILING HERE
            self.logger.info("FIELDS FOUND IN TEMPLATE:")
            for _, field, _, _ in string.Formatter().parse(template):
                if field:
                    self.logger.info(" ->", field)
            # Get response from context
            self.logger.info(f"Context keys available: {list(context.keys())}")
            response = context.get('response', '')
            if not response:
                self.logger.error(f"Context contents: {context}")
                raise ValueError("No response found in context")
            self.logger.info(f"LOADED Response:\n{response}")


            unified_context = {
                "template": template,
                "response": response
            }
            
            safe_unified_context = defaultdict(lambda: '[MISSING]', unified_context)
            try:
                unified_prompt = self.document_meeting_prompt['user'].format_map(safe_unified_context)
                self.logger.debug(f"Formatted prompt: {unified_prompt[:100]}")
            except Exception as e:
                self.logger.error(f"Error formatting prompt: {e}")
                raise

            #unified_prompt = self.document_meeting_prompt['user'].format(
            #    template=template,
            #    response=response
            #)

            self.logger.info(f"UNIFIED Prompt:\n{unified_prompt}")
            
            # Create messages for document worker
            messages = [
                {
                    "role": "system",
                    "content": self.document_meeting_prompt['system']
                },
                {
                    "role": "user",
                    "content": unified_prompt
                }
            ]
            
            # Get merged content from document worker
            document_worker = self.get_agents_by_role('Worker')
            if not document_worker:
                raise ValueError("No document worker found")
                
            document_worker = next(iter(document_worker.values()))
            
            # Log the messages being sent to the document worker
            self.logger.info("Document worker messages:")
            for msg in messages:
                self.logger.info(f"Role: {msg['role']}")
                self.logger.info(f"Content length: {len(msg['content'])}")
                self.logger.info(f"Content preview: {msg['content']}")
            
            merged_content = document_worker.get_chat_response(messages)
            
            if not merged_content:
                raise ValueError("Failed to generate merged content")
            
            # Log the merged content details
            self.logger.info(f"Merged content length: {len(merged_content)}")
            self.logger.info(f"Merged content preview: {merged_content[:1000]}...")
            
            # Write to output file
            output_path = os.path.join(self.project_path, output_dir, output_file)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(merged_content)
            
            # Log file write details
            self.logger.info(f"Wrote merged content to: {output_path}")
            self.logger.info(f"File size after write: {os.path.getsize(output_path)} bytes")
            
            # Update in-memory charter if this is a charter file
            if output_file in doc_types.get('charters', []):
                self.charter = merged_content
                self.logger.info("Updated in-memory charter with merged content")
            
            self.logger.info(f"Generated {output_file} in {output_dir} directory")
            
        except Exception as e:
            self.logger.error(f"Error generating meeting document: {str(e)}")
            raise

    def _read_meeting_doc(self, doc_path: Path) -> Optional[str]:
        """Read a meeting document from disk"""
        try:
            if not doc_path.exists():
                self.logger.warning(f"Document not found: {doc_path}")
                return None
                
            self.logger.info(f"Reading document: {doc_path}")
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.logger.info(f"Successfully read {len(content)} bytes from {doc_path}")
            return content
        except Exception as e:
            self.logger.error(f"Failed to read meeting document: {str(e)}")
            return None

    def _get_meeting_input(self, phase: str, meeting_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get input files for a meeting"""
        input_files = {}
        module_dir = Path(__file__).parent
        
        def get_input_path(input_file: str) -> Path:
            """Determine the correct input path based on file type"""
            # First check project directory
            if input_file == 'code_project_charter.md':
                project_path = self.project_path / "charters" / input_file
                if project_path.exists():
                    return project_path
            else:
                project_path = self.project_path / "meetings" / input_file
                if project_path.exists():
                    return project_path
            
            # If not in project directory, use template
            return module_dir / "templates" / self.project_type / input_file
        
        # Get input from config and handle comma-separated files
        input_config = meeting_config.get('input', '')
        if not input_config:
            self.logger.warning(f"No input files specified for {phase}")
            return input_files
            
        # Split input into list if it's a comma-separated string
        if isinstance(input_config, str):
            input_list = [f.strip() for f in input_config.split(',')]
            if len(input_list) == 1:
                input_list = input_list[0]  # Keep as string if single file
        else:
            input_list = input_config
            
        # Handle single input file
        if isinstance(input_list, str):
            self.logger.info(f"{phase}: single input {input_list}")
            input_path = get_input_path(input_list)
            content = self._read_meeting_doc(input_path)
            if content:
                input_files['input_file'] = content
                
        # Handle multiple input files
        elif isinstance(input_list, list):
            self.logger.info(f"{phase}: {len(input_list)} inputs")
            for i, input_file in enumerate(input_list):
                input_path = get_input_path(input_file)
                content = self._read_meeting_doc(input_path)
                if content:
                    input_files[f'input_file_{i}'] = content
                    self.logger.info(f"Added input file {i} content to context for {phase}")
                    
        if not input_files:
            self.logger.warning(f"No input files found for {phase}")
        else:
            self.logger.info(f"{phase}: loaded {len(input_files)} inputs")
            
        return input_files
        
    def run_all_meetings(self) -> bool:
        """Run all meetings in configured order"""
        try:
            for phase in self.config['phases']:
                if not self.run_meeting(phase):
                    self.logger.error(f"Failed during {phase} phase")
                    return False
                    
            self.logger.info("Successfully completed all meetings")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to run all meetings: {str(e)}")
            return False
            
    def validate_completion(self) -> bool:
        """Validate that all completion criteria are met"""
        try:
            base_folder = self.config['project_structure']['base_folder'].format(
                project_name=self.project_path.name
            )
            
            # Check for required output files
            for output_file in self.config['output_files']:
                file_path = os.path.join(base_folder, 'deliverables', output_file)
                if not os.path.exists(file_path):
                    self.logger.warning(f"Missing output file: {output_file}")
                    return False
                    
            # Check meeting completion
            for phase in self.config['phases']:
                meeting_log = os.path.join(base_folder, 'meetings', f"{phase}.md")
                if not os.path.exists(meeting_log):
                    self.logger.warning(f"Missing meeting log: {phase}")
                    return False
                    
            self.logger.info("All completion criteria met")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating completion: {e}")
            return False 