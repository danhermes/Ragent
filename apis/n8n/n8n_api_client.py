import requests
import logging
import json
from typing import Dict, Any, Optional, List, Union
from .config import N8nConfig

logger = logging.getLogger(__name__)

class N8nApiClient:
    """Client for making requests to the n8n API"""
    
    def __init__(self, config: N8nConfig):
        """Initialize n8n API client
        
        Args:
            config: N8nConfig instance containing API configuration
        """
        self.base_url = config.base_url
        self.headers = config.headers
        self.logger = logging.getLogger(__name__)
        
        # API endpoints
        self.endpoints = {
            'workflows': '/api/v1/workflows',
            'nodes': '/api/v1/nodes',
            'credentials': '/api/v1/credentials',
            'webhooks': '/api/v1/webhooks',
            'executions': '/api/v1/executions'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make a request to the n8n API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Optional request data for POST/PUT
            
        Returns:
            Dict containing the API response
        """
        url = f"{self.base_url}{self.endpoints.get(endpoint, endpoint)}"
        
        try:
            # Log request details
            self.logger.info(f"Making {method} request to {url}")
            if data:
                self.logger.info(f"Request data: {json.dumps(data, indent=2)}")
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Log response details
            self.logger.info(f"Response status: {response.status_code}")
            self.logger.info(f"Response headers: {response.headers}")
            self.logger.info(f"Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making {method} request to n8n API endpoint {endpoint}: {str(e)}")
            if hasattr(e.response, 'text'):
                self.logger.error(f"Error response: {e.response.text}")
            raise

    # Workflow methods
    def get_workflows(self) -> Dict:
        """Get all workflows"""
        return self._make_request('GET', 'workflows')
    
    def get_workflow(self, workflow_id: str) -> Dict:
        """Get a specific workflow"""
        return self._make_request('GET', f'workflows/{workflow_id}')
    
    def create_workflow(self, workflow_data: Dict) -> Dict:
        """Create a new workflow"""
        return self._make_request('POST', 'workflows', workflow_data)
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict) -> Dict:
        """Update an existing workflow"""
        return self._make_request('PUT', f'workflows/{workflow_id}', workflow_data)
    
    def delete_workflow(self, workflow_id: str) -> Dict:
        """Delete a workflow"""
        return self._make_request('DELETE', f'workflows/{workflow_id}')
    
    def activate_workflow(self, workflow_id: str) -> Dict:
        """Activate a workflow"""
        return self._make_request('POST', f'workflows/{workflow_id}/activate')
    
    def deactivate_workflow(self, workflow_id: str) -> Dict:
        """Deactivate a workflow"""
        return self._make_request('POST', f'workflows/{workflow_id}/deactivate')

    # Node methods
    def get_nodes(self) -> Dict:
        """Get all nodes"""
        return self._make_request('GET', 'nodes')
    
    def get_node(self, node_id: str) -> Dict:
        """Get a specific node"""
        return self._make_request('GET', f'nodes/{node_id}')
    
    def create_node(self, node_data: Dict) -> Dict:
        """Create a new node"""
        return self._make_request('POST', 'nodes', node_data)
    
    def update_node(self, node_id: str, node_data: Dict) -> Dict:
        """Update an existing node"""
        return self._make_request('PUT', f'nodes/{node_id}', node_data)
    
    def delete_node(self, node_id: str) -> Dict:
        """Delete a node"""
        return self._make_request('DELETE', f'nodes/{node_id}')

    # Credential methods
    def get_credentials(self) -> Dict:
        """Get all credentials"""
        return self._make_request('GET', 'credentials')
    
    def get_credential(self, credential_id: str) -> Dict:
        """Get a specific credential"""
        return self._make_request('GET', f'credentials/{credential_id}')
    
    def create_credential(self, credential_data: Dict) -> Dict:
        """Create new credentials"""
        return self._make_request('POST', 'credentials', credential_data)
    
    def update_credential(self, credential_id: str, credential_data: Dict) -> Dict:
        """Update existing credentials"""
        return self._make_request('PUT', f'credentials/{credential_id}', credential_data)
    
    def delete_credential(self, credential_id: str) -> Dict:
        """Delete credentials"""
        return self._make_request('DELETE', f'credentials/{credential_id}')

    # Webhook methods
    def get_webhooks(self) -> Dict:
        """Get all webhooks"""
        return self._make_request('GET', 'webhooks')
    
    def get_webhook(self, webhook_id: str) -> Dict:
        """Get a specific webhook"""
        return self._make_request('GET', f'webhooks/{webhook_id}')
    
    def create_webhook(self, webhook_data: Dict) -> Dict:
        """Create a new webhook"""
        return self._make_request('POST', 'webhooks', webhook_data)
    
    def delete_webhook(self, webhook_id: str) -> Dict:
        """Delete a webhook"""
        return self._make_request('DELETE', f'webhooks/{webhook_id}')

    # Execution methods
    def get_executions(self) -> Dict:
        """Get all executions"""
        return self._make_request('GET', 'executions')
    
    def get_execution(self, execution_id: str) -> Dict:
        """Get a specific execution"""
        return self._make_request('GET', f'executions/{execution_id}')
    
    def delete_execution(self, execution_id: str) -> Dict:
        """Delete an execution"""
        return self._make_request('DELETE', f'executions/{execution_id}')
    
    def get_execution_data(self, execution_id: str) -> Dict:
        """Get execution data"""
        return self._make_request('GET', f'executions/{execution_id}/data') 