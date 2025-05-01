from typing import Dict
from pathlib import Path
import re
import logging

class MarkdownSpecParser:
    """Parses a Markdown Automation Tech Spec into a structured section dictionary."""

    def __init__(self, path: str):
        self.path = Path(path)
        self.sections: Dict[str, str] = {}

    def _clean_heading(self, heading: str) -> str:
        """Clean a heading by removing emojis and extra formatting."""
        # Remove emojis (any non-ASCII characters)
        heading = re.sub(r'[^\x00-\x7F]+', '', heading)
        # Remove extra formatting like bold/italic markers
        heading = heading.replace('**', '').replace('__', '').replace('*', '').replace('_', '')
        # Normalize whitespace
        heading = ' '.join(heading.split())
        return heading.strip()

    def _parse_heading(self, line: str) -> str:
        """Parse a markdown heading line into a clean section name."""
        # Remove leading # and whitespace
        heading = re.sub(r'^#+\s*', '', line)
        return self._clean_heading(heading)

    def _parse_node_entry(self, entry: str) -> dict:
        """Parse a node entry from the Markdown list format.
        Format: - Node Name: nodeType - Description
        """
        try:
            # Remove leading dash and whitespace
            entry = entry.lstrip("-").strip()
            
            # Split into name and rest
            if ":" in entry:
                node_name, rest = entry.split(":", 1)
                node_name = node_name.strip()
                
                # Extract node type from the rest
                if "-" in rest:
                    node_type, _ = rest.split("-", 1)
                    node_type = node_type.strip()
                else:
                    node_type = rest.strip()
                
                return {
                    "name": node_name,
                    "type": node_type
                }
        except Exception as e:
            logging.error(f"Error parsing node entry: {entry} ({e})")
            return None

    def load(self) -> Dict[str, str]:
        current_heading = None
        content = {}
        
        try:
            with self.path.open("r", encoding="utf-8") as file:
                for line in file:
                    line = line.rstrip()
                    
                    # Check if line is a heading
                    if line.startswith('#'):
                        current_heading = self._parse_heading(line)
                        if current_heading:
                            content[current_heading] = []
                        continue
                    
                    # Skip empty lines
                    if not line.strip():
                        continue
                    
                    # Process content under current heading
                    if current_heading:
                        if current_heading == "Nodes":
                            # Parse node entry into structured format
                            node_entry = self._parse_node_entry(line)
                            if node_entry:
                                content[current_heading].append(node_entry)
                        else:
                            content[current_heading].append(line)
            
            # Convert lists to strings for non-Node sections
            for key in content:
                if key != "Nodes":
                    content[key] = "\n".join(content[key])
            
            return content
            
        except Exception as e:
            logging.error(f"Error loading markdown spec: {e}")
            return {}
