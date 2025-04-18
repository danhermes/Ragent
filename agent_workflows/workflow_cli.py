import readline
from typing import Optional
from apis.autocoder.agent.test_layer import TestLayer
import logging

logger = logging.getLogger(__name__)

class WorkflowCLI:
    def __init__(self, tasker, test_layer: TestLayer = None):
        self.tasker = tasker
        self.test_layer = test_layer
        self.prompt = "(Blaine) > "
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
        return self.tasker.get_on_this(task)

    def _handle_status(self, _: Optional[str] = None) -> str:
        """Handle status check."""
        status = self.tasker.current_status()
        return f"Current status: {status}"

    def _handle_help(self, _: Optional[str] = None) -> str:
        """Display help information."""
        return "\n".join([
            "Available commands:",
            "  assign <task> - Assign a new task",
            "  status       - Check current status",
            "  help         - Show this help message",
            "  exit         - Exit the program"
        ])

    def _handle_exit(self, _: Optional[str] = None) -> str:
        """Handle exit command."""
        return "exit"

    def run(self):
        """Run the CLI interface."""
        print("(Blaine) > Ready to receive tasks. Type 'help' for available commands.")
        
        while True:
            try:
                command = input(self.prompt).strip()
                if not command:
                    continue

                cmd, *args = command.split(maxsplit=1)
                cmd = cmd.lower()
                arg = args[0] if args else None

                if cmd in self.commands:
                    result = self.commands[cmd](arg)
                    if result == "exit":
                        print("(Blaine) > Shutting down.")
                        break
                    print(f"(Blaine) > {result}")
                else:
                    print("(Blaine) > Unknown command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n(Blaine) > Interrupted. Type 'exit' to quit.")
            except Exception as e:
                print(f"(Blaine) > Error: {e}")
