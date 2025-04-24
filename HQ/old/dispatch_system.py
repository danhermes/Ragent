import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json
import os

logger = logging.getLogger(__name__)

@dataclass
class Task:
    """Represents a task in the dispatch system."""
    task_id: str
    command: str
    type: str
    project: str
    workflow_engine: str
    status: str
    phase: str
    agents: List[str]
    tools: List[str]
    logs: List[str]
    started_at: datetime
    q_doc: Optional[str] = None

class DispatchSystem:
    """Core dispatch system that handles task management and workflow orchestration."""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.workflow_engines = {
            'code': {'engine': 'AutoCoder', 'agents': ['Woz', 'reviewer']},
            'write': {'engine': 'LitLegos', 'agents': ['Writer', 'Editor']},
            'plan': {'engine': 'Ragers', 'agents': ['Planner', 'Strategist']}
        }
        self.tools = ['AutoCoder', 'LitLegos', 'n8n', 'OpenAI Assistants']
        self.data_sources = ['Gmail API', 'Cloud Doc Repo', 'GitHub', 'Local Docs', 'SQL DB', 'Vector DB']
        
    def create_task(self, command: str, task_type: str, project: str) -> Task:
        """Create a new task with the given parameters."""
        task_id = f"{len(self.tasks) + 1:04d}"
        task = Task(
            task_id=task_id,
            command=command,
            type=task_type,
            project=project,
            workflow_engine=self.workflow_engines[task_type]['engine'],
            status='pending',
            phase='initialization',
            agents=self.workflow_engines[task_type]['agents'],
            tools=self.tools,
            logs=[],
            started_at=datetime.now()
        )
        self.tasks[task_id] = task
        self._save_task_state(task)
        return task
    
    def get_task_status(self, task_id: str) -> str:
        """Get the current status of a task."""
        if task_id not in self.tasks:
            return f"Error: Task {task_id} not found"
        return self.tasks[task_id].status
    
    def update_task_status(self, task_id: str, status: str, phase: Optional[str] = None) -> None:
        """Update the status and optionally the phase of a task."""
        if task_id not in self.tasks:
            logger.error(f"Task {task_id} not found")
            return
        task = self.tasks[task_id]
        task.status = status
        if phase:
            task.phase = phase
        task.logs.append(f"[{datetime.now()}] Status updated to {status}")
        self._save_task_state(task)
    
    def _save_task_state(self, task: Task) -> None:
        """Save task state to disk."""
        task_dir = f"tasks/{task.task_id}"
        os.makedirs(task_dir, exist_ok=True)
        
        state_file = f"{task_dir}/state.json"
        with open(state_file, 'w') as f:
            json.dump({
                'task_id': task.task_id,
                'command': task.command,
                'type': task.type,
                'project': task.project,
                'workflow_engine': task.workflow_engine,
                'status': task.status,
                'phase': task.phase,
                'agents': task.agents,
                'tools': task.tools,
                'logs': task.logs,
                'started_at': task.started_at.isoformat(),
                'q_doc': task.q_doc
            }, f, indent=2)
    
    def get_available_commands(self) -> Dict[str, List[str]]:
        """Get a list of available commands and their aliases."""
        return {
            'assign': ['start', 'run'],
            'status': ['?'],
            'pause': [],
            'stop': ['abort'],
            'resume': [],
            'where': [],
            'get': [],
            'code': [],
            'write': [],
            'plan': [],
            'ask': [],
            'give': []
        }
    
    def handle_command(self, command: str, args: Optional[str] = None) -> str:
        """Handle a command from the CLI."""
        cmd = command.lower()
        if cmd in ['assign', 'start', 'run']:
            if not args:
                return "Error: No task provided"
            # Parse task type and project from args
            parts = args.split(maxsplit=1)
            if len(parts) < 2:
                return "Error: Please specify task type and project"
            task_type, project = parts[0], parts[1]
            if task_type not in self.workflow_engines:
                return f"Error: Unknown task type {task_type}"
            task = self.create_task(args, task_type, project)
            return f"Task {task.task_id} created: {task.command}"
        
        elif cmd in ['status', '?']:
            if not args:
                return "Error: No task ID provided"
            return self.get_task_status(args)
        
        elif cmd in ['stop', 'abort']:
            if not args:
                return "Error: No task ID provided"
            self.update_task_status(args, 'aborted')
            return f"Task {args} aborted"
        
        return "Error: Unknown command" 