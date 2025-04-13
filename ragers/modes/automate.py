import os
import sys
import json
from typing import Any, Dict, List
from pathlib import Path
from datetime import datetime

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels to root
sys.path.insert(0, parent_dir)

from .base import BaseMode
from apis.autocoder.adapters.n8n_adapter import N8nAdapter

class AutomateMode(BaseMode):
    """Mode for workflow automation using autocoder's AgentBuildCycle"""
    
    def __init__(self):
        super().__init__("automate")
        self.workflow_adapter = N8nAdapter(logger=self.logger)
        
    def run_meeting(self, orchestrator: Any) -> None:
        """Run automation planning meeting focusing on technical requirements"""
        # Log mode banner
        banner = "\n" + "=" * 80 + "\n"
        banner += "AUTOMATE MODE\n"
        banner += "=" * 80 + "\n"
        self.logger.info(banner)
        print(banner)
        
        self.logger.info("Starting automation planning meeting")
        
        # Get workflow helper methods for prompts
        workflow_methods = self.workflow_adapter.get_workflow_helper_methods()
        
        # Get supervisor's automation requirements
        supervisor_prompt = f"""Based on these high-level goals: {orchestrator.goals}
{orchestrator._format_conversation_history()}

What specific tasks need to be automated? Focus on:
1. Input data sources
2. Required transformations
3. Output destinations
4. Trigger conditions

Available workflow methods:
{workflow_methods}

RAG DATA: {orchestrator.RAG_data}"""
        supervisor_response = orchestrator.supervisor.get_chat_response(supervisor_prompt)
        orchestrator._log_conversation("automation_requirements", "supervisor", supervisor_response)
        
        # Get manager technical specifications
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Review these automation requirements: {supervisor_response}

Specify:
1. Required workflow steps
2. Data transformations needed
3. API integrations required
4. Testing requirements

Available workflow methods:
{workflow_methods}

GOALS: {orchestrator.goals}"""
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("automation_specs", f"manager_{manager_name}", manager_response)
        
        # Get worker implementation details
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Review these automation specifications: {manager_response}

Detail the requirements for the workflow implementation. Your response MUST include a 'requirements' field with the following structure:

```python
requirements = {{
    "name": "Workflow Name",  # Descriptive name for the workflow
    "trigger": {{
        "type": "schedule",   # Type of trigger (schedule, webhook, etc.)
        "interval": "days",   # How often to run (days, hours, minutes)
        "time": "HH:MM"      # Time to run (24-hour format)
    }},
    "input": {{
        "type": "text_generation",  # Type of input (text_generation, file, api, etc.)
        "source": "openai",         # Source of input (openai, file, api, etc.)
        "prompt": "Your prompt"     # Prompt or input specification
    }},
    "transformations": [  # List of transformation steps
        {{
            "name": "Step 1",       # Descriptive name for the transformation
            "type": "text_processing",  # Type of transformation
            "description": "What this step does",  # Detailed description
            "input_format": "text",  # Expected input format
            "output_format": "json"  # Expected output format
        }},
        # Add more transformation steps as needed
    ],
    "logic": [  # List of logic/decision points
        {{
            "name": "Decision Point 1",  # Descriptive name
            "type": "condition",         # Type of logic (condition, loop, etc.)
            "description": "What this decision does",  # Detailed description
            "conditions": [              # List of conditions
                {{
                    "field": "status",   # Field to check
                    "operator": "equals", # Comparison operator
                    "value": "success"   # Value to compare against
                }}
            ]
        }},
        # Add more logic points as needed
    ],
    "output": {{
        "type": "file",            # Type of output (file, email, api, etc.)
        "destination": "dropbox",  # Where to save output
        "path": "/path",          # Path for output
        "filename": "output.txt"  # Output filename
    }},
    "notification": {{
        "type": "email",          # Type of notification
        "to": "recipient@example.com",  # Notification recipient
        "subject": "Subject",     # Notification subject
        "body": "Message body"    # Notification message
    }},
    "error_handling": {{
        "retry_count": 3,         # Number of retry attempts
        "notify_on_failure": True # Whether to notify on failure
    }}
}}
```

For each transformation and logic node:
1. Describe what the node does
2. Specify input and output formats
3. List any conditions or rules
4. Note dependencies on other nodes

GOALS: {orchestrator.goals}"""
            worker_response = worker.get_chat_response(worker_prompt)
            orchestrator._log_conversation("automation_implementation", f"worker_{worker_name}", worker_response)
            
    def review_deliverables(self, orchestrator: Any) -> None:
        """Review automation workflow with managers and workers"""
        self.logger.info("Starting automation deliverables review")
        
        # Each manager reviews the workflow
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Review the workflow for:
1. Completeness of requirements
2. Technical feasibility
3. Data flow correctness
4. Error handling adequacy
5. Security considerations

