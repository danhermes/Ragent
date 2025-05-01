# n8n API Integration

This module provides a Python interface for interacting with n8n workflows and API. It allows for programmatic creation, management, and execution of n8n workflows. User calls API methods and this generator produces a JSON file for submission to n8n application.

Warning: This functionality works up until a point. Uploaded nodes appear in n8n but there are lots of "?"s in the n8n app and the workflow doesn't run.  This needs work.

This framework requires the development of a n8n_run.py script to call the helper. The use of YAMLgen was intended to ease this burden with the following pipeline: 

Ragers -> (tech spec) -> YAMLgen -> (n8n_workflow.yaml) -> autocoder -> (n8n_run.py) 
  -> n8n api [this module] -> n8n_workflow.json -> n8n Application

  Ragers -> [YAMLgen Adapters,  Autocode, APIs]  -> Deliverable (raw or upload to destination app)

## Architecture

The module consists of three main components:

1. **N8nApiClient**: Core API client for direct communication with n8n
2. **N8nWorkflowHelper**: High-level helper for creating and managing workflows
3. **N8nConfig**: Configuration management for n8n API settings

### Component Details

#### N8nApiClient
- Handles direct HTTP communication with n8n API
- Provides methods for CRUD operations on workflows, nodes, credentials, and webhooks
- Implements error handling and logging
- Supports all major n8n API endpoints

#### N8nWorkflowHelper
- High-level interface for workflow creation and management
- Provides helper methods for creating common node types:
  - Schedule triggers
  - OpenAI integration
  - Dropbox operations
  - Email sending
  - Spreadsheet operations
  - Data filtering
  - Field editing
- Handles node connections and workflow structure

#### N8nConfig
- Manages n8n API configuration
- Loads settings from environment variables
- Provides default values for local development

## Usage

### Basic Setup

1. Configure environment variables:
```bash
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your_api_key
```

2. Initialize the helper:
```python
from apis.n8n import N8nConfig, N8nWorkflowHelper

config = N8nConfig()
helper = N8nWorkflowHelper(config)
```

### Creating Workflows

Example workflow creation:
```python
# Create nodes
schedule_node = helper.create_schedule_trigger("Daily Schedule", trigger_at_hour=9)
openai_node = helper.create_openai_message("Analyze Data", "gpt-4", "Analyze the following data...")
email_node = helper.create_send_email("Send Report", "team@example.com", "Daily Report", "{{$json}}")

# Define connections
connections = {
    "Daily Schedule": {"main": [[{"node": "Analyze Data", "type": "main"}]]},
    "Analyze Data": {"main": [[{"node": "Send Report", "type": "main"}]]}
}

# Create workflow
workflow = helper.create_workflow(
    name="Daily Analysis Workflow",
    nodes=[schedule_node, openai_node, email_node],
    connections=connections
)
```

### Available Node Types

1. **Schedule Trigger**
   - Creates time-based workflow triggers
   - Supports daily, weekly, and custom intervals

2. **OpenAI Integration**
   - Connects to OpenAI API
   - Supports chat completions and analysis

3. **Dropbox Operations**
   - List folders
   - Upload files
   - Download files

4. **Email**
   - Send emails via SMTP
   - Supports HTML and text formats

5. **Spreadsheet Operations**
   - Read XLSX files
   - Write XLSX files
   - Extract data from specific ranges

6. **Data Processing**
   - Filter data based on conditions
   - Edit fields and transform data

## Input/Output

### Input
- Workflow configuration (nodes, connections, settings)
- Node parameters (credentials, settings, data)
- API configuration (URL, API key)

### Output
- Workflow objects with unique IDs
- Execution results and status
- Error messages and logs

## Error Handling

The module implements comprehensive error handling:
- API connection errors
- Invalid configurations
- Workflow creation failures
- Node connection issues

All errors are logged with detailed information for debugging.

## Logging

The module uses Python's logging system with detailed formatting:
```python
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Logs include:
- API requests and responses
- Workflow creation steps
- Node configuration details
- Error messages and stack traces

## Docker Support

The module is compatible with n8n Docker deployments. See `n8n_docker_guide.txt` for detailed Docker setup instructions.

## Best Practices

1. Always use environment variables for sensitive data
2. Implement proper error handling in workflow creation
3. Use the helper methods for common node types
4. Test workflows in a development environment first
5. Monitor execution logs for debugging
6. Keep credentials secure and rotate them regularly 