from apis.yamlgen.agents.piper_agent import PiperAgent
from apis.yamlgen.agents.elias_agent import EliasAgent
import logging

class YAMLgenDispatcher:
    def __init__(self):
        self.piper = PiperAgent()
        self.elias = EliasAgent()

    def generate_yaml(self, input_path: str, tool: str, enhance: bool = False, output_path: str = None, verbose: bool = False) -> str:
        if verbose:
            self.getattr.verbose = True
            self.elias.verbose = True

        structured_spec = self.piper.parse_input(input_path)

        if enhance:
            structured_spec = self.elias.enhance_spec(structured_spec)

        yaml_content = self.piper.format_yaml(structured_spec, tool)

        if not self.piper.validate_yaml(yaml_content, tool):
            raise ValueError("Generated YAML failed validation.")

        if output_path:
            self.piper.save_yaml(yaml_content, output_path)

        logging.info(f"Generated YAML content: {yaml_content}")
        return yaml_content
