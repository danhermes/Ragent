import os
import sys
import logging
from typing import Dict, List, Optional
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from apis.n8n.n8n_workflow_helper import N8nWorkflowHelper
from apis.n8n.config import N8nConfig

class N8nAdapter:
    """Adapter for n8n-specific functionality used by autocoder"""
    
    def __init__(self, logger=None):
        self.config = N8nConfig()
        self.workflow_helper = N8nWorkflowHelper(self.config)
        self.logger = logger or logging.getLogger("n8n_adapter")
        
    def get_nodes(self) -> Dict:
        """Get available n8n nodes"""
        try:
            return self.workflow_helper.get_nodes()
        except Exception as e:
            self.logger.error(f"Error getting n8n nodes: {str(e)}")
            return {}
            
    def deploy_workflow(self, workflow_json: Dict) -> bool:
        """Deploy workflow to n8n"""
        try:
            # Create workflow using helper with the JSON provided by autocoder
            workflow = self.workflow_helper.create_workflow(
                name=workflow_json.get("name", "Generated Workflow"),
                nodes=workflow_json.get("nodes", []),
                connections=workflow_json.get("connections", {})
            )
            
            # Deploy using helper's API client
            return self.workflow_helper.api_client.deploy_workflow(workflow)
            
        except Exception as e:
            self.logger.error(f"Error deploying workflow to n8n: {str(e)}")
            return False
            
    def get_workflow_examples(self) -> str:
        """Get example workflows from n8n/workflows directory"""
        try:
            workflow_dir = Path("apis/n8n/workflows")
            if not workflow_dir.exists():
                self.logger.warning(f"Workflow directory not found: {workflow_dir}")
                return ""
                
            examples = []
            for workflow_file in workflow_dir.glob("*.json"):
                try:
                    with open(workflow_file, 'r', encoding='utf-8') as f:
                        workflow = json.load(f)
                        examples.append(f"""
Workflow: {workflow_file.stem}
{json.dumps(workflow, indent=2)}
""")
                except Exception as e:
                    self.logger.error(f"Error loading workflow {workflow_file}: {str(e)}")
                    
            return "\n".join(examples)
            
        except Exception as e:
            self.logger.error(f"Error loading workflow examples: {str(e)}")
            return ""
            
    def save_workflow(self, workflow_json: Dict) -> Path:
        """Save workflow to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            workflow_file = Path(f"workflow_{timestamp}.json")
            
            with open(workflow_file, 'w', encoding='utf-8') as f:
                json.dump(workflow_json, f, indent=2)
                
            return workflow_file
            
        except Exception as e:
            self.logger.error(f"Error saving workflow: {str(e)}")
            return None
            
    def parse_workflow_code(self, code: str) -> Dict:
        """Parse workflow code into JSON format"""
        try:
            # Create a local namespace to execute the code
            local_vars = {}
            exec(code, {}, local_vars)
            
            # Get the workflow JSON from the local variables
            workflow_json = local_vars.get("workflow_json", {})
            if not workflow_json:
                self.logger.error("No workflow_json found in code")
                return {}
                
            # Ensure the workflow JSON has the required structure
            if not isinstance(workflow_json, dict):
                self.logger.error("workflow_json is not a dictionary")
                return {}
                
            if "nodes" not in workflow_json or "connections" not in workflow_json:
                self.logger.error("workflow_json missing required fields (nodes, connections)")
                return {}
                
            return workflow_json
            
        except Exception as e:
            self.logger.error(f"Error parsing workflow code: {str(e)}")
            return {}

    def get_workflow_helper_methods(self) -> str:
        """Get available workflow helper methods and their parameters for autocoder prompts"""
        return """
Available N8nWorkflowHelper methods for creating workflows:

1. create_schedule_trigger(name: str, trigger_at_hour: int = 0, interval: str = "days")
   - Creates a schedule trigger node
   - Example: create_schedule_trigger("Daily Trigger", 9, "days")

2. create_openai_message(name: str, model: str, prompt: str, credentials_id: str = "KcAhGHqBrsmriXlY")
   - Creates an OpenAI node for text generation
   - Example: create_openai_message("Generate Text", "gpt-4", "Write a summary")

3. create_dropbox_list_folder(name: str, folder_path: str, credentials_id: str = "KcAhGHqBrsmriXlY")
   - Creates a Dropbox node to list folder contents
   - Example: create_dropbox_list_folder("List Files", "/sources")

4. create_dropbox_upload(name: str, folder_path: str, file_name: str, credentials_id: str = "KcAhGHqBrsmriXlY")
   - Creates a Dropbox node to upload files
   - Example: create_dropbox_upload("Upload File", "/deliverables", "output.txt")

5. create_send_email(name: str, to_email: str, subject: str, body: str, credentials_id: str = "JTbu1l5Wfqw1zrie")
   - Creates an email node to send messages
   - Example: create_send_email("Send Report", "user@example.com", "Daily Report", "Here's the report")

6. create_workflow(name: str, nodes: List[Dict], connections: Dict)
   - Creates a complete workflow with nodes and connections
   - Example: create_workflow("My Workflow", [node1, node2], {"node1": {"main": [["node2"]]}})

To use these methods:
1. Create nodes using the helper methods
2. Define connections between nodes
3. Create the workflow with create_workflow
4. Deploy using deploy_workflow
""" 