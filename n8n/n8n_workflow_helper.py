import json
from typing import Dict, Any, Optional, List, Union
import logging
import uuid
from n8n_api_client import N8nApiClient
from config import N8nConfig

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class N8nWorkflowHelper:
    """Helper class for creating and managing n8n workflows"""
    
    def __init__(self, config: Optional[N8nConfig] = None):
        """Initialize n8n API connection
        
        Args:
            config: Optional N8nConfig instance. If not provided, a new one will be created.
        """
        logger.debug("Initializing N8nWorkflowHelper")
        self.config = config or N8nConfig()
        self.api_client = N8nApiClient(self.config)
        self.logger = logging.getLogger(__name__)
        logger.debug(f"Initialized with config: {self.config.__dict__}")
    
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
        logger.debug(f"Creating base node: {name} of type {type}")
        logger.debug(f"Parameters: {json.dumps(parameters, indent=2)}")
        if credentials:
            logger.debug(f"Credentials: {json.dumps(credentials, indent=2)}")
        
        # Clean up parameters to remove None values and duplicates
        clean_params = {}
        for key, value in parameters.items():
            if value is not None and not key.startswith('webhookAuthentication'):
                clean_params[key] = value
        
        logger.debug(f"Cleaned parameters: {json.dumps(clean_params, indent=2)}")
        
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
            
        logger.debug(f"Created node: {json.dumps(node, indent=2)}")
        return node
    
    def create_schedule_trigger(self, name: str, trigger_at_hour: int = 0, 
                              interval: str = "days") -> Dict[str, Any]:
        """Create a Schedule Trigger node"""
        logger.debug(f"Creating schedule trigger: {name} at {trigger_at_hour}:00 {interval}")
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
        logger.debug(f"Schedule parameters: {json.dumps(parameters, indent=2)}")
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.scheduleTrigger",
            position=[-980, -260],
            parameters=parameters
        )
    
    def create_openai_message(self, name: str, model: str, prompt: str,
                            credentials_id: str = "KcAhGHqBrsmriXlY") -> Dict[str, Any]:
        """Create an OpenAI node"""
        logger.debug(f"Creating OpenAI node: {name} with model {model}")
        logger.debug(f"Prompt: {prompt}")
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
        
        logger.debug(f"OpenAI parameters: {json.dumps(parameters, indent=2)}")
        logger.debug(f"OpenAI credentials: {json.dumps(credentials, indent=2)}")
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.openAi",
            position=[-660, -260],
            parameters=parameters,
            credentials=credentials
        )
    
    def create_dropbox_list_folder(self, name: str, folder_path: str,
                                 credentials_id: str = "KcAhGHqBrsmriXlY") -> Dict[str, Any]:
        """Create a Dropbox List Folder node"""
        logger.debug(f"Creating Dropbox List Folder node: {name}")
        logger.debug(f"Folder path: {folder_path}")
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
        
        logger.debug(f"Dropbox parameters: {json.dumps(parameters, indent=2)}")
        logger.debug(f"Dropbox credentials: {json.dumps(credentials, indent=2)}")
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.dropbox",
            position=[-820, -260],
            parameters=parameters,
            credentials=credentials
        )
    
    def create_dropbox_upload(self, name: str, folder_path: str, file_name: str,
                            credentials_id: str = "KcAhGHqBrsmriXlY") -> Dict[str, Any]:
        """Create a Dropbox Upload File node"""
        logger.debug(f"Creating Dropbox Upload node: {name}")
        logger.debug(f"Upload path: {folder_path}/{file_name}")
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
        
        logger.debug(f"Dropbox upload parameters: {json.dumps(parameters, indent=2)}")
        logger.debug(f"Dropbox credentials: {json.dumps(credentials, indent=2)}")
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.dropbox",
            position=[-440, -260],
            parameters=parameters,
            credentials=credentials
        )
    
    def create_send_email(self, name: str, to_email: str, subject: str, body: str,
                         credentials_id: str = "JTbu1l5Wfqw1zrie") -> Dict[str, Any]:
        """Create a Send Email node"""
        logger.debug(f"Creating Email node: {name}")
        logger.debug(f"To: {to_email}")
        logger.debug(f"Subject: {subject}")
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
        
        logger.debug(f"Email parameters: {json.dumps(parameters, indent=2)}")
        logger.debug(f"Email credentials: {json.dumps(credentials, indent=2)}")
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.emailSend",
            position=[-300, -260],
            parameters=parameters,
            credentials=credentials
        )
    
    def create_extract_xlsx(self, name: str, sheet_name: str, range: str) -> Dict[str, Any]:
        """Create a Spreadsheet File node for reading XLSX"""
        logger.debug(f"Creating Extract XLSX node: {name}")
        logger.debug(f"Sheet: {sheet_name}, Range: {range}")
        parameters = {
            "operation": "read",
            "fileFormat": "xlsx",
            "options": {
                "range": range,
                "sheet": sheet_name
            }
        }
        
        logger.debug(f"XLSX parameters: {json.dumps(parameters, indent=2)}")
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.spreadsheetFile",
            position=[-1040, -260],
            parameters=parameters
        )
    
    def create_filter(self, name: str, conditions: List[Dict[str, Any]], 
                     combinator: str = "and") -> Dict[str, Any]:
        """Create a Filter node"""
        logger.debug(f"Creating Filter node: {name}")
        logger.debug(f"Conditions: {json.dumps(conditions, indent=2)}")
        logger.debug(f"Combinator: {combinator}")
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
        
        logger.debug(f"Filter parameters: {json.dumps(parameters, indent=2)}")
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.filter",
            position=[-820, -260],
            parameters=parameters
        )
    
    def create_edit_fields(self, name: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Create an Edit Fields node"""
        logger.debug(f"Creating Edit Fields node: {name}")
        logger.debug(f"Fields to edit: {json.dumps(fields, indent=2)}")
        parameters = {
            "fields": fields
        }
        
        logger.debug(f"Edit Fields parameters: {json.dumps(parameters, indent=2)}")
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.editFields",
            position=[-440, -260],
            parameters=parameters
        )
    
    def create_convert_to_xlsx(self, name: str, sheet_name: str) -> Dict[str, Any]:
        """Create a Spreadsheet File node for writing XLSX"""
        logger.debug(f"Creating Convert to XLSX node: {name}")
        logger.debug(f"Sheet name: {sheet_name}")
        parameters = {
            "operation": "write",
            "fileFormat": "xlsx",
            "options": {
                "sheet": sheet_name
            }
        }
        
        logger.debug(f"Convert XLSX parameters: {json.dumps(parameters, indent=2)}")
        
        return self._create_node_base(
            name=name,
            type="n8n-nodes-base.spreadsheetFile",
            position=[-1040, -260],
            parameters=parameters
        )
    
    def connect_nodes(self, from_node: str, to_node: str) -> Dict[str, Any]:
        """Connect two nodes in the workflow"""
        logger.debug(f"Creating connection from {from_node} to {to_node}")
        connection = {
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
        logger.debug(f"Connection data: {json.dumps(connection, indent=2)}")
        return connection
    
    def create_workflow(self, name: str, nodes: List[Dict[str, Any]], 
                       connections: Dict[str, Any]) -> Dict[str, Any]:
        """Create a complete workflow with nodes and connections"""
        logger.debug(f"Creating workflow: {name}")
        logger.debug(f"Number of nodes: {len(nodes)}")
        logger.debug(f"Number of connections: {len(connections)}")
        
        # Create a mapping of node names to their IDs
        node_id_map = {node["name"]: node["id"] for node in nodes}
        logger.debug(f"Node ID mapping: {json.dumps(node_id_map, indent=2)}")
        
        # Update connections to use node IDs instead of names
        updated_connections = {}
        for from_name, connection_data in connections.items():
            from_id = node_id_map.get(from_name)
            if not from_id:
                logger.error(f"Node name '{from_name}' not found in nodes list")
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
        
        logger.debug(f"Updated connections: {json.dumps(updated_connections, indent=2)}")
        
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
        
        logger.debug(f"Final workflow data: {json.dumps(workflow_data, indent=2)}")
        return self.api_client.create_workflow(workflow_data) 