import os
import sys
from typing import Any, Dict
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
        self.workflow_adapter = N8nAdapter()
        
    def run_meeting(self, orchestrator: Any) -> None:
        """Run automation planning meeting focusing on technical requirements"""
        # Log mode banner
        banner = "\n" + "=" * 80 + "\n"
        banner += "AUTOMATE MODE\n"
        banner += "=" * 80 + "\n"
        self.logger.info(banner)
        print(banner)
        
        self.logger.info("Starting automation planning meeting")
        
        # Get supervisor's automation requirements
        supervisor_prompt = f"""Based on these high-level goals: {orchestrator.goals}
{orchestrator._format_conversation_history()}

What specific tasks need to be automated? Focus on:
1. Input data sources
2. Required transformations
3. Output destinations
4. Trigger conditions
5. Error handling needs

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
4. Error handling approach
5. Testing requirements

GOALS: {orchestrator.goals}"""
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("automation_specs", f"manager_{manager_name}", manager_response)
        
        # Get worker implementation details
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Review these automation specifications: {manager_response}

Detail:
1. Specific workflow logic
2. API call details
3. Data transformation steps
4. Error handling implementation
5. Testing approach

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
        """Generate n8n workflow using n8n adapter"""
        self.logger.info("Generating n8n workflow")
        
        try:
            # Get requirements and specifications from conversation history
            requirements = self._extract_requirements(orchestrator)
            specifications = self._extract_specifications(orchestrator)
            
            # Generate workflow using n8n adapter
            workflow_file = self.workflow_adapter.generate_workflow(requirements, specifications)
            
            if workflow_file:
                # Deploy workflow to n8n
                success = self.workflow_adapter.deploy_workflow(workflow_file)
                if success:
                    self.logger.info(f"Successfully deployed workflow to n8n")
                else:
                    self.logger.error("Failed to deploy workflow to n8n")
                    
            return workflow_file
            
        except Exception as e:
            self.logger.error(f"Error generating workflow: {str(e)}")
            return None
            
    def _extract_requirements(self, orchestrator: Any) -> Dict:
        """Extract requirements from conversation history"""
        # This would parse the conversation history to extract structured requirements
        return {}
        
    def _extract_specifications(self, orchestrator: Any) -> Dict:
        """Extract specifications from conversation history"""
        # This would parse the conversation history to extract structured specifications
        return {} 