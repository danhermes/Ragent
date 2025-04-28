import json
from pathlib import Path
from agents.base_agent import BaseAgent
from apis.yamlgen.modules.markdown_spec_parser import MarkdownSpecParser
from apis.yamlgen.modules.yaml_generator import YAMLGenerator
from apis.yamlgen.modules.n8n_field_mapping import TEMPLATE_FIELDS_N8N
import logging

class PiperAgent(BaseAgent):
    """Piper Agent - Translates fuzzy Markdown into structured spec using GPT."""

    def __init__(self):
        super().__init__()

    def parse_input(self, input_path: str) -> dict:
        """Parse a Markdown Tech Spec into structured fields using GPT guidance."""
        raw_text = Path(input_path).read_text(encoding="utf-8")

        # Step 1: Build GPT prompt
        prompt = self.build_structuring_prompt(raw_text)

        # Step 2: Call GPT
        structured_json = self.get_chat_response(prompt)
        
        if not structured_json:
            raise ValueError("Empty response received from GPT")

        # Clean the response by removing markdown code block markers
        structured_json = structured_json.strip()
        if structured_json.startswith("```json"):
            structured_json = structured_json[7:]
        if structured_json.endswith("```"):
            structured_json = structured_json[:-3]
        structured_json = structured_json.strip()

        # Step 3: Parse JSON safely
        try:
            structured_spec = json.loads(structured_json)
            logging.info("Successfully parsed structured spec from GPT response.")
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse structured spec: {e}")
            logging.error(f"Raw GPT response: {structured_json}")
            raise ValueError("Invalid GPT response: could not parse JSON.")

        # Step 4: Validate basic fields
        self.validate_spec(structured_spec)

        return structured_spec

    def build_structuring_prompt(self, raw_text: str) -> str:
        """Construct a GPT prompt instructing it how to structure the spec."""
        #expected_fields = "\n".join(f"- {field}" for field in TEMPLATE_FIELDS_N8N.keys())
        expected_fields = "\n".join(
            f"- {internal_key} ({description})"
            for internal_key, description in TEMPLATE_FIELDS_N8N.items()
        )

        prompt = (
            "You are a JSON spec structuring assistant.\n\n"
            "Given the following messy Markdown document, extract and organize it into a clean JSON dictionary "
            "with these fields as keys:\n\n"
            f"{expected_fields}\n\n"
            "Each key must be present in the JSON. If information is missing for a key, use `null`.\n\n"
            "Markdown delimiters include but are not limited to:':','➔','-','\u2794'. Here is the Markdown document:\n\n"
            f"{raw_text}\n\n"
            "Output ONLY valid JSON."
        )
        return prompt

    def validate_spec(self, spec: dict):
        """Basic validation to ensure critical fields exist."""
        required_fields = ["workflow_name", "nodes", "connections"]
        for field in required_fields:
            if field not in spec or not spec[field]:
                self.log(f"Missing critical field in structured spec: {field}", level="warning")