GOALS: {orchestrator.goals}"""
            
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("automation_review", manager_name, manager_response)
            
            # Workers under this manager verify implementation
            for worker_name, worker in orchestrator.workers.items():
                if worker.manager == manager_name:
                    worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Your manager {manager_name} has reviewed the workflow: {manager_response}
Verify:
1. Requirements are met
2. Technical implementation is correct
3. Data transformations work
4. Error handling is implemented
5. Testing is complete

GOALS: {orchestrator.goals}"""
                    
                    worker_response = worker.get_chat_response(worker_prompt)
                    orchestrator._log_conversation("automation_verification", worker_name, worker_response)
                    
    def generate_deliverable(self, orchestrator: Any) -> Path:
        """Generate n8n workflow using automation adapter"""
        self.logger.info("Starting workflow generation")
        
        try:
            # Get workflow requirements from worker
            requirements = {
                "name": "Generated Workflow",
                "trigger": {
                    "type": "schedule",
                    "interval": "days",
                    "time": "09:00"
                },
                "input": {
                    "type": "text_generation",
                    "source": "openai",
                    "prompt": "Generate content"
                },
                "transformations": [],
                "output": {
                    "type": "file",
                    "destination": "local",
                    "path": "/outputs",
                    "filename": "output.json"
                }
            }
            
            # Get workflow specifications from n8n adapter
            specifications = {
                "nodes": self.workflow_adapter.get_nodes(),
                "workflow_examples": self.workflow_adapter.get_workflow_examples()
            }
            
            # Use automation adapter to generate and deploy workflow
            self.logger.info("Using automation adapter to generate workflow")
            result = orchestrator.automation_adapter.generate_workflow(requirements, specifications)
            
            if not result or not result.get("success"):
                self.logger.error("Failed to generate workflow")
                return None
                
            self.logger.info("Successfully generated and deployed workflow")
            return Path(result["workflow_file"])
            
        except Exception as e:
            self.logger.error(f"Error generating workflow: {str(e)}")
            return None
            
    def _extract_workflow_requirements(self, conversation_history: List[Dict]) -> Dict:
        """Extract workflow requirements from conversation history"""
        self.logger.info("Starting workflow requirements extraction")
        
        try:
            # Get the last worker response
            worker_response = next(
                (msg for msg in reversed(conversation_history) 
                 if msg["role"].startswith("worker_")),
                None
            )
            
            if not worker_response:
                self.logger.error("No worker response found in conversation history")
                return {}
                
            content = worker_response.get("content", "")
            if not content:
                self.logger.error("Worker response content is empty")
                return {}
                
            self.logger.debug(f"Worker response content: {content}")
            
            # Find the requirements block
            start_idx = content.find("requirements = {")
            if start_idx == -1:
                self.logger.error("Could not find requirements block")
                return {}
                
            # Find the end of the block
            end_idx = content.find("}", start_idx)
            if end_idx == -1:
                self.logger.error("Could not find end of requirements block")
                return {}
                
            # Include the closing brace
            end_idx += 1
            
            # Extract the requirements dictionary text
            requirements_text = content[start_idx:end_idx]
            self.logger.debug(f"Extracted requirements text: {requirements_text}")
            
            try:
                # Convert Python booleans to JSON booleans
                requirements_text = (
                    requirements_text
                    .replace("True", "true")
                    .replace("False", "false")
                    .replace("None", "null")
                )
                
                # Parse as JSON
                requirements = json.loads(requirements_text)
                self.logger.info("Successfully parsed requirements")
                return requirements
                
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Failed to parse requirements: {str(json_error)}")
                self.logger.error(f"Requirements text that failed to parse: {requirements_text}")
                return {}
            
        except Exception as e:
            self.logger.error(f"Error extracting workflow requirements: {str(e)}")
            return {} 