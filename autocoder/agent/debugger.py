import openai
from utils.file_ops import save_code, clean_code_block

def revise_code_with_error_context(code_path, error_log):
    with open(code_path, "r") as f:
        original_code = f.read()

    prompt = f"""
The following Python code has an error. Analyze the error and revise the code to fix it.

--- Original Code ---
{original_code}

--- Error Log ---
{error_log}

Please provide the entire corrected Python code file only. Do not include explanations or markdown.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    fixed_code = response.choices[0].message.content.strip()
    fixed_code = clean_code_block(fixed_code)
    fixed_path = code_path.replace(".py", "_fixed.py")
    save_code(fixed_code, fixed_path)
    return fixed_path
