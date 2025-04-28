# Piper Agent Spec

- `parse_input(filepath)` reads `.md` Automation Tech Spec
- Extracts fields: Workflow Name, Purpose, Inputs, Outputs, Apps, Nodes, Connections
- Structures parsed data into a clean dictionary
- `format_yaml(structured_spec, tool)` prepares GPT prompts for YAML
- `validate_yaml(yaml_output, tool)` ensures structural compliance
