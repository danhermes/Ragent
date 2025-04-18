# Agent Workflows Documentation

## Overview
The Agent Workflows system provides a framework for managing and executing development tasks through a command-line interface. It integrates code generation, testing, and task management in a modular architecture.

## Architecture

### Components

1. **WorkflowCLI** (`workflow_cli.py`)
   - Command-line interface for task management
   - Commands:
     - `assign <task>`: Assign a new task to the developer agent
     - `status`: Check current task status
     - `exit`/`quit`: Exit the CLI
   - Handles user input and command routing
   - Provides error handling and user feedback

2. **CodeTasker** (`code_tasker.py`)
   - Manages task workflow and history
   - Tracks active tasks and task history
   - Integrates with DeveloperAdapter for task execution
   - Provides status reporting
   - Maintains task history with status and results

3. **DeveloperAdapter** (`developer_adapter.py`)
   - Coordinates code generation and testing
   - Components:
     - CodeWriter: Handles code generation
     - Tester: Manages test execution
   - Features:
     - Task execution pipeline
     - Error handling and logging
     - Test result processing
     - Debug attempt on test failure

4. **TestLayer** (`apis/autocoder/agent/test_layer.py`)
   - Provides test infrastructure and mock services
   - Features:
     - Mock API implementations
     - File system operations
     - Database operations
     - ChatGPT responses
   - Supports baseline data loading
   - Enables test mode operation

## Usage

### Starting the Workflow CLI
```python
from agent_workflows.code_tasker import CodeTasker

tasker = CodeTasker()
tasker.cli.workflow_cli(tasker)
```

### Example Session
```
(Blaine) > Ready to receive tasks. Type 'exit' to quit.
(Blaine) > assign Create a new API endpoint
(Blaine) > Assigning to Woz...
(Woz) > Tests passed. Task complete.
(Blaine) > status
(Blaine) > Current task status: {'task': 'Create a new API endpoint', 'status': 'assigned', 'result': 'Tests passed. Task complete.'}
```

## Error Handling
- CLI commands are wrapped in try-except blocks
- Task execution errors are logged and reported
- Test failures trigger debug attempts
- Fatal errors return appropriate error messages

## Logging
- Comprehensive logging throughout the system
- Log levels: INFO, WARNING, ERROR
- Log messages include component identification (e.g., [Woz], [Blaine])

## Testing
- TestLayer provides mock implementations for:
  - API calls
  - File operations
  - Database operations
  - ChatGPT responses
- Supports baseline data loading for consistent testing
- Enables test mode operation without external dependencies

## Dependencies
- Python standard library
- Logging module
- Custom components:
  - CodeWriter
  - Tester
  - TestLayer

## Future Enhancements
- Enhanced debug capabilities
- More sophisticated task queuing
- Additional CLI commands
- Extended test coverage
- Performance monitoring 