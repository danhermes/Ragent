import json
from typing import Dict, Any, Optional, List, Union
import logging
import uuid
from n8n_api_client import N8nApiClient
from config import N8nConfig

logger = logging.getLogger(__name__)

class N8nWorkflowHelper:
    """Helper class for creating and managing n8n workflows"""
    
    def __init__(self, config: Optional[N8nConfig] = None):
        """Initialize n8n API connection
        
        Args:
            config: Optional N8nConfig instance. If not provided, a new one will be created.
        """
        self.config = config or N8nConfig()
        self.api_client = N8nApiClient(self.config)
        self.logger = logging.getLogger(__name__)
    
    def _create_node_base(self, name: str, type: str, position: List[int], parameters: Dict[str, Any], 
                         credentials: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create base node structure
        
        Args:
            name: Node name
            type: Node type (e.g., 'n8n-nodes-base.scheduleTrigger')
            position: [x, y] coordinates for UI layout
            parameters: Node parameters
            credentials: Optional credentials configuration
            
        Returns:
            Dict containing the complete node structure
        """
        # Clean up parameters to remove None values and duplicates
        clean_params = {}
        for key, value in parameters.items():
            if value is not None and not key.startswith('webhookAuthentication'):
                clean_params[key] = value
        
        node = {
            "parameters": clean_params,
            "type": type,
            "typeVersion": 1.2,  # Default to latest version
            "position": position,
            "id": str(uuid.uuid4()),
            "name": name
        }
        
        if credentials:
            node["credentials"] = credentials
            
        return node
    
    def create_schedule_trigger(self, name: str, trigger_at_hour: int = 0, 
                              interval: str = "days") -> Dict[str, Any]:
        """Create a Schedule Trigger node
        
        Args:
            name: Node name
            trigger_at_hour: Hour of day to trigger (0-23)
            interval: Trigger interval (days, weeks, months)
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "rule": {
                "interval": [
                    {
                        "field": interval,
                        "triggerAtHour": trigger_at_hour
                    }
                ]
            }
        }
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.scheduleTrigger",
            position=[-980, -260],
            parameters=parameters
        )
    
    def create_openai_message(self, name: str, model: str, prompt: str,
                            credentials_id: str = "KcAhGHqBrsmriXlY") -> Dict[str, Any]:
        """Create an OpenAI node
        
        Args:
            name: Node name
            model: Model to use (e.g., gpt-4)
            prompt: Prompt text
            credentials_id: ID of the OpenAI credentials
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "authentication": "apiKey",
            "model": model,
            "prompt": prompt,
            "options": {
                "temperature": 0.7,
                "maxTokens": 2000
            }
        }
        
        credentials = {
            "openAiApi": {
                "id": credentials_id,
                "name": "OpenAI account"
            }
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.openAi",
            position=[-660, -260],
            parameters=parameters,
            credentials=credentials
        )
    
    def create_dropbox_list_folder(self, name: str, folder_path: str,
                                 credentials_id: str = "KcAhGHqBrsmriXlY") -> Dict[str, Any]:
        """Create a Dropbox List Folder node
        
        Args:
            name: Node name
            folder_path: Path to the folder to list
            credentials_id: ID of the Dropbox credentials
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "operation": "list",
            "path": folder_path,
            "limit": 100,
            "options": {}
        }
        
        credentials = {
            "dropboxApi": {
                "id": credentials_id,
                "name": "Dropbox account"
            }
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.dropbox",
            position=[-820, -260],
            parameters=parameters,
            credentials=credentials
        )
    
    def create_dropbox_upload(self, name: str, folder_path: str, file_name: str,
                            credentials_id: str = "KcAhGHqBrsmriXlY") -> Dict[str, Any]:
        """Create a Dropbox Upload File node
        
        Args:
            name: Node name
            folder_path: Path to upload to
            file_name: Name of the file to upload
            credentials_id: ID of the Dropbox credentials
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "operation": "upload",
            "path": folder_path + "/" + file_name,
            "binary": True,
            "options": {}
        }
        
        credentials = {
            "dropboxApi": {
                "id": credentials_id,
                "name": "Dropbox account"
            }
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.dropbox",
            position=[-440, -260],
            parameters=parameters,
            credentials=credentials
        )
    
    def create_send_email(self, name: str, to_email: str, subject: str, body: str,
                         credentials_id: str = "JTbu1l5Wfqw1zrie") -> Dict[str, Any]:
        """Create a Send Email node
        
        Args:
            name: Node name
            to_email: Recipient email address
            subject: Email subject
            body: Email body text
            credentials_id: ID of the SMTP credentials
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "fromEmail": "dan@lexicon.systems",
            "to": to_email,
            "subject": subject,
            "text": body,
            "options": {}
        }
        
        credentials = {
            "smtp": {
                "id": credentials_id,
                "name": "SMTP account"
            }
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.emailSend",
            position=[-300, -260],
            parameters=parameters,
            credentials=credentials
        )
    
    def create_extract_xlsx(self, name: str, sheet_name: str, range: str) -> Dict[str, Any]:
        """Create a Spreadsheet File node for reading XLSX
        
        Args:
            name: Node name
            sheet_name: Name of the sheet to extract from
            range: Excel range to extract (e.g., 'A1:B10')
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "operation": "read",
            "fileFormat": "xlsx",
            "options": {
                "range": range,
                "sheet": sheet_name
            }
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.spreadsheetFile",
            position=[-1040, -260],
            parameters=parameters
        )
    
    def create_filter(self, name: str, conditions: List[Dict[str, Any]], 
                     combinator: str = "and") -> Dict[str, Any]:
        """Create a Filter node
        
        Args:
            name: Node name
            conditions: List of filter conditions
            combinator: How to combine conditions (and/or)
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "loose",
                    "version": 2
                },
                "conditions": conditions,
                "combinator": combinator
            },
            "looseTypeValidation": True,
            "options": {}
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.filter",
            position=[-820, -260],
            parameters=parameters
        )
    
    def create_if(self, name: str, conditions: List[Dict[str, Any]], 
                  combinator: str = "and") -> Dict[str, Any]:
        """Create an If node
        
        Args:
            name: Node name
            conditions: List of if conditions
            combinator: How to combine conditions (and/or)
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "conditions": {
                "conditions": conditions,
                "combinator": combinator
            }
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.if",
            position=[-620, -260],
            parameters=parameters
        )
    
    def create_edit_fields(self, name: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Create an Edit Fields node
        
        Args:
            name: Node name
            fields: Fields to edit
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "fields": fields
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.editFields",
            position=[-440, -260],
            parameters=parameters
        )
    
    def create_convert_to_xlsx(self, name: str, sheet_name: str) -> Dict[str, Any]:
        """Create a Spreadsheet File node for writing XLSX
        
        Args:
            name: Node name
            sheet_name: Name of the sheet to write to
            
        Returns:
            Dict containing the complete node structure
        """
        parameters = {
            "operation": "write",
            "fileFormat": "xlsx",
            "options": {
                "sheet": sheet_name
            }
        }
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.spreadsheetFile",
            position=[-1040, -260],
            parameters=parameters
        )
    
    def connect_nodes(self, from_node: str, to_node: str) -> Dict[str, Any]:
        """Connect two nodes in the workflow
        
        Args:
            from_node: Name of the source node
            to_node: Name of the target node
            
        Returns:
            Dict containing the connection data
        """
        return {
            from_node: {
                "main": [
                    [
                        {
                            "node": to_node,
                            "type": "main"
                        }
                    ]
                ]
            }
        }
    
    def create_workflow(self, name: str, nodes: List[Dict[str, Any]], 
                       connections: Dict[str, Any]) -> Dict[str, Any]:
        """Create a complete workflow with nodes and connections
        
        Args:
            name: Workflow name
            nodes: List of node definitions
            connections: Dictionary of node connections
            
        Returns:
            Dict containing the complete workflow definition
        """
        # Create a mapping of node names to their IDs
        node_id_map = {node["name"]: node["id"] for node in nodes}
        
        # Update connections to use node IDs instead of names
        updated_connections = {}
        for from_name, connection_data in connections.items():
            from_id = node_id_map.get(from_name)
            if not from_id:
                raise ValueError(f"Node name '{from_name}' not found in nodes list")
                
            updated_connections[from_id] = {
                "main": [
                    [
                        {
                            "node": node_id_map.get(conn["node"]),
                            "type": conn["type"]
                        }
                        for conn in conn_list
                    ]
                    for conn_list in connection_data["main"]
                ]
            }
        
        workflow_data = {
            "name": name,
            "nodes": nodes,
            "connections": updated_connections,
            "settings": {
                "saveExecutionProgress": True,
                "saveManualExecutions": True,
                "saveDataErrorExecution": "all",
                "saveDataSuccessExecution": "all",
                "executionTimeout": 3600,
                "timezone": "UTC"
            }
        }
        return self.api_client.create_workflow(workflow_data) 