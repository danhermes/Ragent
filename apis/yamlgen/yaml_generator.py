import yaml
from typing import Dict, Any
from pathlib import Path

class YAMLGenerator:
    """Generates YAML files for LitLegos, n8n, AutoCoder, and Proof systems from a unified tech spec."""

    def __init__(self, tech_spec: Dict[str, Any]):
        self.spec = tech_spec

    def generate_litlegos_yaml(self) -> Dict[str, Any]:
        return {
            "title": self.spec.get("title", "Untitled"),
            "content_type": self.spec.get("content_type", "book"),
            "length": self.spec.get("length", "5 chapters"),
            "prompt": self.spec.get("prompt", "Write clearly and persuasively."),
            "style_profile": self.spec.get("style", "thoughtful and concise"),
            "narrative_rhythm": self.spec.get("narrative_rhythm", "confusion > clarity > empowerment"),
            "target_reader": self.spec.get("target_reader", "business leader"),
            "arc": self.spec.get("arc", "pedagogical progression"),
            "flavor": self.spec.get("flavor", "professional with spark"),
            "test_mode": self.spec.get("test_mode", False),
            "big_ideas": self.spec.get("big_ideas", []),
            "themes": self.spec.get("themes", []),
            "patterns": self.spec.get("patterns", []),
            "examples": self.spec.get("examples", []),
            "inserts": self.spec.get("inserts", []),
            "toc": self.spec.get("toc", [])
        }

    def generate_n8n_yaml(self) -> Dict[str, Any]:
        return {
            "workflow": {
                "name": self.spec.get("workflow_name", "Generated Workflow"),
                "settings": self.spec.get("settings", {"timezone": "UTC"}),
            },
            "nodes": self.spec.get("nodes", []),
            "connections": self.spec.get("connections", [])
        }

    def generate_autocoder_yaml(self) -> Dict[str, Any]:
        return {
            "project": self.spec.get("title", "Untitled Code Project"),
            "goal": self.spec.get("goal", "Generate reusable code modules."),
            "modules": self.spec.get("modules", []),
            "test_mode": self.spec.get("test_mode", False)
        }

    def generate_proof_yaml(self) -> Dict[str, Any]:
        return {
            "document_title": self.spec.get("title", "Untitled"),
            "purpose": self.spec.get("purpose", "Validate structure and logic."),
            "sections": self.spec.get("sections", []),
            "tone": self.spec.get("style", "clear and logical"),
        }

    def write_all(self, out_dir: str = "./generated_yamls") -> None:
        """Write all generated YAML files to disk."""
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        outputs = {
            "litlegos.yaml": self.generate_litlegos_yaml(),
            "n8n.yaml": self.generate_n8n_yaml(),
            "autocoder.yaml": self.generate_autocoder_yaml(),
            "proof.yaml": self.generate_proof_yaml(),
        }
        for filename, content in outputs.items():
            with open(Path(out_dir) / filename, "w") as f:
                yaml.dump(content, f, sort_keys=False)
