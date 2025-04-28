from agents.base_agent import BaseAgent
from apis.yamlgen.modules.markdown_spec_parser import MarkdownSpecParser
from apis.yamlgen.modules.yaml_generator import YAMLGenerator
from apis.yamlgen.modules.n8n_field_mapping import TEMPLATE_FIELDS_N8N
import logging

class PiperAgent_v1(BaseAgent):
    """Piper Agent - Parses Markdown Automation Tech Spec into structured fields."""

    def parse_input(self, input_path: str) -> dict:
        """Parse a Markdown Tech Spec and organize it using template field mappings."""
        parser = MarkdownSpecParser(input_path)
        raw_sections = parser.load()
        organized_spec = self.organize_fields(raw_sections)
        logging.info(f"Parsed and organized input from {input_path}")
        return organized_spec

    def organize_fields(self, parsed_data: dict) -> dict:
        """Organize fields based on external template-driven mappings."""
        organized = {}
        for internal_key, md_heading in TEMPLATE_FIELDS_N8N.items():
            value = parsed_data.get(md_heading)
            organized[internal_key] = value
            logging.debug(f"Mapping '{md_heading}' -> '{internal_key}': {value}")
        
        logging.info("Organized fields into structured spec (template-driven).")
        return organized

    def format_yaml(self, organized_spec: dict, tool: str) -> dict:
        """Format the organized spec into YAML according to target tool."""
        generator = YAMLGenerator(organized_spec)
        method_name = f"generate_{tool}_yaml"
        if not hasattr(generator, method_name):
            raise ValueError(f"Unsupported tool: {tool}")
        generate_method = getattr(generator, method_name)
        yaml_output = generate_method()
        logging.info(f"Formatted spec into {tool} YAML")
        return yaml_output

    def validate_yaml(self, yaml_content: dict, tool: str) -> bool:
        """Validate the output YAML (basic checks)."""
        if not yaml_content:
            logging.error("Validation failed: Empty YAML content.")
            return False
        logging.info("Validation passed.")
        return True

    def save_yaml(self, yaml_content: dict, output_path: str):
        """Save the generated YAML to file."""
        import yaml
        from pathlib import Path
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, sort_keys=False)
        logging.info(f"Saved YAML output to {output_path}")
