from typing import Any
from pathlib import Path
from datetime import datetime
from .base import BaseMode

class PlanMode(BaseMode):
    """Mode for strategic planning and project management"""
    
    def __init__(self):
        super().__init__("plan")
        
    def run_meeting(self, orchestrator: Any) -> None:
        """Run planning meeting focusing on project requirements"""
        # Log mode banner
        banner = "\n" + "=" * 80 + "\n"
        banner += "PLAN MODE\n"
        banner += "=" * 80 + "\n"
        self.logger.info(banner)
        print(banner)
        
        self.logger.info("Starting planning meeting")
        
        # Get supervisor's project requirements
        supervisor_prompt = f"""Based on these high-level goals: {orchestrator.goals}
{orchestrator._format_conversation_history()}

What are the strategic goals for our company? RAG DATA: {orchestrator.RAG_data}"""
        supervisor_response = orchestrator.supervisor.get_chat_response(supervisor_prompt)
        orchestrator._log_conversation("strategic_goal_setting", "supervisor", supervisor_response)
        
        # Get manager feedback
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Please review and provide feedback on these strategic goals: {supervisor_response}
How do these align with our high-level goals: {orchestrator.goals}?"""
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("strategic_goal_setting", f"manager_{manager_name}", manager_response)
        
        # Get worker feedback
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Please review and provide feedback on these strategic goals: {supervisor_response}
How do these align with our high-level goals: {orchestrator.goals}?"""
            worker_response = worker.get_chat_response(worker_prompt)
            orchestrator._log_conversation("strategic_goal_setting", f"worker_{worker_name}", worker_response)
            
    def review_deliverables(self, orchestrator: Any) -> None:
        """Review planning deliverables with managers and workers"""
        self.logger.info("Starting planning deliverables review")
        
        # Each manager reviews with their team
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Let's review our strategic plans and deliverables. What's the status and any concerns?
GOALS: {orchestrator.goals}"""
            
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("plan_review", manager_name, manager_response)
            
            # Workers under this manager respond
            for worker_name, worker in orchestrator.workers.items():
                if worker.manager == manager_name:
                    worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Your manager {manager_name} has reviewed the plans: {manager_response}
What's your progress and any challenges? How can others help?
GOALS: {orchestrator.goals}"""
                    
                    worker_response = worker.get_chat_response(worker_prompt)
                    orchestrator._log_conversation("plan_review", worker_name, worker_response)
                    
    def generate_deliverable(self, orchestrator: Any) -> Path:
        """Generate planning deliverable"""
        self.logger.info("Generating planning deliverable")
        
        # Create timestamped deliverable file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deliverable_file = self.deliverables_dir / f"plan_{timestamp}.md"
        
        # Write deliverable content
        with open(deliverable_file, 'w', encoding='utf-8') as f:
            f.write("# Strategic Planning Deliverable\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Goals\n")
            f.write(orchestrator.goals)
            f.write("\n\n## Strategic Plans\n")
            f.write(orchestrator._format_conversation_history())
            
        return deliverable_file
        
    def run_company_kickoff(self, orchestrator: Any) -> None:
        """Run company-wide kickoff meeting"""
        self.logger.info("Starting company-wide kickoff meeting")
        
        # Supervisor leads the kickoff
        kickoff_prompt = f"""Let's have a company-wide kickoff to align everyone on our strategic objectives and team structure.
{orchestrator._format_conversation_history()}
GOALS: {orchestrator.goals} RAG DATA: {orchestrator.RAG_data}"""
        kickoff_response = orchestrator.supervisor.get_chat_response(kickoff_prompt)
        orchestrator._log_conversation("company_kickoff", "supervisor", kickoff_response)
        
        # Managers and workers participate
        for agent_name, agent in {**orchestrator.managers, **orchestrator.workers}.items():
            agent_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Supervisor has initiated the kickoff: {kickoff_response}
