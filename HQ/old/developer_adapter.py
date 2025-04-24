import os
import sys
# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from apis.autocoder.agent.code_writer import CodeWriter
from apis.autocoder.agent.tester import Tester
from apis.autocoder.agent.test_layer import TestLayer

logger = logging.getLogger(__name__)

class DeveloperAdapter:
    def __init__(self, test_layer: TestLayer = None):
        self.test_layer = test_layer
        self.code_writer = CodeWriter(role="python_dev", test_layer=self.test_layer)
        self.tester = Tester(test_layer=test_layer)

    def handle_task(self, task: str) -> str:
        logger.info(f"[Woz] Starting task: {task}")

        try:
            code = self.code_writer.generate_code(task)
            file_path = self.code_writer.save_code(code)

            logger.info(f"[Woz] Testing code at {file_path}...")
            passed = self.tester.test_manager(code)

            if passed:
                return "Tests passed. Task complete."

            logger.warning(f"[Woz] Initial tests failed. Attempting debug...")
            #fixed_path = revise_code_with_error_context(file_path, "Test failure log")  # Stub for now
            # with open(fixed_path, 'r') as f:
            #     new_code = f.read()
            # passed = self.tester.test_manager(new_code)

            if passed:
                return "Tests passed after debug. Task complete."
            else:
                return "Debug attempt failed. Manual intervention may be required."

        except Exception as e:
            logger.error(f"[Woz] Fatal error during task: {str(e)}")
            return f"Task failed due to internal error: {str(e)}"
