from typing import Any, Dict
from pathlib import Path
from datetime import datetime
from .base_mode import BaseMode
from ..apis.autocoder.adapters.proof_adapter import ProofAdapter

class ProofMode(BaseMode):
    """Mode for text proofing using proof API"""
    
    def __init__(self):
        super().__init__("proof")
        self.proof_adapter = ProofAdapter()
        
    def run_meeting(self, orchestrator: Any) -> None:
        """Run proofing planning meeting focusing on text requirements"""
        self.logger.info("Starting proofing planning meeting")
        
        # Get supervisor's proofing requirements
        supervisor_prompt = f"""Based on these high-level goals: {orchestrator.goals}
{orchestrator._format_conversation_history()}

What specific aspects of the text need to be proofed? Focus on:
1. Grammar and syntax
2. Style and tone
3. Terminology and jargon
4. Formatting and structure
5. Consistency with standards

RAG DATA: {orchestrator.RAG_data}"""
        supervisor_response = orchestrator.supervisor.get_chat_response(supervisor_prompt)
        orchestrator._log_conversation("proofing_requirements", "supervisor", supervisor_response)
        
        # Get manager technical specifications
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Review these proofing requirements: {supervisor_response}

Specify:
1. Required proofing tools
2. Style guide requirements
3. Terminology standards
4. Formatting rules
5. Quality metrics

GOALS: {orchestrator.goals}"""
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("proofing_specs", f"manager_{manager_name}", manager_response)
            
        # Get worker implementation details
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Review these proofing requirements and specifications:
Supervisor: {supervisor_response}
Manager: {manager_response}

Specify:
1. Proofing approach
2. Tool configurations
3. Quality checks
4. Error handling
5. Testing strategy

GOALS: {orchestrator.goals}"""
            worker_response = worker.get_chat_response(worker_prompt)
            orchestrator._log_conversation("proofing_impl", f"worker_{worker_name}", worker_response)
            
    def review_deliverables(self, orchestrator: Any) -> bool:
        """Review proofed content for accuracy and compliance"""
        self.logger.info("Reviewing proofed content")
        
        # Get manager review
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Review the proofed content for:
1. Grammar and syntax accuracy
2. Style consistency
3. Terminology correctness
4. Formatting compliance
5. Overall readability

Previous discussions:
{orchestrator._format_conversation_history()}

GOALS: {orchestrator.goals}"""
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("proofing_review", f"manager_{manager_name}", manager_response)
            
        # Get worker verification
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Verify that all proofing corrections were applied correctly:
1. Grammar fixes
2. Style adjustments
3. Terminology updates
4. Formatting changes
5. Quality improvements

Previous discussions:
{orchestrator._format_conversation_history()}

GOALS: {orchestrator.goals}"""
            worker_response = worker.get_chat_response(worker_prompt)
            orchestrator._log_conversation("proofing_verify", f"worker_{worker_name}", worker_response)
            
        return True
        
    def generate_deliverable(self, orchestrator: Any) -> Path:
        """Generate proofed content using proof adapter"""
        self.logger.info("Generating proofed content")
        
        try:
            # Get text and requirements from conversation history
            text = self._extract_text(orchestrator)
            requirements = self._extract_requirements(orchestrator)
            
            # Proof text using proof adapter
            proof_file = self.proof_adapter.proof_text(text, requirements)
            
            if proof_file:
                self.logger.info(f"Successfully generated proofed content: {proof_file}")
            else:
                self.logger.error("Failed to generate proofed content")
                
            return proof_file
            
        except Exception as e:
            self.logger.error(f"Error generating proofed content: {str(e)}")
            return None
            
    def _extract_text(self, orchestrator: Any) -> str:
        """Extract text to be proofed from conversation history"""
        try:
            # Get the latest conversation content
            history = orchestrator._format_conversation_history()
            
            # Look for a file name in the conversation history
            # This assumes the file name is mentioned in the last message
            last_message = history.split("\n")[-1]
            
            # Look for a file name pattern
            import re
            file_pattern = r'file:\s*([^\s]+)'
            match = re.search(file_pattern, last_message)
            
            if not match:
                self.logger.warning("No file name found in conversation history")
                return ""
                
            file_name = match.group(1)
            file_path = Path("proof/sources") / file_name
            
            if not file_path.exists():
                self.logger.error(f"File not found: {file_path}")
                return ""
                
            # Read the file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                self.logger.error(f"Error reading file {file_path}: {str(e)}")
                return ""
                
        except Exception as e:
            self.logger.error(f"Error extracting text from conversation history: {str(e)}")
            return ""
        
    def _extract_requirements(self, orchestrator: Any) -> Dict:
        """Extract proofing requirements from conversation history"""
        # This would parse the conversation history to extract structured requirements
        return {} 