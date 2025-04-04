from typing import Dict, List, Optional
import json
from pathlib import Path
from ..apis.autocode.autocode_api_client import AutocodeAPIClient
from ..apis.n8n.n8n_api_client import N8nApiClient

class WorkflowAdapter:
    """Adapter that uses autocode API to generate n8n workflows"""
    
    def __init__(self):
        self.autocode_client = AutocodeAPIClient()
        self.n8n_client = N8nApiClient()
        
    def generate_workflow(self, requirements: Dict, specifications: Dict) -> Optional[Path]:
        """Generate n8n workflow from requirements and specifications"""
        try:
            # Convert requirements and specs to code generation prompt
            prompt = self._create_code_prompt(requirements, specifications)
            
            # Generate workflow code using autocode API
            workflow_code = self.autocode_client.generate_code(prompt)
            
            # Convert generated code to n8n workflow JSON
            workflow_json = self._convert_to_n8n_format(workflow_code)
            
            # Save workflow to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            workflow_file = Path(f"workflow_{timestamp}.json")
            
            with open(workflow_file, 'w', encoding='utf-8') as f:
                json.dump(workflow_json, f, indent=2)
                
            return workflow_file
            
        except Exception as e:
            self.logger.error(f"Error generating workflow: {str(e)}")
            return None
            
    def _create_code_prompt(self, requirements: Dict, specifications: Dict) -> str:
        """Create prompt for autocode API"""
        return f"""Generate n8n workflow code based on these requirements and specifications:

Requirements:
{json.dumps(requirements, indent=2)}

Specifications:
{json.dumps(specifications, indent=2)}

The workflow should:
1. Use appropriate n8n nodes for each task
2. Handle data flow between nodes
3. Include error handling
4. Follow n8n best practices
5. Include comments explaining the workflow"""
        
    def _convert_to_n8n_format(self, code: str) -> Dict:
        """Convert generated code to n8n workflow JSON format"""
        # Parse the generated code to extract workflow structure
        # This is a placeholder - actual implementation would parse the code
        # and convert it to n8n's expected JSON format
        return {
            "name": "Generated Workflow",
            "nodes": [],
            "connections": {}
        }
        
    def deploy_workflow(self, workflow_file: Path) -> bool:
        """Deploy workflow to n8n"""
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow_json = json.load(f)
                
            # Deploy to n8n
            success = self.n8n_client.deploy_workflow(workflow_json)
            return success
            
        except Exception as e:
            self.logger.error(f"Error deploying workflow: {str(e)}")
            return False 