# 🧰 Safe Formatter Module for RAgent

The `SafeFormatter` is a utility module designed to prevent runtime `KeyError`s during prompt formatting in the RAgent system. It ensures robust template expansion by gracefully handling missing context variables.

---

## 🧠 Core Problem

In modules like `project_work.py`, using `.format(**context)` frequently causes `KeyError` exceptions or silent prompt failures when context is incomplete. This leads to empty prompt submissions and degraded agent performance.

---

## ✅ Features

- Prevents `KeyError` by injecting default values for missing fields
- Detects required fields from templates
- Returns missing keys for diagnostics
- Clean integration with all RAgent meeting and prompt handling workflows

---

## 🏗️ Architecture

```bash
ragent/
├── helpers/
│   └── safe_formatter.py  # <--- Add this here
├── project_work.py        # Uses SafeFormatter for template processing
├── prompts/               # Templates with .format fields
└── ...
```

---

## 💡 Usage Example

```python
from helpers.safe_formatter import formatter

context = {"project_name": "Guard America"}
template = """
Welcome to {project_name}.
Your role is {user_role}.
"""

# Print missing keys
print(formatter.missing_keys(template, context))
# ['user_role']

# Safely fill in the template
result = formatter.safe_format(template, context)
print(result)
# Welcome to Guard America.
# Your role is .
```

---

## 🧩 Integration Instructions

1. **Place** `safe_formatter.py` into `helpers/`.
2. **Import** where needed:
   ```python
   from helpers.safe_formatter import formatter
   ```
3. **Replace** all raw `.format(**context)` calls with:
   ```python
   formatter.safe_format(template, context)
   ```
4. **Optional:** Log missing fields using:
   ```python
   missing = formatter.missing_keys(template, context)
   if missing:
       log.warning(f"Missing fields: {missing}")
   ```

---

## 🚀 Next Steps

- Add CLI or debug view to output missing context fields at runtime
- Extend to support `jinja2` in future prompt rendering
