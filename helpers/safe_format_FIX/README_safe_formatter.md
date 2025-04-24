
# 🧠 Ragent Prompt Formatter Utility

This module (`ragent/utils/prompt_utils/safe_formatter.py`) provides a safe and robust way to handle string template formatting within the Ragent application. It ensures that missing fields do not cause silent failures or empty prompts when communicating with ChatGPT.

## 📐 Architecture Overview

### 📁 File Structure
```
ragent/
├── utils/
│   └── prompt_utils/
│       └── safe_formatter.py
```

### 🔧 Component: `safe_format_prompt()`
This function is the core logic of the formatter.

#### Inputs:
- `template: str` — The prompt template string containing `{placeholders}`.
- `context: dict` — A dictionary with values to inject.
- `strict: bool` — If `True`, raises an error on missing keys. If `False`, logs warnings.

#### Output:
- A formatted string with placeholders replaced or warnings raised.

### 🔐 Safety Features
- Logs missing fields instead of silently failing.
- Optional strict mode for debugging.
- Falls back gracefully when data is missing.

---

## 🚀 Usage

```python
from ragent.utils.prompt_utils.safe_formatter import safe_format_prompt

template = "Generate meeting notes for {project_name} with {attendees}."
context = {"project_name": "Guard America"}  # 'attendees' is missing

# Non-strict use (warns)
formatted = safe_format_prompt(template, context)

# Strict use (raises error)
formatted = safe_format_prompt(template, context, strict=True)
```

---

## ✅ Integration Points

Replace the following in `project_work.py`:
```python
prompt = template_content.format(**context)
```
With:
```python
from ragent.utils.prompt_utils.safe_formatter import safe_format_prompt
prompt = safe_format_prompt(template_content, context, strict=False)
```

This ensures templates are robust and ChatGPT always receives valid prompts.

---

## 📎 Related Modules

- `project_work.py`
- `meeting_manager.py`
- `document_generator.py`

---

## 📅 Last Updated
2025-04-23
