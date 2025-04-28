# safe_formatter.py

from collections import defaultdict
from typing import Dict, Any, List, Optional
import logging
import re

class SafeFormatter:
    def __init__(self, missing_default=""):
        self.logger = logging.getLogger(__name__)
        self.missing_default = missing_default

    def safe_context(self, context):
        """
        Return a defaultdict context that supplies default values for missing keys.
        """
        return defaultdict(lambda: self.missing_default, context)

    def required_fields(self, template):
        """
        Extract all fields required by the template using regex.
        """
        return set(re.findall(r"{([a-zA-Z0-9_]+)}", template))

    def missing_keys(self, template, context):
        """
        Identify missing keys based on the template and context provided.
        """
        required = self.required_fields(template)
        existing = set(context.keys())
        return list(required - existing)

    def safe_format(self, template, context):
        """
        Format a template with a safe context to avoid KeyErrors.
        """
        try:
            formatted = template.format(**self.safe_context(context))
        except Exception as e:
            self.logger.error(f"!!!$ Safe_format error formatting template: {e}")
            required = self.required_fields(template)
            self.logger.error(f"!!$$ Required keys: {required}")
            missing = self.missing_keys(template, context)
            self.logger.error(f"!$$$ Missing keys: {missing}")
            raise

        return formatted
    
    def format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary as a readable string"""
        formatted = []
        for key, value in context.items():
            if isinstance(value, (str, int, float, bool)):
                formatted.append(f"{key}: {value}")
            elif isinstance(value, list):
                formatted.append(f"{key}:")
                for item in value:
                    formatted.append(f"  - {item}")
            elif isinstance(value, dict):
                formatted.append(f"{key}:")
                for k, v in value.items():
                    formatted.append(f"  {k}: {v}")
            else:
                formatted.append(f"{key}: {str(value)}")
        return "\n".join(formatted)

# Singleton instance for use
formatter = SafeFormatter()
