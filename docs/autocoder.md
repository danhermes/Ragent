# Autocoder Documentation

## Overview

The Autocoder is an AI-powered code generation system that transforms requirements into working code. It provides two modes of operation:
1. Iterative Mode (`main.py`) - Runs multiple passes to refine code, supporting both n8n workflow generation and Python code generation
2. Single-Pass Mode (`main_one_pass.py`) - Generates code in a single execution

## Architecture

```
apis/autocoder/
├── main.py              # Primary entry point for both n8n and Python code generation
├── main_one_pass.py     # Single-pass mode entry point
├── agent/
│   ├── build_cycle_agent.py    # Manages iterative code refinement
│   └── worker_agent.py         # Handles single-pass code generation
├── core/
│   ├── code_generator.py       # Core code generation logic
│   ├── requirements_parser.py  # Requirements processing
│   └── validation.py          # Code validation
├── templates/           # Code templates
├── tests/              # Test suite
└── utils/              # Utility functions
```

## Components

### Iterative Mode (`main.py`)
- Runs multiple iterations (default=3) to refine code
- Supports both n8n workflow generation and Python code generation
- Uses AgentBuildCycle for iterative improvement
- Handles overall coordination
- Determines task type based on language specification

### Single-Pass Mode (`main_one_pass.py`)
- Generates code in a single execution
- Focuses on direct Python code generation
- Uses WorkerAgent for one-time execution
- Simpler, more focused operation

### AgentBuildCycle
- Manages iterative code refinement
- Runs multiple passes to improve code
- Handles both n8n workflow and Python code generation
- Determines task type based on language specification
- Handles code validation and improvement

### WorkerAgent
- Generates Python code in a single pass
- Executes tasks directly
- Provides focused code generation
- Runs in isolated environment

## Functionality

### Task Specification
- Tasks are defined in `.spec` files
- Default file: `autocoder.spec`
- Custom path via `AUTOCODER_SPEC` env var
- Supports both n8n workflow and Python code tasks
- Task type determined by language specification

### Code Generation Process
1. Read task from spec file
2. Choose mode (iterative or single-pass)
3. For iterative mode:
   - If n8n task: generate and deploy workflow
   - If Python task: generate and test code through iterations
4. For single-pass mode: generate Python code once
5. Validate and output final code

### n8n Integration
- Available in iterative mode
- Generates n8n workflows
- Manages workflow automation
- Coordinates with n8n API

### Logging
- Iterative mode: `logs/autocoder_{timestamp}.log`
- Single-pass mode: `logs/worker_{timestamp}.log`
- Separate logging for each mode
- Timestamped log files

## Usage

### Running the Autocoder
```bash
# Run iterative mode (multiple passes)
python apis/autocoder/main.py

# Run single-pass mode
python apis/autocoder/main_one_pass.py
```

### Spec File Format
```text
# For n8n workflow
{
    "language": "n8n",
    "requirements": {...},
    "specifications": {...}
}

# For Python code
Write a Python script that fetches current weather data for a list of cities using a public weather API and stores the results in a JSON file.
```

### Environment Variables
- `AUTOCODER_SPEC`: Path to spec file
- `AUTOCODER_API_KEY`: API authentication
- `AUTOCODER_MODEL`: Model selection

## Development

### Adding New Features
1. Create feature branch
2. Update agent logic
3. Add tests
4. Update documentation

### Testing
- Unit tests for agents
- Integration tests
- n8n workflow tests
- Code generation tests

## Troubleshooting

### Common Issues
1. Spec file not found
2. Code generation failures
3. n8n workflow errors
4. Validation errors

### Solutions
1. Check spec file path
2. Review task description
3. Check n8n configuration
4. Verify validation rules

## Support

For issues and questions:
1. Check documentation
2. Review error logs
3. Contact support 