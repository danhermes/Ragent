import os
import shutil
import logging
from datetime import datetime
from . import code_writer
from . import runner_docker
from . import tester
from . import debugger
from utils.logger import log

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
        #self.code_writer = code_writer  # Use the module directly since generate_code is static

    def _write_log(self, content):
        with open(self.log_file, "a", encoding='utf-8') as f:
            f.write(content + "\n")

    def run_cycle(self):
        # Generate code and save it to a file
        code = code_writer.CodeWriter.generate_code(self.agent_task)
        file_path = code_writer.CodeWriter().save_code(code)
        shutil.copy(file_path, os.path.join(self.debug_dir, os.path.basename(file_path)))
        self._write_log(f"Prompt Task: {self.agent_task}\n")

        for i in range(self.max_iterations):
            self._write_log(f"--- Iteration {i+1} ---")
            log(f"--- Iteration {i+1} ---")

            # stdout, stderr = runner_docker.run_code_in_docker(file_path)

            # self._write_log("STDOUT:\n" + stdout)
            # self._write_log("STDERR:\n" + stderr)

            # log(f"Execution Output:\n{stdout}\nErrors:\n{stderr}")

            # with open(os.path.join(self.debug_dir, f"stdout_{i+1}.txt"), "w", encoding='utf-8') as out_f:
            #     out_f.write(stdout)
            # with open(os.path.join(self.debug_dir, f"stderr_{i+1}.txt"), "w", encoding='utf-8') as err_f:
            #     err_f.write(stderr)

            tests_passed = tester.Tester().test_manager(code)

            if tests_passed:
                msg = "*** All tests passed! ***"
                log(msg)
                self._write_log(msg)
                self.final_status = "success"
                break
            else:
                msg = " XXX Tests failed. Moving to next iteration..."
                log(msg)
                self._write_log(msg)

        if self.final_status != "success":
            msg = "XXXXXXXXXXXXXXX ----- Maximum iterations reached. Final attempt failed."
            log(msg)
            self._write_log(msg)
            self.final_status = "failure"

        # Add summary to end of log
        summary = f"Run Summary:\nStatus: {self.final_status.upper()}\nLog Directory: {self.debug_dir}"
        self._write_log("\n" + summary)
        log(summary)
