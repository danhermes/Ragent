# Autocoder Documentation

## Overview

The Autocoder is an AI-powered code generation system that transforms requirements into working code. It provides two modes of operation:

1. Iterative Mode (`main.py`) - Runs multiple passes to refine code, supporting both n8n workflow generation and Python code generation - > python main.py
2. Single-Pass Mode (`main_one_pass.py`) - Generates code in a single execution

First place  .spec file in /autocoder containing tasks for coding.

## Architecture

```
apis/autocoder/
├── main.py              # Primary entry point for both n8n and Python code generation
├── main_one_pass.py     # Single-pass mode entry point
├── agent/
│   ├── build_cycle_agent.py    # Manages iterative code refinement
│   ├── worker_agent.py         # Handles single-pass code generation
│   ├── code_writer.py          # Generates code using OpenAI API
│   ├── tester.py              # Manages code testing
│   ├── runner_docker.py       # Runs tests in Docker containers
│   └── Dockerfile            # Docker configuration for testing
├── adapters/
│   ├── n8n_adapter.py        # Handles n8n workflow generation
│   ├── automation_adapter.py  # Connects with ragers automation
│   └── proof_adapter.py      # Handles text proofing
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

## Docker Testing Setup

The autocoder uses Docker containers for running pytest tests in an isolated environment. The testing setup includes:

### Docker Configuration
- Base image: `python:3.11-slim`
- Working directory: `/app`
- Required packages:
  - pytest
  - requests-mock
  - pytest-mock
  - requests

### Testing Process
1. Code is generated and saved to a sandbox directory
2. Tests are generated using OpenAI API
3. Baseline test data is created
4. Tests are run in a Docker container with:
   - Mounted sandbox directory
   - Environment variables for baseline data
   - Clean container for each test run

### Building the Docker Image
```bash
# Build the Docker image (run once)
cd apis/autocoder
./build_image.sh
```

### Test Execution Flow
1. Code is saved to `sandbox/temp_code.py`
2. Tests are generated and saved to `sandbox/test_generated.py`
3. Baseline data is saved to `sandbox/baseline_test_data.json`
4. Docker container is started with:
   - Mounted sandbox directory
   - Environment variables for baseline data
5. Tests are executed in the container
6. Results are captured and reported

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
3. Generate initial code
4. Run tests in Docker container
5. Refine code based on test results
6. Repeat until tests pass or max iterations reached

## Adapters
These allow direct connection to other APIs.

### N8nAdapter
- Handles n8n workflow generation
- Manages workflow deployment
- Provides workflow examples
- Handles node configuration

### AutomationAdapter
- Bridges ragers automation requirements
- Connects with AgentBuildCycle
- Manages workflow generation
- Handles deployment

### ProofAdapter
- Handles text proofing requirements
- Connects with proof API
- Manages text corrections
- Saves proofed content

## Logging

Logs are stored in:
1. `apis/autocoder/logs/autocoder_YYYYMMDD_HHMMSS.log`
2. Console output during execution

Log format:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Starting Points

### For `.spec` file based tasks:
```bash
python apis/autocoder/main.py
```

### For direct task execution:
```bash
python apis/autocoder/main_one_pass.py
```

### For n8n workflows:
```python
from apis.autocoder.adapters.n8n_adapter import N8nAdapter
adapter = N8nAdapter()
```

### For automation:
```python
from apis.autocoder.adapters.automation_adapter import AutomationAdapter
adapter = AutomationAdapter()
```

## Configuration

### Environment Variables
- `AUTOCODER_SPEC`: Path to spec file
- `OPENAI_API_KEY`: OpenAI API key for code generation
- `N8N_API_URL`: n8n API endpoint
- `N8N_API_KEY`: n8n API authentication

### Logging Configuration
- Level: DEBUG
- Format: Timestamp - Module - Level - Message
- Output: Both file and console
- Directory: `apis/autocoder/logs` 