import yaml
from pathlib import Path
from typing import Dict, Any, Union

class YamlParser:
    """Parses a generic tech spec file (.yaml or .json-like .goal) into a unified dictionary."""

    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)
        self.spec: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        if self.path.suffix in [".yaml", ".yml"]:
            with open(self.path, "r") as f:
                self.spec = yaml.safe_load(f)
        elif self.path.suffix == ".goal" or self.path.suffix == ".json":
            with open(self.path, "r") as f:
                content = f.read()
                try:
                    self.spec = yaml.safe_load(content)
                except yaml.YAMLError:
                    raise ValueError("Could not parse file. Ensure it's valid YAML or JSON.")
        else:
            raise ValueError("Unsupported file type. Only .yaml, .yml, .goal, or .json are allowed.")
        return self.spec

    def to_unified_spec(self) -> Dict[str, Any]:
        unified = {
            "title": self.spec.get("title") or self.spec.get("project"),
            "prompt": self.spec.get("prompt"),
            "style": self.spec.get("style_profile") or self.spec.get("style"),
            "big_ideas": self.spec.get("big_ideas", []),
            "themes": self.spec.get("themes", []),
            "patterns": self.spec.get("patterns", []),
            "examples": self.spec.get("examples", []),
            "inserts": self.spec.get("inserts", []),
            "toc": self.spec.get("toc", []),
            "length": self.spec.get("length"),
            "arc": self.spec.get("arc"),
            "flavor": self.spec.get("flavor"),
            "target_reader": self.spec.get("target_reader"),
            "narrative_rhythm": self.spec.get("narrative_rhythm"),
            "test_mode": self.spec.get("test_mode", False),

            # n8n specific
            "workflow_name": self.spec.get("workflow", {}).get("name") or self.spec.get("workflow_name"),
            "settings": self.spec.get("workflow", {}).get("settings") or self.spec.get("settings"),
            "nodes": self.spec.get("nodes", []),
            "connections": self.spec.get("connections", []),

            # autocoder specific
            "goal": self.spec.get("goal"),
            "modules": self.spec.get("modules", []),

            # proof specific
            "purpose": self.spec.get("purpose"),
            "sections": self.spec.get("sections", []),
        }
        return unified 