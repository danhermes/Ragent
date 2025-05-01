import os
import sys
from pathlib import Path

# Add the root directory to Python path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import readline
from typing import Optional, Tuple
from apis.autocoder.agent.test_layer import TestLayer
import logging
from HQ.dispatch_system import DispatchSystem
from HQ.nlp_processor import NLPProcessor
from agents.agent_blane import AgentBlane

logger = logging.getLogger(__name__)

class WorkflowCLI:
    def __init__(self, test_layer: TestLayer = None, openai_api_key: Optional[str] = None):
        self.test_layer = test_layer
        self.dispatch = DispatchSystem()
        self.nlp = NLPProcessor(openai_api_key) if openai_api_key else None
        self.blane = AgentBlane()
        self.prompt = "(Blane) > "
        self.commands = {
            "assign": self._handle_assign,
            "status": self._handle_status,
            "help": self._handle_help,
            "exit": self._handle_exit
        }

    def _handle_assign(self, task: str) -> str:
        """Handle task assignment."""
        if not task:
            return "Error: No task provided"
        if self.test_layer and self.test_layer.enabled:
            logger.debug(f"Test layer enabled for task: {task}")
        return self.dispatch.handle_command("assign", task)

    def _handle_status(self, task_id: Optional[str] = None) -> str:
        """Handle status check."""
        if not task_id:
            return "Error: No task ID provided"
        return self.dispatch.handle_command("status", task_id)

    def _handle_help(self, _: Optional[str] = None) -> str:
        """Display help information."""
        commands = self.dispatch.get_available_commands()
        help_text = ["Available commands:"]
        for cmd, aliases in commands.items():
            aliases_str = f" ({', '.join(aliases)})" if aliases else ""
            help_text.append(f"  {cmd}{aliases_str} - {self._get_command_description(cmd)}")
        return "\n".join(help_text)

    def _get_command_description(self, cmd: str) -> str:
        """Get description for a command."""
        descriptions = {
            "assign": "Assign a new task",
            "status": "Check current task status",
            "pause": "Pause a running task",
            "stop": "Stop/abort a task",
            "resume": "Resume a paused task",
            "where": "Get task location/context",
            "get": "Retrieve task information",
            "code": "Start a coding task",
            "write": "Start a writing task",
            "plan": "Start a planning task",
            "ask": "Ask a question about a task",
            "give": "Provide information for a task",
            "help": "Show this help message",
            "exit": "Exit the program"
        }
        return descriptions.get(cmd, "No description available")

    def _handle_exit(self, _: Optional[str] = None) -> str:
        """Handle exit command."""
        return "exit"

    def _cli_response(self, message: str) -> None:
        """Output a message to the user with Blane's prompt format."""
        print(f"(Blane) > {message}")

    def _parse_natural_language(self, user_input: str) -> Tuple[str, Optional[str]]:
        """Parse natural language input into command and args."""
        if not self.nlp:
            return "help", None
            
        cmd, args, confidence, explanation = self.nlp.parse_command(user_input)
        
        if confidence < 0.7:
            self._cli_response(f"I'm not very confident about this interpretation. {explanation}")
            self._cli_response(f"Did you mean: {cmd} {args if args else ''}? (y/n)")
            if input().lower() != 'y':
                return "help", None
                
        return cmd, args

    def run(self):
        """Run the CLI interface."""
        self._cli_response("Ready to receive tasks. Type 'help' for available commands.")
        
        while True:
            try:
                user_input = input(self.prompt).strip()
                if not user_input:
                    continue

                # Try natural language parsing if available
                if self.nlp:
                    cmd, args = self._parse_natural_language(user_input)
                else:
                    # Fallback to traditional command parsing
                    parts = user_input.split(maxsplit=1)
                    cmd = parts[0].lower()
                    args = parts[1] if len(parts) > 1 else None

                if cmd in self.commands:
                    result = self.commands[cmd](args)
                    if result == "exit":
                        self._cli_response("Shutting down.")
                        break
                    self._cli_response(result)
                else:
                    self._cli_response("Unknown command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                self._cli_response("\nInterrupted. Type 'exit' to quit.")
            except Exception as e:
                self._cli_response(f"Error: {e}")

if __name__ == "__main__":
    import os
    cli = WorkflowCLI(openai_api_key=os.getenv('OPENAI_API_KEY'))
    cli.run()
