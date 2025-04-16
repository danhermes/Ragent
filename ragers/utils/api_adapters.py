import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

# Add the apis directory to the Python path
current_dir = Path(__file__).resolve().parent.parent
apis_dir = current_dir.parent / 'apis'
sys.path.append(str(apis_dir))

from apis.n8n.n8n_api_client import N8nApiClient
from apis.n8n.config import N8nConfig
from apis.proof.proof_API_client import ProofAPIClient

class N8nAPI:
    """Adapter for n8n workflow automation"""
    
    def __init__(self):
        self.logger = logging.getLogger("n8n_api")
        self.logger.setLevel(logging.INFO)
        n8n_config = N8nConfig()
        self.client = N8nApiClient(n8n_config)
        self.logger.info("Initialized n8n client")
    
    # Workflow methods
    def get_workflows(self) -> Dict[str, Any]:
        """Get all workflows"""
        self.logger.info("Getting all workflows")
        return self.client.get_workflows()
    
    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow by ID"""
        self.logger.info(f"Getting workflow: {workflow_id}")
        return self.client.get_workflow(workflow_id)
    
    def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new workflow"""
        self.logger.info("Creating new workflow")
        return self.client.create_workflow(workflow_data)
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update workflow by ID"""
        self.logger.info(f"Updating workflow: {workflow_id}")
        return self.client.update_workflow(workflow_id, workflow_data)
    
    def delete_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Delete workflow by ID"""
        self.logger.info(f"Deleting workflow: {workflow_id}")
        return self.client.delete_workflow(workflow_id)
    
    def activate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Activate workflow by ID"""
        self.logger.info(f"Activating workflow: {workflow_id}")
        return self.client.activate_workflow(workflow_id)
    
    def deactivate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Deactivate workflow by ID"""
        self.logger.info(f"Deactivating workflow: {workflow_id}")
        return self.client.deactivate_workflow(workflow_id)
    
    # Node methods
    def get_nodes(self) -> Dict[str, Any]:
        """Get all nodes"""
        self.logger.info("Getting all nodes")
        return self.client.get_nodes()
    
    def get_node(self, node_id: str) -> Dict[str, Any]:
        """Get node by ID"""
        self.logger.info(f"Getting node: {node_id}")
        return self.client.get_node(node_id)
    
    def create_node(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new node"""
        self.logger.info("Creating new node")
        return self.client.create_node(node_data)
    
    def update_node(self, node_id: str, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update node by ID"""
        self.logger.info(f"Updating node: {node_id}")
        return self.client.update_node(node_id, node_data)
    
    def delete_node(self, node_id: str) -> Dict[str, Any]:
        """Delete node by ID"""
        self.logger.info(f"Deleting node: {node_id}")
        return self.client.delete_node(node_id)
    
    # Credential methods
    def get_credentials(self) -> Dict[str, Any]:
        """Get all credentials"""
        self.logger.info("Getting all credentials")
        return self.client.get_credentials()
    
    def get_credential(self, credential_id: str) -> Dict[str, Any]:
        """Get credential by ID"""
        self.logger.info(f"Getting credential: {credential_id}")
        return self.client.get_credential(credential_id)
    
    def create_credential(self, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new credential"""
        self.logger.info("Creating new credential")
        return self.client.create_credential(credential_data)
    
    def update_credential(self, credential_id: str, credential_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update credential by ID"""
        self.logger.info(f"Updating credential: {credential_id}")
        return self.client.update_credential(credential_id, credential_data)
    
    def delete_credential(self, credential_id: str) -> Dict[str, Any]:
        """Delete credential by ID"""
        self.logger.info(f"Deleting credential: {credential_id}")
        return self.client.delete_credential(credential_id)
    
    # Webhook methods
    def get_webhooks(self) -> Dict[str, Any]:
        """Get all webhooks"""
        self.logger.info("Getting all webhooks")
        return self.client.get_webhooks()
    
    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Get webhook by ID"""
        self.logger.info(f"Getting webhook: {webhook_id}")
        return self.client.get_webhook(webhook_id)
    
    def create_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new webhook"""
        self.logger.info("Creating new webhook")
        return self.client.create_webhook(webhook_data)
    
    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete webhook by ID"""
        self.logger.info(f"Deleting webhook: {webhook_id}")
        return self.client.delete_webhook(webhook_id)
    
    # Execution methods
    def get_executions(self) -> Dict[str, Any]:
        """Get all executions"""
        self.logger.info("Getting all executions")
        return self.client.get_executions()
    
    def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """Get execution by ID"""
        self.logger.info(f"Getting execution: {execution_id}")
        return self.client.get_execution(execution_id)
    
    def delete_execution(self, execution_id: str) -> Dict[str, Any]:
        """Delete execution by ID"""
        self.logger.info(f"Deleting execution: {execution_id}")
        return self.client.delete_execution(execution_id)
    
    def get_execution_data(self, execution_id: str) -> Dict[str, Any]:
        """Get execution data by ID"""
        self.logger.info(f"Getting execution data: {execution_id}")
        return self.client.get_execution_data(execution_id)

class LanguageToolsAPI:
    """Adapter for LanguageTool text proofreading"""
    
    def __init__(self):
        self.logger = logging.getLogger("language_tools_api")
        self.logger.setLevel(logging.INFO)
        self.client = ProofAPIClient()
        self.logger.info("Initialized proof client")
    
    def check_text(self, text: str) -> Dict[str, Any]:
        """Check text for grammar/style issues"""
        self.logger.info(f"Checking text: {text[:50]}...")
        return self.client.check_text(text)
    
    def apply_corrections(self, text: str, matches: Dict[str, Any]) -> str:
        """Apply corrections to text"""
        self.logger.info("Applying corrections to text")
        return self.client.apply_corrections(text, matches)

class RagersAPIAdapter:
    """Main adapter providing access to all API services"""
    
    def __init__(self):
        self.logger = logging.getLogger("ragers_api_adapter")
        self.logger.setLevel(logging.INFO)
        self.n8n = N8nAPI()
        self.language_tools = LanguageToolsAPI()
        self.logger.info("Initialized all API services") 