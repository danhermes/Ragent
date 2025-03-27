import logging
import os
from datetime import datetime
from agents.agent_blane import AgentBlane
from agents.agent_dee import AgentDee
from agents.agent_dum import AgentDum
from agents.agent_steve import AgentSteve
from agents.agent_bill import AgentBill
from agents.agent_woz import AgentWoz

class Orchestrator:
    """Manages the company structure and conversation flow between agents"""
    
    def __init__(self):
        # Get logger
        self.logger = logging.getLogger("orchestrator")
        
        self.logger.info("Initializing Orchestrator")
        
        # Create deliverables directory
        self.deliverables_dir = "deliverables"
        if not os.path.exists(self.deliverables_dir):
            os.makedirs(self.deliverables_dir)
            self.logger.debug(f"Created deliverables directory: {self.deliverables_dir}")
        
        # Create conversations directory
        self.conversations_dir = "conversations"
        if not os.path.exists(self.conversations_dir):
            os.makedirs(self.conversations_dir)
            self.logger.debug(f"Created conversations directory: {self.conversations_dir}")
        
        # Initialize conversation file for this session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversation_file = os.path.join(self.conversations_dir, f"conversation_{timestamp}.md")
        self.logger.debug(f"Created conversation file: {self.conversation_file}")
        
        # Test write to conversation file
        try:
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                f.write("# Conversation Log\n\n")
                f.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            self.logger.debug(f"Successfully wrote header to conversation file: {self.conversation_file}")
        except Exception as e:
            self.logger.error(f"Failed to write to conversation file: {str(e)}")
            self.logger.error(f"Current working directory: {os.getcwd()}")
            self.logger.error(f"Conversation file path: {os.path.abspath(self.conversation_file)}")
        
        # Load goals
        self.logger.debug("Loading high-level goals")
        try:
            with open('.goals', 'r') as f:
                self.goals = f.read()
            self.logger.info("Successfully loaded goals")
        except Exception as e:
            self.logger.error(f"Error loading goals: {str(e)}")
            self.goals = "Error: Goals could not be loaded"
        
        # Initialize the company structure
        self.logger.debug("Creating supervisor (Blane)")
        self.supervisor = AgentBlane()
        
        self.logger.debug("Creating managers (Dee and Dum)")
        self.managers = {
            "Dee": AgentDee(),
            "Dum": AgentDum()
        }
        
        self.logger.debug("Creating workers (Steve, Bill, and Woz)")
        self.workers = {
            "Steve": AgentSteve(),
            "Bill": AgentBill(),
            "Woz": AgentWoz()
        }
        
        # Initialize conversation history
        self.conversation_history = []
        self.logger.info("Orchestrator initialization complete")
        
    def _log_conversation(self, phase: str, role: str, content: str):
        """Log a conversation entry to both the history and a file"""
        self.logger.debug(f"=== Starting _log_conversation ===")
        self.logger.debug(f"Phase: {phase}")
        self.logger.debug(f"Role: {role}")
        self.logger.debug(f"Content length: {len(content)}")
        self.logger.debug(f"Content: {content[:100]}...")
        
        # Add to conversation history
        self.conversation_history.append({"role": role, "content": content})
        self.logger.debug(f"Added to conversation history. History length: {len(self.conversation_history)}")
        
        try:
            self.logger.debug(f"Attempting to write to conversation file: {self.conversation_file}")
            # Ensure the file exists
            if not os.path.exists(self.conversation_file):
                self.logger.debug("Conversation file does not exist, creating it")
                with open(self.conversation_file, 'w', encoding='utf-8') as f:
                    f.write("# Conversation Log\n\n")
                    f.write(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Append the conversation
            self.logger.debug("Appending conversation to file")
            with open(self.conversation_file, 'a', encoding='utf-8') as f:
                f.write(f"### {role} ({phase})\n")
                f.write(f"{content}\n\n")
            
            # Verify the write
            if os.path.exists(self.conversation_file):
                file_size = os.path.getsize(self.conversation_file)
                self.logger.debug(f"Successfully logged conversation to {self.conversation_file}. File size: {file_size} bytes")
                
                # Read back the last few lines to verify
                with open(self.conversation_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-5:]
                    self.logger.debug(f"Last lines in file: {''.join(lines)}")
            else:
                self.logger.error("Conversation file was not created")
                
        except Exception as e:
            self.logger.error(f"Error logging conversation: {str(e)}")
            self.logger.error(f"Current working directory: {os.getcwd()}")
            self.logger.error(f"Conversation file path: {os.path.abspath(self.conversation_file)}")
        
        self.logger.debug(f"=== Completed _log_conversation ===")
        
    def strategic_goal_setting(self, high_level_goals: str = None) -> str:
        """Set strategic goals for the company"""
        self.logger.debug("=== Starting strategic_goal_setting ===")
        
        # Use provided goals or loaded goals
        goals_to_use = high_level_goals if high_level_goals else self.goals
        self.logger.debug(f"Using goals: {goals_to_use[:100]}...")
        
        # Get supervisor's strategic goals
        self.logger.debug("Getting supervisor's strategic goals")
        supervisor_prompt = f"Based on these high-level goals: {goals_to_use}\n\nWhat are the strategic goals for our company?"
        supervisor_response = self.supervisor.get_chat_response(supervisor_prompt)
        self.logger.debug(f"Supervisor response: {supervisor_response[:100]}...")
        
        # Log supervisor's response
        self.logger.debug("Logging supervisor's response")
        self._log_conversation("strategic_goal_setting", "supervisor", supervisor_response)
        
        # Get manager feedback
        self.logger.debug("Getting manager feedback")
        for manager_name, manager in self.managers.items():
            manager_prompt = f"Please review and provide feedback on these strategic goals: {supervisor_response}"
            manager_response = manager.get_chat_response(manager_prompt)
            self.logger.debug(f"Manager {manager_name} response: {manager_response[:100]}...")
            self._log_conversation("strategic_goal_setting", f"manager_{manager_name}", manager_response)
        
        # Get worker feedback
        self.logger.debug("Getting worker feedback")
        for worker_name, worker in self.workers.items():
            worker_prompt = f"Please review and provide feedback on these strategic goals: {supervisor_response}"
            worker_response = worker.get_chat_response(worker_prompt)
            self.logger.debug(f"Worker {worker_name} response: {worker_response[:100]}...")
            self._log_conversation("strategic_goal_setting", f"worker_{worker_name}", worker_response)
        
        self.logger.debug("=== Completed strategic_goal_setting ===")
        return self.conversation_history
    
    def company_kickoff(self) -> str:
        """Facilitate company-wide kickoff meeting"""
        self.logger.info("Starting company-wide kickoff meeting")
        
        # Supervisor leads the kickoff
        self.logger.debug("Initiating supervisor's kickoff presentation")
        kickoff_prompt = "Let's have a company-wide kickoff to align everyone on our strategic objectives and team structure."
        kickoff_response = self.supervisor.get_chat_response(kickoff_prompt)
        self.logger.debug(f"Supervisor's kickoff message: {kickoff_response[:100]}...")
        self._log_conversation("company_kickoff", "supervisor", kickoff_response)
        
        # Managers and workers participate
        self.logger.debug("Gathering team feedback")
        for agent_name, agent in {**self.managers, **self.workers}.items():
            self.logger.debug(f"Getting feedback from {agent_name}")
            agent_prompt = f"Supervisor has initiated the kickoff: {kickoff_response}. What are your thoughts and questions?"
            agent_response = agent.get_chat_response(agent_prompt)
            self.logger.debug(f"{agent_name}'s kickoff response: {agent_response[:100]}...")
            self._log_conversation("company_kickoff", agent_name, agent_response)
        
        self.logger.info("Company-wide kickoff complete")
        return self.conversation_history
    
    def project_creation(self) -> str:
        """Facilitate project creation between managers and workers"""
        self.logger.info("Starting project creation phase")
        
        # Each manager works with their team
        for manager_name, manager in self.managers.items():
            self.logger.debug(f"Manager {manager_name} creating projects")
            # Include relevant conversation history in the prompt
            manager_prompt = f"""Based on our previous discussions:
{self._format_conversation_history()}

Let's create strategic projects with clear tasks and deliverables for our team. What projects should we focus on?"""
            
            manager_response = manager.get_chat_response(manager_prompt)
            self.logger.debug(f"{manager_name}'s project outline: {manager_response[:100]}...")
            self._log_conversation("project_creation", manager_name, manager_response)
            
            # Workers under this manager respond
            self.logger.debug(f"Gathering worker feedback for {manager_name}'s team")
            for worker_name, worker in self.workers.items():
                if worker.manager == manager_name:
                    self.logger.debug(f"Getting input from {worker_name}")
                    # Include manager's response and relevant history
                    worker_prompt = f"""Based on our previous discussions:
{self._format_conversation_history()}

Your manager {manager_name} has outlined these projects: {manager_response}
What are your thoughts on the tasks and deliverables? How can you contribute?"""
                    
                    worker_response = worker.get_chat_response(worker_prompt)
                    self.logger.debug(f"{worker_name}'s project response: {worker_response[:100]}...")
                    self._log_conversation("project_creation", worker_name, worker_response)
        
        self.logger.info("Project creation phase complete")
        return self.conversation_history
    
    def _format_conversation_history(self, limit: int = 5) -> str:
        """Format recent conversation history for context"""
        recent_history = self.conversation_history[-limit:] if self.conversation_history else []
        formatted = []
        for msg in recent_history:
            formatted.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(formatted)
    
    def worker_collaboration(self) -> str:
        """Facilitate worker collaboration and task discussion"""
        self.logger.info("Starting worker collaboration phase")
        
        # Workers discuss their tasks and help each other
        for worker_name, worker in self.workers.items():
            self.logger.debug(f"Getting collaboration input from {worker_name}")
            # Include relevant conversation history and other workers' responses
            worker_prompt = f"""Based on our previous discussions:
{self._format_conversation_history()}

Let's discuss our tasks and deliverables, and help each other succeed. 
What are you working on and how can others help?"""
            
            worker_response = worker.get_chat_response(worker_prompt)
            self.logger.debug(f"{worker_name}'s collaboration response: {worker_response[:100]}...")
            self._log_conversation("worker_collaboration", worker_name, worker_response)
        
        self.logger.info("Worker collaboration phase complete")
        return self.conversation_history
    
    def milestone_review(self, milestone: str) -> str:
        """Facilitate milestone review between managers and workers"""
        self.logger.info(f"Starting milestone review for: {milestone}")
        
        # Each manager reviews with their team
        for manager_name, manager in self.managers.items():
            self.logger.debug(f"Manager {manager_name} reviewing milestone")
            # Include relevant conversation history
            manager_prompt = f"""Based on our previous discussions:
{self._format_conversation_history()}

Let's review our progress on milestone: {milestone}
What's the overall status and any concerns?"""
            
            manager_response = manager.get_chat_response(manager_prompt)
            self.logger.debug(f"{manager_name}'s milestone review: {manager_response[:100]}...")
            self._log_conversation("milestone_review", manager_name, manager_response)
            
            # Workers under this manager respond
            self.logger.debug(f"Gathering worker progress reports for {manager_name}'s team")
            for worker_name, worker in self.workers.items():
                if worker.manager == manager_name:
                    self.logger.debug(f"Getting progress report from {worker_name}")
                    # Include manager's review and relevant history
                    worker_prompt = f"""Based on our previous discussions:
{self._format_conversation_history()}

Your manager {manager_name} has reviewed milestone {milestone}: {manager_response}
What's your progress and any challenges? How can others help?"""
                    
                    worker_response = worker.get_chat_response(worker_prompt)
                    self.logger.debug(f"{worker_name}'s progress report: {worker_response[:100]}...")
                    self._log_conversation("milestone_review", worker_name, worker_response)
        
        self.logger.info(f"Milestone review for {milestone} complete")
        return self.conversation_history
    
    def work_loop(self) -> str:
        """Facilitate ongoing work and collaboration between workers"""
        self.logger.info("Starting work loop")
        
        # Workers collaborate and work independently
        for worker_name, worker in self.workers.items():
            self.logger.debug(f"Getting work status from {worker_name}")
            worker_prompt = f"""Based on our previous discussions:
{self._format_conversation_history()}

Let's continue working on our deliverables and goals. What's your current focus and any updates?"""
            
            worker_response = worker.get_chat_response(worker_prompt)
            self.logger.debug(f"{worker_name}'s work status: {worker_response[:100]}...")
            self._log_conversation("work_loop", worker_name, worker_response)
        
        self.logger.info("Work loop complete")
        return self.conversation_history
    
    def present_deliverables(self) -> str:
        """Present deliverables to the Big Boss"""
        self.logger.info("Preparing deliverables for Big Boss review")
        
        # Supervisor summarizes deliverables
        self.logger.debug("Generating supervisor's deliverable summary")
        supervisor_prompt = "Let's prepare a summary of our deliverables for Big Boss review."
        supervisor_response = self.supervisor.get_chat_response(supervisor_prompt)
        self.logger.debug(f"Supervisor's deliverable summary: {supervisor_response[:100]}...")
        self._log_conversation("present_deliverables", "supervisor", supervisor_response)
        
        # Save deliverables to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deliverable_file = os.path.join(self.deliverables_dir, f"deliverables_{timestamp}.md")
        self.logger.info(f"Attempting to save deliverables to: {deliverable_file}")
        
        try:
            # Ensure deliverables directory exists
            if not os.path.exists(self.deliverables_dir):
                self.logger.debug(f"Creating deliverables directory: {self.deliverables_dir}")
                os.makedirs(self.deliverables_dir)
            
            self.logger.debug("Writing deliverables to file")
            with open(deliverable_file, 'w', encoding='utf-8') as f:
                f.write("# Deliverables Report\n\n")
                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("## Goals\n")
                f.write(self.goals)
                f.write("\n\n## Deliverables Summary\n")
                f.write(supervisor_response)
                f.write("\n\n## Reference to Conversation Log\n")
                f.write(f"Full conversation history can be found in: {os.path.basename(self.conversation_file)}\n")
            
            self.logger.info(f"Successfully saved deliverables to: {deliverable_file}")
            
            # Verify file was created
            if os.path.exists(deliverable_file):
                file_size = os.path.getsize(deliverable_file)
                self.logger.info(f"Deliverable file created successfully. Size: {file_size} bytes")
            else:
                self.logger.error("File was not created successfully")
                
        except Exception as e:
            self.logger.error(f"Error saving deliverables: {str(e)}")
            self.logger.error(f"Current working directory: {os.getcwd()}")
            self.logger.error(f"Deliverables directory path: {os.path.abspath(self.deliverables_dir)}")
        
        self.logger.info("Deliverable presentation complete")
        return self.conversation_history
    
    def handle_upward_communication(self, message: str, sender: str) -> str:
        """Handle questions or statements traveling upward"""
        self.logger.info(f"Handling upward communication from {sender}")
        self.logger.debug(f"Message content: {message}")
        
        # Determine the appropriate recipient based on sender's manager
        if sender in self.workers:
            recipient = self.managers[self.workers[sender].manager]
            recipient_name = self.workers[sender].manager
            self.logger.debug(f"Routing message to {recipient_name} (worker's manager)")
        elif sender in self.managers:
            recipient = self.supervisor
            recipient_name = "supervisor"
            self.logger.debug("Routing message to supervisor (manager's supervisor)")
        else:
            self.logger.error(f"Invalid sender: {sender}")
            return "Invalid sender"
        
        # Forward the message
        self.logger.debug(f"Forwarding message to {recipient_name}")
        recipient_prompt = f"Message from {sender}: {message}"
        recipient_response = recipient.get_chat_response(recipient_prompt)
        self.logger.debug(f"{recipient_name}'s response: {recipient_response[:100]}...")
        self._log_conversation("upward_communication", recipient_name, recipient_response)
        
        self.logger.info(f"Upward communication handling complete for {sender}")
        return self.conversation_history 