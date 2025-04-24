import re
from string import Template

# Success Criteria
# Never sends empty prompts to ChatGPT
# Provides explicit warnings or fails fast
# Compatible with run_meeting() and _generate_meeting_doc()
# Drop-in safe replacement for template.format(**context)

def safe_format_prompt(template: str, context: dict, strict=False) -> str:
    required_keys = set(re.findall(r'{([a-zA-Z0-9_]+)}', template))
    missing = required_keys - context.keys()

    if missing:
        msg = f"Missing fields for template: {missing}"
        if strict:
            raise ValueError(msg)
        else:
            print("⚠️ Warning:", msg)

    return Template(template).safe_substitute(**context)

# Example usage
template = "Hello, {name}! Welcome to {company}."
context = {"name": "John", "company": "Acme Inc."}

print(safe_format_prompt(template, context))