What are your thoughts and questions?
GOALS: {orchestrator.goals} RAG DATA: {orchestrator.RAG_data}"""
            agent_response = agent.get_chat_response(agent_prompt)
            orchestrator._log_conversation("company_kickoff", agent_name, agent_response)
            
    def run_project_creation(self, orchestrator: Any) -> None:
        """Run project creation phase"""
        self.logger.info("Starting project creation phase")
        
        # Each manager works with their team
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Let's create strategic projects with clear tasks and deliverables for our team. What projects should we focus on?
GOALS: {orchestrator.goals} RAG DATA: {orchestrator.RAG_data}"""
            
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("project_creation", manager_name, manager_response)
            
            # Workers under this manager respond
            for worker_name, worker in orchestrator.workers.items():
                if worker.manager == manager_name:
                    worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Your manager {manager_name} has outlined these projects: {manager_response}
What are your thoughts on the tasks and deliverables? How can you contribute?
GOALS: {orchestrator.goals} RAG DATA: {orchestrator.RAG_data}"""
                    
                    worker_response = worker.get_chat_response(worker_prompt)
                    orchestrator._log_conversation("project_creation", worker_name, worker_response)
                    
    def run_worker_collaboration(self, orchestrator: Any) -> None:
        """Run worker collaboration phase"""
        self.logger.info("Starting worker collaboration phase")
        
        # Workers discuss their tasks and help each other
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Let's discuss our tasks and deliverables, and help each other succeed. 
What are you working on and how can others help?
GOALS: {orchestrator.goals}"""
            
            worker_response = worker.get_chat_response(worker_prompt)
            orchestrator._log_conversation("worker_collaboration", worker_name, worker_response)
            
    def run_milestone_review(self, orchestrator: Any, milestone: str) -> None:
        """Run milestone review phase"""
        self.logger.info(f"Starting milestone review for: {milestone}")
        
        # Each manager reviews with their team
        for manager_name, manager in orchestrator.managers.items():
            manager_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Let's review our progress on milestone: {milestone}
What's the overall status and any concerns?
GOALS: {orchestrator.goals}"""
            
            manager_response = manager.get_chat_response(manager_prompt)
            orchestrator._log_conversation("milestone_review", manager_name, manager_response)
            
            # Workers under this manager respond
            for worker_name, worker in orchestrator.workers.items():
                if worker.manager == manager_name:
                    worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Your manager {manager_name} has reviewed milestone {milestone}: {manager_response}
What's your progress and any challenges? How can others help?
GOALS: {orchestrator.goals} RAG DATA: {orchestrator.RAG_data}"""
                    
                    worker_response = worker.get_chat_response(worker_prompt)
                    orchestrator._log_conversation("milestone_review", worker_name, worker_response)
                    
    def run_work_loop(self, orchestrator: Any) -> None:
        """Run work loop phase"""
        self.logger.info("Starting work loop")
        
        # Workers collaborate and work independently
        for worker_name, worker in orchestrator.workers.items():
            worker_prompt = f"""Based on our previous discussions:
{orchestrator._format_conversation_history()}

Let's continue working on our deliverables and goals. What's your current focus and any updates?
GOALS: {orchestrator.goals} RAG DATA: {orchestrator.RAG_data}"""
            
            worker_response = worker.get_chat_response(worker_prompt)
            orchestrator._log_conversation("work_loop", worker_name, worker_response)
            
    def run_present_deliverables(self, orchestrator: Any) -> Path:
        """Run deliverables presentation phase"""
        self.logger.info("Preparing deliverables for Big Boss review")
        
        # Supervisor summarizes deliverables
        supervisor_prompt = f"""Let's prepare a summary of our deliverables for Big Boss review.
{orchestrator._format_conversation_history()}
GOALS: {orchestrator.goals} RAG DATA: {orchestrator.RAG_data}"""
        supervisor_response = orchestrator.supervisor.get_chat_response(supervisor_prompt)
        orchestrator._log_conversation("present_deliverables", "supervisor", supervisor_response)
        
        # Save deliverables to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deliverable_file = orchestrator.deliverables_dir / f"deliverables_{timestamp}.md"
        
        # Write deliverables content
        with open(deliverable_file, 'w', encoding='utf-8') as f:
            f.write("# Deliverables Report\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Goals\n")
            f.write(orchestrator.goals)
            f.write("\n\n## Deliverables Summary\n")
            f.write(supervisor_response)
            f.write("\n\n## Reference to Conversation Log\n")
            f.write(f"Full conversation history can be found in: {orchestrator.conversation_file}\n")
            
        return deliverable_file 