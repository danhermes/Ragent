from apis.yamlgen.agents.piper_agent import PiperAgent
from apis.yamlgen.agents.elias_agent import EliasAgent
from apis.yamlgen.modules.yaml_generator import YAMLGenerator
import yaml
from pathlib import Path
import logging
import json

class YAMLgenDispatcher:
    """Dispatcher for YAMLgen tasks. Coordinates Piper and Elias agents."""

    def __init__(self):
        self.piper = PiperAgent()
        self.elias = EliasAgent()

    def generate_yaml(
        self,
        input_path: str,
        tool: str,
        enhance: bool = False,
        output_path: str = None,
        verbose: bool = False
    ) -> dict:
        """
        Full YAML generation flow:
        1. Parse and organize input spec
        2. Optionally enhance spec
        3. Format YAML using YAMLGenerator
        4. Validate basic structure
        5. Save YAML to output path
        """
        if verbose:
            self.piper.verbose = True
            self.elias.verbose = True

        logging.info(f"Starting YAML generation for tool: {tool}")
        logging.info(f"Input path: {input_path}")
        logging.info(f"Enhance mode: {enhance}")
        logging.info(f"Output path: {output_path}")

        # Step 1: Parse input using Piper
        logging.info("Step 1: Parsing input with Piper")
        structured_spec = self.piper.parse_input(input_path)
        logging.info(f"Piper parsed spec: {json.dumps(structured_spec, indent=2)}")

        # Step 2: Optionally enhance with Elias
        if enhance:
            logging.info("Step 2: Enhancing spec with Elias")
            structured_spec = self.elias.enhance_spec(structured_spec)
            logging.info(f"Elias enhanced spec: {json.dumps(structured_spec, indent=2)}")

        # Step 3: Format YAML using YAMLGenerator
        logging.info("Step 3: Formatting YAML")
        generator = YAMLGenerator(structured_spec)
        method_name = f"generate_{tool}_yaml"
        logging.info(f"Method name: {method_name}")
        
        if not hasattr(generator, method_name):
            logging.error(f"Unsupported tool: {tool}")
            raise ValueError(f"Unsupported tool: {tool}")

        generate_method = getattr(generator, method_name)
        yaml_content = generate_method()
        logging.info(f"Generated YAML content: {json.dumps(yaml_content, indent=2)}")

        # Step 4: Validate basic YAML content
        logging.info("Step 4: Validating YAML content")
        if not yaml_content or not isinstance(yaml_content, dict):
            logging.error("Generated YAML is invalid or empty")
            raise ValueError("Generated YAML is invalid or empty.")

        # Step 5: Save YAML if output path provided
        if output_path:
            logging.info(f"Step 5: Saving YAML to {output_path}")
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(yaml_content, f, sort_keys=False)
            logging.info("YAML saved successfully")

        return yaml_content
