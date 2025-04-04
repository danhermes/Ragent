from typing import Dict, List, Optional
import json
from pathlib import Path
from datetime import datetime
from ...n8n.n8n_api_client import N8nApiClient
from ...n8n.config import N8nConfig

class N8nAdapter:
    """Adapter for n8n-specific functionality used by autocoder"""
    
    def __init__(self):
        self.config = N8nConfig()
        self.client = N8nApiClient(self.config)
        
    def get_nodes(self) -> Dict:
        """Get available n8n nodes"""
        try:
            return self.client.get_nodes()
        except Exception as e:
            self.logger.error(f"Error getting n8n nodes: {str(e)}")
            return {}
            
    def deploy_workflow(self, workflow_json: Dict) -> bool:
        """Deploy workflow to n8n"""
        try:
            return self.client.deploy_workflow(workflow_json)
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