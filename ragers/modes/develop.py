import os
import sys
from typing import Any, Dict
from pathlib import Path
from datetime import datetime
import re

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels to root
sys.path.insert(0, parent_dir)

from .base import BaseMode

class DevelopMode(BaseMode):
    """Mode for technical design and development planning"""
    
    def __init__(self):
        super().__init__("develop")
        
    def run_meeting(self, orchestrator: Any) -> None:
        """Run development planning meeting focusing on technical design"""
        # Log mode banner
        banner = "\n" + "=" * 80 + "\n"
        banner += "DEVELOP MODE\n"
        banner += "=" * 80 + "\n"
        self.logger.info(banner)
        print(banner)
        
        self.logger.info("Starting development planning meeting")
        
        # Get supervisor's technical requirements
        supervisor_prompt = f"""Based on these high-level goals: {orchestrator.goals}
{orchestrator._format_conversation_history()}

What are the key technical requirements and challenges for this project? Focus on:
1. Alignment with GOALS and requirements
2. Core functionality requirements
3. Technical constraints and limitations
4. Design and architecture considerations
5. Code examples to address the key challenges and functionalities
6. Recommended class structure with methods and variables
7. Outline the technical hurdles that are unresolved to address in the next meeting.

RAG DATA: {orchestrator.RAG_data}"""
        supervisor_response = orchestrator.supervisor.get_chat_response(supervisor_prompt)
        self.logger.debug(f"Supervisor response length: {len(supervisor_response)}")
        orchestrator._log_conversation("technical_requirements", "supervisor", supervisor_response)
        
        # Get manager architectural design
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Review these requirements: {supervisor_response}

Design the application focusing on:
1. Alignment with GOALS and requirements
2. Effective, elegant technical architecture
3. Blockers to address in this meeting, prioritized by importance
4. Ways to tackle the most important aspects of the application
5. With intractible problems, step back and consider alternative ways of tackling them.
6. Discuss what is working and what is not working on this team and how to do more of the former and improve the latter.
7. Outline the hurdles that are unresolved to address in this meeting.
8. List blockers and achievements in this meeting at the end of the meeting.

Provide specific solutions and technical design where appropriate.

GOALS: {orchestrator.goals}"""
            manager_response = manager.get_chat_response(manager_prompt)
            self.logger.debug(f"Manager {manager_name} response length: {len(manager_response)}")
            orchestrator._log_conversation("architectural_design", f"manager_{manager_name}", manager_response)
            
        # Get worker implementation details
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Review these technical requirements and architectural design:
Supervisor: {supervisor_response}
Manager: {manager_response}

Specify:
1. Meets GOALS and requirements.
2. What is most important to address in this meeting.
3. Blockers to address in this meeting, prioritized by importance
4. Detailed application architecture and design for today
5. Detailed class structures and relationships for today
6. Specific solutions to the blockers identified in the previous meeting
7. Testing strategies for today

Provide code examples and implementation details.

GOALS: {orchestrator.goals}"""
            worker_response = worker.get_chat_response(worker_prompt)
            self.logger.debug(f"Worker {worker_name} response length: {len(worker_response)}")
            orchestrator._log_conversation("implementation_details", f"worker_{worker_name}", worker_response)
            
    def review_deliverables(self, orchestrator: Any) -> bool:
        """Review technical design for completeness and feasibility"""
        self.logger.info("Reviewing technical design")
        self.logger.debug(f"Current conversation history length: {len(orchestrator.conversation_history)}")
        
        # Get manager review
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Review the technical design for:
1. Meets GOALS and requirements
2. Completeness of the technical design
3. Technical feasibility
4. Clarity and readability
5. Simplicity
6. Testing coverage

Previous discussions:
{orchestrator._format_conversation_history()}

GOALS: {orchestrator.goals}"""
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("technical_review", f"manager_{manager_name}", manager_response)
            
        # Get worker verification
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Verify the technical implementation details:
1. Meets GOALS and requirements.
2. Architecture completeness.
3. Technical feasibility.
4. Brevity and elegance.
5. Clarity and readability.
6. Completeness of the technical design.
7. Testing coverage.

Previous discussions:
{orchestrator._format_conversation_history()}

GOALS: {orchestrator.goals}"""
            worker_response = worker.get_chat_response(worker_prompt)
            orchestrator._log_conversation("implementation_verify", f"worker_{worker_name}", worker_response)
            
        return True
        
    def generate_deliverable(self, orchestrator: Any) -> Path:
        """Generate technical design document"""
        self.logger.info("Generating technical design document")
        
        # Create timestamped deliverable file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deliverable_file = self.deliverables_dir / f"technical_design_{timestamp}.md"
        
        # Write deliverable content
        with open(deliverable_file, 'w', encoding='utf-8') as f:
            f.write("# Technical Design Document\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Project Goals\n")
            f.write(orchestrator.goals)
            f.write("\n\n## Technical Requirements\n")
            f.write(self._extract_section(orchestrator, "technical_requirements"))
            f.write("\n\n## System Architecture\n")
            f.write(self._extract_section(orchestrator, "architectural_design"))
            f.write("\n\n## Implementation Details\n")
            f.write(self._extract_section(orchestrator, "implementation_details"))
            f.write("\n\n## Technical Review\n")
            f.write(self._extract_section(orchestrator, "technical_review"))
            f.write("\n\n## Implementation Verification\n")
            f.write(self._extract_section(orchestrator, "implementation_verify"))
            
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