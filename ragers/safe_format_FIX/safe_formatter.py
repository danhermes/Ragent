# safe_formatter.py

from collections import defaultdict
import re

class SafeFormatter:
    def __init__(self, missing_default=""):
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
        return template.format(**self.safe_context(context))

# Singleton instance for use
formatter = SafeFormatter()
