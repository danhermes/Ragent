import os
import re

def save_code(code, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(code)
    return path

def clean_code_block(text):
    """
    Extract the first code block from the GPT output.
    Assumes it's in markdown format like ```python ... ```
    """
    
    language_hint="python"
    # Match ```python\n<code>\n```
    pattern = rf"```{language_hint}\s*(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Fallback: if no language hint present
    fallback_match = re.search(r"```(?:\w+)?\s*(.*?)```", text, re.DOTALL)
    if fallback_match:
        return fallback_match.group(1).strip()

    # Strip '''
    lines = text.strip().splitlines()
    # If it starts and ends with triple backticks, remove them
    if lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines[0].strip().startswith("```python"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    text = "\n".join(lines).strip()

    return text