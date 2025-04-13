# n8n Integration Documentation

## Overview

The n8n integration provides workflow automation capabilities for the Ragents system. It allows for the creation and management of automated workflows that connect various services and APIs.

## Architecture

```
apis/n8n/
├── core/             # Core functionality
│   ├── workflow_manager.py
│   ├── api_client.py
│   └── node_handler.py
├── workflows/        # Workflow definitions
├── tests/           # Test suite
└── utils/           # Utility functions
```

## Key Components

### Workflow Manager
- Creates and manages workflows
- Handles workflow execution
- Manages workflow state
- Provides workflow templates

### API Client
- Handles n8n API communication
- Manages authentication
- Processes API responses
- Handles error cases

### Node Handler
- Manages workflow nodes
- Handles node configuration
- Processes node data
- Manages node connections

## Usage

### Basic Usage
```python
from n8n import WorkflowManager

# Initialize manager
manager = WorkflowManager()

# Create workflow
workflow = manager.create_workflow(definition)
```

### Managing Workflows
```python
# Start workflow
manager.start_workflow(workflow_id)

# Stop workflow
manager.stop_workflow(workflow_id)

# Get workflow status
status = manager.get_workflow_status(workflow_id)
```

### Node Operations
```python
# Add node
node = manager.add_node(workflow_id, node_type, config)

# Connect nodes
manager.connect_nodes(workflow_id, source_node, target_node)
```

## Integration with Autocoder

The n8n integration works with the Autocoder to:
1. Generate workflow definitions
2. Deploy generated workflows
3. Monitor workflow execution
4. Handle workflow errors

## Configuration

### Environment Variables
- `N8N_API_URL`: API endpoint
- `N8N_API_KEY`: API authentication
- `N8N_WEBHOOK_URL`: Webhook endpoint

### Workflow Templates
- Common workflow patterns
- Node configurations
- Error handling
- Data processing

## Development

### Adding New Features
1. Create feature branch
2. Update node handlers
3. Add tests
4. Update documentation

### Testing
- Unit tests for workflow management
- Integration tests with Autocoder
- API client tests
- Node handler tests

## Troubleshooting

### Common Issues
1. API connection errors
2. Workflow execution failures
3. Node configuration issues
4. Data processing errors

### Solutions
1. Check API configuration
2. Review workflow definition
3. Verify node settings
4. Check data formats

## Support

For issues and questions:
1. Check documentation
2. Review error logs
3. Contact support 