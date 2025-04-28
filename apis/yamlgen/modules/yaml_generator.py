import yaml
from typing import Dict, Any
from pathlib import Path

class YAMLGenerator:
    """Generates YAML files for LitLegos, n8n, AutoCoder, and Proof systems from a structured spec."""

    def __init__(self, structured_spec: Dict[str, Any]):
        self.spec = structured_spec

    def generate_n8n_yaml(self) -> Dict[str, Any]:
        """Generate n8n-compatible YAML format from structured spec."""
        nodes = self._build_nodes()
        connections = self._build_connections(nodes)

        return {
            "workflow": {
                "name": self.spec.get("workflow_name", "Generated Workflow"),
                "settings": self._build_settings()
            },
            "nodes": nodes,
            "connections": connections
        }

    def _build_nodes(self) -> list:
        """Build list of n8n nodes based on core_nodes field."""
        node_list = []
        for idx, entry in enumerate(self.spec.get("core_nodes", [])):
            try:
                node_name, rest = entry.split(":", 1)
                node_type, _purpose = rest.strip().split("-", 1)
                node = {
                    "name": node_name.strip(),
                    "type": node_type.strip(),
                    "params": {},  # GPT or Templates can fill this later
                    "position": [idx * 200, 0]  # Simple left-to-right positioning
                }
                node_list.append(node)
            except Exception as e:
                print(f"⚠️ Error parsing node entry: {entry} ({e})")
        return node_list

    def _build_connections(self, nodes: list) -> list:
        """Build node-to-node connections."""
        node_names = {node["name"]: idx for idx, node in enumerate(nodes)}
        connections = []
        for connection in self.spec.get("connections", []):
            try:
                from_node, to_node = connection.split("➔")
                from_node = from_node.strip()
                to_node = to_node.strip()
                if from_node in node_names and to_node in node_names:
                    connections.append({
                        "from": from_node,
                        "to": to_node
                    })
                else:
                    print(f"⚠️ Invalid connection nodes: {from_node} ➔ {to_node}")
            except Exception as e:
                print(f"⚠️ Error parsing connection entry: {connection} ({e})")
        return connections

    def _build_settings(self) -> dict:
        """Build workflow settings block."""
        settings = {}
        for setting in self.spec.get("workflow_settings", []):
            try:
                setting_name, value = setting.split(":", 1)
                settings[setting_name.strip()] = value.strip()
            except Exception as e:
                print(f"⚠️ Error parsing workflow setting: {setting} ({e})")
        if "timezone" not in settings:
            settings["timezone"] = "UTC"  # Default fallback
        return settings

    # Other generators (autocoder,
