
from agents.base_agent import WorkerAgent
import logging
class EliasAgent(WorkerAgent):
    def __init__(self):
        super().__init__()

    def enhance_spec(self, structured_spec: dict) -> dict:
        logging.info("Enhancing spec via OpenAI.")
        prompt = self.build_enhancement_prompt(structured_spec)
        enhanced_response = self.get_chat_response(prompt)
        enhanced_spec = self.parse_response(enhanced_response, structured_spec)
        logging.info("Enhancement complete.")
        return enhanced_spec

    def build_enhancement_prompt(self, structured_spec: dict) -> str:
        prompt = (
            "You are a workflow designer expert.\n"
            "Enhance this automation spec by:\n"
            "- Proposing additional nodes if missing\n"
            "- Clarifying vague steps\n"
            "- Strengthening connections and logic\n\n"
            f"Here is the current structured spec:\n{structured_spec}\n\n"
            "Return the improved spec in JSON format."
        )
        return prompt

    def parse_response(self, gpt_response: str, original_spec: dict) -> dict:
        import json
        try:
            enhanced = json.loads(gpt_response)
            updated_spec = {**original_spec, **enhanced}
            logging.info("Parsed and merged enhanced spec successfully.")
            return updated_spec
        except Exception as e:
            logging.error(f"Failed to parse GPT response: {e}")
            return original_spec
        
    def get_chat_response(self, text: str) -> str:
        return super().get_chat_response(text) 
