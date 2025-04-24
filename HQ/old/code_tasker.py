from HQ.old.developer_adapter import DeveloperAdapter
from workflow_cli import WorkflowCLI
from apis.autocoder.agent.test_layer import TestLayer
import logging
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"logs/code_tasker_{timestamp}.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CodeTasker:
    def __init__(self):

        self.test_layer = TestLayer()
        self.woz = DeveloperAdapter(self.test_layer)
        self.task_history = []
        self.active_task = None
        self.cli = WorkflowCLI(self, self.test_layer)

    def get_on_this(self, task: str):
        logger.info(f"Blaine assigned new task: {task}")
        self.active_task = task
        self.task_history.append({"task": task, "status": "assigned"})
        result = self.woz.handle_task(task)
        self.task_history[-1]["result"] = result
        return result

    def current_status(self):
        return self.task_history[-1] if self.task_history else {}

if __name__ == '__main__':
    tasker = CodeTasker()
    tasker.cli.run()
