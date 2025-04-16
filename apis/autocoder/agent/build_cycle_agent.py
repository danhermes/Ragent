import os
import sys
import shutil
import logging
from datetime import datetime
from pathlib import Path

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from . import code_writer
from . import runner_docker
from . import tester
from . import debugger
from utils.logger import log
from apis.autocoder.adapters.n8n_adapter import N8nAdapter

logger = logging.getLogger(__name__)

class AgentBuildCycle:
    def __init__(self, agent_task, max_iterations=3, log_dir="debuglog"):
        self.agent_task = agent_task
        self.max_iterations = max_iterations
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(log_dir, f"debug_cycle_{timestamp}.log")
        self.debug_dir = os.path.join(log_dir, f"debug_run_{timestamp}")
        os.makedirs(self.debug_dir, exist_ok=True)
        self.final_status = None
        
        # Initialize n8n adapter if needed
        self.n8n_adapter = N8nAdapter() if self._is_n8n_language() else None

    def _is_n8n_language(self) -> bool:
        """Check if task is for n8n workflow generation"""
        return isinstance(self.agent_task, dict) and self.agent_task.get("language") == "n8n"

    def _write_log(self, content):
        with open(self.log_file, "a", encoding='utf-8') as f:
            f.write(content + "\n")

    def run_cycle(self):
        logger.info(f"Starting build cycle for task: {self.agent_task}\n")

        if self._is_n8n_language():
            # Handle n8n workflow task
            logger.info("Generating n8n workflow...")
            
            # Get n8n-specific context
            nodes = self.n8n_adapter.get_nodes()
            workflow_examples = self.n8n_adapter.get_workflow_examples()
            
            # Create context for code generation
            context = {
                "nodes": nodes,
                "workflow_examples": workflow_examples,
                "requirements": self.agent_task.get("requirements", {}),
                "specifications": self.agent_task.get("specifications", {})
            }
            
            # Generate workflow code
            code = code_writer.CodeWriter.generate_code(context)
            workflow_json = self.n8n_adapter.parse_workflow_code(code)
            
            # Save and deploy workflow
            workflow_file = self.n8n_adapter.save_workflow(workflow_json)
            if workflow_file:
                success = self.n8n_adapter.deploy_workflow(workflow_json)
                if success:
                    self.final_status = "success"
                    return {"workflow_file": str(workflow_file)}
                else:
                    self.final_status = "failure"
                    return None
            else:
                self.final_status = "failure"
                return None
        else:
            # Handle regular Python code generation task
            logger.info("Generating Python code...")
            code = code_writer.CodeWriter.generate_code(self.agent_task)
            file_path = code_writer.CodeWriter().save_code(code)
            shutil.copy(file_path, os.path.join(self.debug_dir, os.path.basename(file_path)))

            for i in range(self.max_iterations):
                logger.info(f"\n--- Iteration {i+1} of {self.max_iterations} ---")

                tests_passed = tester.Tester().test_manager(code)

                if tests_passed:
                    msg = "All tests passed"
                    log(msg)
                    logger.info(msg)
                    self.final_status = "success"
                    break
                else:
                    msg = "Tests failed"
                    log(msg)
                    logger.info(msg)

            if self.final_status != "success":
                msg = "Maximum iterations reached. Build failed."
                log(msg)
                logger.info(msg)
                self.final_status = "failure"

        # Add summary to end of log
        summary = f"\nBuild Cycle Summary:\nStatus: {self.final_status.upper()}\nIterations: {i+1}\nLog Directory: {self.debug_dir}"
        logger.info(summary)
        log(summary)
