import yaml
from typing import Dict, Any
from pathlib import Path
import json
import logging
class YAMLGenerator:
    """Generates YAML files for LitLegos, n8n, AutoCoder, and Proof systems from a structured spec."""

    def __init__(self, structured_spec: Dict[str, Any]):
        self.spec = structured_spec

    def generate_n8n_yaml(self) -> Dict[str, Any]:
        """Generate n8n-compatible YAML format from structured spec."""
        nodes = self._build_nodes()
        connections = self._build_connections(nodes)
        logging.info(f"Nodes: {nodes[:20]}")
        return {
            "workflow": {
                "name": self.spec.get("workflow_name", "Generated Workflow"),
                "settings": self._build_settings()
            },
            "nodes": nodes,
            "connections": connections
        }

    def _build_nodes(self) -> list:
        """Build list of n8n nodes based on nodes field."""
        node_list = []
        nodes = self.spec.get("nodes", [])
        logging.info(f"Building nodes: {nodes[:20]}")
        for idx, entry in enumerate(nodes):
            logging.info(f"Building node: {entry.get('node_name', '')}")
            try:
                if isinstance(entry, dict):
                    # Map from enhanced spec format to our YAML format
                    node = {
                        "node_name": entry.get("node_name", ""),
                        "node_type": entry.get("node_type", ""),
                        "description": entry.get("description", "")#,
                        #"params": entry.get("parameters", ""),
                    }
                    node_list.append(node)
                elif isinstance(entry, str):
                    # Format: "Node Name: nodeType - Description"
                    parts = entry.split(":", 1)
                    if len(parts) != 2:
                        print(f"⚠️ Invalid node entry format: {entry}")
                        continue
                        
                    node_name = parts[0].strip()
                    rest = parts[1].strip()

                    # Extract node type and description
                    if " - " in rest:
                        node_type, description = rest.split(" - ", 1)
                        node_type = node_type.strip()
                        description = description.strip()
                    else:
                        node_type = rest.strip()
                        description = ""
                        
                    node = {
                        "node_name": node_name,
                        "node_type": node_type,
                        "description": description,
                        "params": {}
                    }
                    node_list.append(node)
            except Exception as e:
                print(f"⚠️ Error parsing node entry: {entry} ({e})")
        return node_list

    def _build_connections(self, nodes: list) -> list:
        """Build node-to-node connections."""
        node_names = {node["node_name"]: idx for idx, node in enumerate(nodes)}
        connections = []
        
        # Get connections list
        connection_entries = self.spec.get("connections", [])
        logging.info(f"Building connections: {connection_entries[:20]}")
        for connection in connection_entries:
            try:
                if isinstance(connection, str):
                    # Format: "Source Node ➔ Target Node"
                    source, target = connection.split(" ➔ ")
                    source = source.strip()
                    target = target.strip()
                else:
                    # Dictionary format
                    source = connection.get("source_node", "")
                    target = connection.get("target_node", "")
                    
                if source in node_names and target in node_names:
                    connections.append({
                        "source_node": source,
                        "target_node": target
                    })
                else:
                    print(f"⚠️ Invalid connection nodes: {source} -> {target}")
            except Exception as e:
                print(f"⚠️ Error parsing connection entry: {connection} ({e})")
        return connections

    def _build_settings(self) -> dict:
        """Build workflow settings block."""
        settings = {}
        workflow_settings = self.spec.get("workflow_settings", [])
        if workflow_settings is None:
            workflow_settings = []
            
        for setting in workflow_settings:
            try:
                if isinstance(setting, str):
                    # Format: "key: value" or just "key"
                    if ":" in setting:
                        setting_name, value = setting.split(":", 1)
                        settings[setting_name.strip()] = value.strip()
                    else:
                        # If no value provided, use True as default
                        settings[setting.strip()] = True
                elif isinstance(setting, dict):
                    # Already in dictionary format
                    settings.update(setting)
            except Exception as e:
                print(f"⚠️ Error parsing workflow setting: {setting} ({e})")
        if "timezone" not in settings:
            settings["timezone"] = "UTC"  # Default fallback
        return settings

    # Other generators (autocoder,
