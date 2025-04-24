# YAML Generator

A CLI tool for generating tool-specific YAML files from structured templates. Supports multiple output formats including AutoCoder, LitLegos, n8n, and Proof.

## 🏗️ Architecture

The tool consists of three main components:

1. **YamlParser** (`yaml_parser.py`)
   - Parses input files (YAML/JSON)
   - Converts input into a unified specification format
   - Handles file loading and validation

2. **YAMLGenerator** (`yaml_generator.py`)
   - Takes unified spec and generates tool-specific YAML
   - Supports multiple output formats:
     - `autocoder`: For code generation projects
     - `litlegos`: For book/document generation
     - `n8n`: For workflow automation
     - `proof`: For content validation

3. **CLI Interface** (`cli.py`)
   - Command-line interface for the tool
   - Handles argument parsing and execution flow
   - Manages input/output file operations
   - Organizes output into project-specific folders

## 📁 Project Structure

The tool automatically organizes all generated files into a project-specific structure:

```
projects/
  └── project_name/
      ├── specs/          # Original and unified specs
      │   ├── input_spec_TIMESTAMP.yaml
      │   └── unified_spec_TIMESTAMP.yaml
      ├── yaml/           # Generated YAML files
      │   └── TOOL_TIMESTAMP.yaml
      └── logs/           # Generation logs
          └── generation_TIMESTAMP.log
```

Each generation creates:
- Input spec copy
- Unified spec copy
- Generated YAML file
- Generation log

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>

# Navigate to the yamlgen directory
cd apis/yamlgen

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Usage

```bash
python cli.py --input-file <input-file> --tool <tool-name> [--output <output-file>] [--verbose]
```

### Arguments

- `--input-file`: Path to input template file (YAML/JSON) [required]
- `--tool`: Target tool for YAML generation [required]
  - Choices: `autocoder`, `litlegos`, `n8n`, `proof`
- `--output`: Path to save output YAML (default: stdout)
- `--verbose`: Show detailed parsing and generation steps

### Examples

```bash
# Generate LitLegos YAML
python cli.py --input-file example_input.yaml --tool litlegos --verbose

# Generate AutoCoder YAML
python cli.py --input-file example_input.yaml --tool autocoder

# Generate n8n YAML
python cli.py --input-file example_input.yaml --tool n8n

# Generate Proof YAML
python cli.py --input-file example_input.yaml --tool proof
```

## 📝 Input Format

The input file should be a YAML or JSON file containing the following structure:

```yaml
title: Your Project Title
project: Your Project Name
goal: Project goal description
prompt: Generation prompt
style: Style description
content_type: Type of content
length: Content length
narrative_rhythm: Narrative structure
target_reader: Target audience
arc: Content arc
flavor: Content flavor
test_mode: false

# LitLegos specific
big_ideas: []
themes: []
patterns: []
examples: []
inserts: []
toc: []

# n8n specific
workflow_name: Workflow Name
settings: {}
nodes: []
connections: []

# AutoCoder specific
modules: []

# Proof specific
purpose: Validation purpose
sections: []
```

## 🎯 Output Formats

### AutoCoder YAML
```yaml
project: Project Name
goal: Project Goal
modules: []
test_mode: false
```

### LitLegos YAML
```yaml
title: Title
content_type: book
length: Length
prompt: Prompt
style_profile: Style
narrative_rhythm: Rhythm
target_reader: Reader
arc: Arc
flavor: Flavor
test_mode: false
big_ideas: []
themes: []
patterns: []
examples: []
inserts: []
toc: []
```

### n8n YAML
```yaml
workflow:
  name: Workflow Name
  settings: {}
nodes: []
connections: []
```

### Proof YAML
```yaml
document_title: Title
purpose: Purpose
tone: Tone
sections: []
```

## 📊 Logging

The tool automatically creates detailed logs for each generation:
- Timestamp of generation
- Input file used
- Output file created
- Tool used
- Verbose mode status

Logs are stored in the project's `logs` directory with timestamps for easy tracking.

## 🐛 Error Handling

The tool provides error handling for:
- Invalid input file formats
- Missing required fields
- File I/O errors
- Invalid tool specifications
- Project directory creation issues

## 📚 Dependencies

- Python 3.7+
- PyYAML
- argparse
- pathlib

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

[Your License Here] 