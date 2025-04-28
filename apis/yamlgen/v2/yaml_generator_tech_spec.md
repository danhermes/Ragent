# 🧠 Technical Specification – YAML Generator with CLI

This module provides a unified CLI-driven interface for generating YAML files from 
structured input templates across multiple output formats: AutoCoder, LitLegos, n8n, and Proof.

---

ORIGINAL IDEA:
Create an n8n YAML spec template, loader/parser, and workflow creation system like 
the ragers and litlegos template approach.  See current n8n API with py scripts instead of YAML.

 Ragers -> [YAMLgen Adapters,  Autocode, APIs]  -> Deliverable (raw or upload to destination app)

FLAWS

However, you're right that the core value proposition is weakened by the requirement for 
input files to be so similar to the output. The tool would be more valuable if it:
- Supported more diverse input formats (e.g., Markdown, JSON, or even natural language)
- Performed more meaningful transformations between formats
- Added value through validation, enrichment, or standardization of the data
- Provided templates or wizards to help create the input files

---

## 📛 Module Name
`yaml_generator`

---

## 🎯 Purpose
To parse structured template input (e.g., populated markdown, form, or dict) and output valid YAML files according to the selected tool specification. The goal is to unify template-to-YAML generation across projects for code generation (AutoCoder), documentation (LitLegos), workflow automation (n8n), and content proofing (Proof).

---

## 📥 Inputs

### CLI Parameters
- `--input-file`: Path to the structured template file (typically markdown or pre-parsed JSON/dict).
- `--tool`: One of: `autocoder`, `litlegos`, `n8n`, `proof`.
- `--output`: Optional path to save the resulting YAML (otherwise print to stdout).
- `--verbose`: Optional flag to show parsing steps and extracted fields.

### Template Requirements
Each tool type has a corresponding `*_template.yaml` structure defining required keys and formatting logic.

---

## 📤 Outputs

- A YAML file formatted to the specific structure of the target tool.
- CLI output summary (or `stdout`) for visual inspection.

---

## 🧩 Interfaces & Dependencies

- `tech_spec_parser.py`: Responsible for extracting structured information from the input source.
- `yaml_generator.py`: Central logic that receives parsed input and maps to appropriate template format.
- `*_template.yaml` files: Define the final formatting rules and required sections.

---

## 🔄 Core Components

### Main Generator (`yaml_generator.py`)
- `YamlGenerator`: Class that handles templating logic and output formatting.
- `generate(tool, spec)`: Dispatch function that formats the parsed `spec` dict using the correct template.
- `load_template(tool)`: Loads `*.yaml` template for a given tool.

### Parser (`tech_spec_parser.py`)
- `TechSpecParser`: Class with methods like `parse_from_file(filepath)` to return normalized spec.
- Supports Markdown parsing or structured input parsing (JSON/dict).

### CLI Interface (to add)
- `main()`: CLI entrypoint using `argparse`.
- Dispatches to `TechSpecParser` and `YamlGenerator` based on CLI args.

---

## 📂 Files & Directories

| Path                       | Description                                    |
|---------------------------|------------------------------------------------|
| `yaml_generator.py`       | Main YAML generation logic                     |
| `tech_spec_parser.py`     | Converts structured input into a normalized spec dict |
| `*_template.yaml`         | Format-specific YAML output templates          |
| `cli_yaml_generator.py`   | (New) CLI wrapper invoking generator and parser |

---

## 💻 Code Snippets

### Sample CLI usage (to implement)

```bash
python cli_yaml_generator.py   --input-file example.md   --tool litlegos   --output litlegos_output.yaml   --verbose
```

---

## 🔐 Error Handling

- Checks for required keys in parsed input against template.
- Logs missing or incompatible fields.
- If `--verbose`, show warnings and fallback logic.

---

## ✅ Completion Checklist

- [ ] CLI parser implemented with `argparse`.
- [ ] Tool-specific template loading verified.
- [ ] Input validation and error reporting.
- [ ] Output YAML syntax-validated.
- [ ] Unit tests on all 4 tool types.

---

## 📈 Future Enhancements

- Add dry-run mode with diff preview.
- Integrate with `LitLegos`, `n8n API`, or `AutoCoder` runner directly.
- Support directory-wide batch generation.
- GUI wrapper for template selection and previewing.