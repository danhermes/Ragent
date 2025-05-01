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

#from apis.n8n.n8n_workflow_helper import N8nWorkflowHelper
#from apis.n8n.config import N8nConfig

class DevAdapter:
    """Adapter for dev-specific functionality used by ragers"""
    
    def __init__(self, logger=None):
        #self.config = N8nConfig()
        #self.workflow_helper = N8nWorkflowHelper(self.config)
        self.logger = logger or logging.getLogger("dev_adapter")
        
    # def get_nodes(self) -> Dict:
    #     """Get available n8n nodes"""
    #     try:
    #         return self.workflow_helper.get_nodes()
    #     except Exception as e:
    #         self.logger.error(f"Error getting n8n nodes: {str(e)}")
    #         return {}
            
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
        Below is the recommended high-level class/design diagram:

Controller  
Attributes: test_mode (bool), logger (Logger instance), prompt_manager (PromptManager instance), available_formats (list), prev_format (str)  
Methods: run_pipeline() (iterates over chapter definitions and coordinates generation), set_test_mode()

ChapterGenerator  
Attributes: chapter (e.g., “/chapter_1”), length (int), prompts (list of prompt strings), theme (str), available_formats (list), prev_format (str), format (selected template), logger (Logger instance), test_mode (bool)  
Methods: generate_prompt_stories() (returns a list of 150+ word narratives), generate_chapter() (creates complete chapter content), log_progress()

PromptManager  
Attributes: raw_prompt (dictionary as in the pipeline prompt)  
Methods: parse_pipeline_prompt() (extracts structured data from the prompt), generate_prompts(chapter, count) (returns required prompt list)

Logger  
Attributes: date_stamp (str), log_file (str), mode (production/test)  
Methods: setup_logging(), log(message)

Utility: TemplateSelector  
Function: select_template(prev_format, available_formats) → returns a new non-repeated format

The Controller instantiates Logger and PromptManager, then for each chapter definition it creates a ChapterGenerator by passing in the previous format (for memory tracking). The ChapterGenerator invokes TemplateSelector and PromptManager, logs activity via Logger, and writes the final markdown content including a “\newpage” command after each chapter.

""" 