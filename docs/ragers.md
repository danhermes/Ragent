# Ragers Documentation

## Overview

Ragers is the core orchestration system that manages the entire development lifecycle of AI projects. It provides a structured approach to goal setting, project management, and deliverable generation.

## Template-Based Architecture

Ragers uses a template-based architecture to standardize project workflows and deliverables. The system supports multiple project types, each with its own set of templates and phases.

### Project Types

Ragers supports three main project types:

1. **Code Projects**
   - Focus: Software development
   - Phases: Strategy → Kickoff → Architecture → Modules → Review
   - Outputs: Technical designs, code modules, tests

2. **Writing Projects**
   - Focus: Documentation and content creation
   - Phases: Planning → Outline → Draft → Review → Final
   - Outputs: Project outlines, content drafts, final documents

3. **Planning Projects**
   - Focus: Strategic planning and project management
   - Phases: Discovery → Analysis → Strategy → Roadmap → Review
   - Outputs: Project plans, strategy documents, roadmaps

### Template Structure

Each project type follows a consistent template structure:

```
ragers/templates/
├── code/             # Code project templates
│   ├── code_mode.yaml
│   ├── code_meeting_*.md
│   └── code_review_*.md
├── write/            # Writing project templates
│   ├── write_mode.yaml
│   ├── write_meeting_*.md
│   └── write_review_*.md
└── plan/             # Planning project templates
    ├── plan_mode.yaml
    ├── plan_meeting_*.md
    └── plan_review_*.md
```

### Meeting Protocols

Each project type uses standardized meeting protocols that:
- Follow consistent prompts and headings
- Produce atomic, reusable, agent-runnable material
- Maintain traceability and documentation
- Support automated processing

## Command Line Interface (CLI)

### Getting Started

1. **Initialize a New Project**
```bash
python -m ragers init <project_name> --type <project_type>
```

2. **Start a Project Phase**
```bash
python -m ragers start <phase_name> --project <project_name>
```

3. **Run a Meeting**
```bash
python -m ragers meeting <meeting_type> --project <project_name>
```

### Common Commands

```bash
# List available project types
python -m ragers list types

# Show project status
python -m ragers status <project_name>

# Generate deliverables
python -m ragers generate <deliverable_type> --project <project_name>

# Review project
python -m ragers review <project_name>
```

### Project Configuration

Each project maintains its configuration in:
- `.goals` - Project objectives
- `.env` - Environment variables
- `project_config.yaml` - Project-specific settings

### Phase Management

Phases are managed through the CLI:
```bash
# Start a new phase
python -m ragers phase start <phase_name>

# Complete current phase
python -m ragers phase complete

# Review phase progress
python -m ragers phase status
```

### Meeting Management

Meetings follow standardized templates:
```bash
# Start a new meeting
python -m ragers meeting start <meeting_type>

# Generate meeting minutes
python -m ragers meeting minutes

# Review meeting outcomes
python -m ragers meeting review
```

## System Architecture

```
ragers/
├── core/             # Core orchestration
│   ├── orchestrator.py
│   ├── workflow_manager.py
│   └── deliverable_manager.py
├── subsystems/       # Specialized subsystems
│   ├── rag/         # RAG system
│   ├── worker/      # Worker system
│   ├── autocoder/   # Autocoder system
│   ├── proof/       # Proof verification
│   └── n8n/         # n8n integration
├── modes/           # Operational modes
├── tools/           # Utility tools
└── utils/          # Helper functions
```

## Core Components

### Orchestrator
- Manages project lifecycle
- Coordinates subsystem interactions
- Handles milestone tracking
- Generates deliverables

### Workflow Manager
- Controls execution flow
- Manages state transitions
- Handles error recovery
- Maintains execution history

### Deliverable Manager
- Tracks deliverables
- Manages versions
- Handles approvals
- Maintains documentation

## Subsystems

### RAG System
The RAG (Retrieval-Augmented Generation) system enhances AI responses by retrieving relevant information from a knowledge base.

#### Architecture
```
ragers/rag/
├── core/             # Core functionality
│   ├── retriever.py
│   ├── generator.py
│   └── knowledge_base.py
├── data/            # Knowledge base files
├── tests/           # Test suite
└── utils/          # Utility functions
```

#### Key Components
- **Retriever**: Searches knowledge base, ranks documents, filters results
- **Generator**: Processes context, generates responses, formats output
- **Knowledge Base**: Stores documents, manages indexing, handles versioning

#### Usage
```python
from rag import RAGSystem
rag = RAGSystem()
response = rag.query("What is the best way to handle API errors?")
```

#### Configuration
- `RAG_MODEL_PATH`: Model location
- `RAG_KB_PATH`: Knowledge base path
- `RAG_CACHE_DIR`: Cache directory
- `RAG_LOG_LEVEL`: Logging level

### Worker System
Manages AI agents that perform specific tasks within the system.

#### Architecture
```
ragers/worker/
├── core/             # Core functionality
│   ├── worker.py
│   ├── task_manager.py
│   └── communication.py
├── workers/         # Worker implementations
├── tests/          # Test suite
└── utils/         # Utility functions
```

#### Key Components
- **Worker**: Executes tasks, manages state, handles errors
- **Task Manager**: Assigns tasks, monitors progress, manages queues
- **Communication**: Handles interactions, message passing, coordination

#### Usage
```python
from worker import WorkerSystem
worker_system = WorkerSystem()
worker = worker_system.create_worker("developer")
task = worker.assign_task("Implement API endpoint")
```

#### Configuration
- `WORKER_MODEL_PATH`: Model location
- `WORKER_TASK_DIR`: Task directory
- `WORKER_LOG_DIR`: Log directory
- `WORKER_LOG_LEVEL`: Logging level

### Autocoder System
Transforms requirements into working code and workflows.

#### Architecture
```
apis/autocoder/
├── core/             # Core functionality
│   ├── code_generator.py
│   ├── requirements_parser.py
│   └── validation.py
├── templates/        # Code templates
├── tests/           # Test suite
└── utils/           # Utility functions
```

#### Key Components
- **Code Generator**: Converts requirements to code, generates workflows
- **Requirements Parser**: Processes input, extracts specifications
- **Validation System**: Verifies code, runs tests, checks errors

#### Usage
```python
from autocoder import CodeGenerator
generator = CodeGenerator()
code = generator.generate_code(requirements)
```

#### Configuration
- `AUTOCODER_API_KEY`: API authentication
- `AUTOCODER_MODEL`: Model selection
- `AUTOCODER_TEMPLATE_DIR`: Template directory

### Proof System
Validates and verifies the correctness of generated code and workflows.

#### Architecture
```
apis/proof/
├── core/             # Core functionality
│   ├── verifier.py
│   ├── validator.py
│   └── reporter.py
├── tests/           # Test suite
├── templates/       # Verification templates
└── utils/          # Utility functions
```

#### Key Components
- **Verifier**: Validates code, checks workflow integrity
- **Validator**: Runs tests, performs analysis, checks style
- **Reporter**: Generates reports, tracks issues, provides metrics

#### Usage
```python
from proof import Verifier
verifier = Verifier()
result = verifier.verify_code(code, requirements)
```

#### Configuration
- `PROOF_API_KEY`: API authentication
- `PROOF_TEST_DIR`: Test directory
- `PROOF_REPORT_DIR`: Report directory
- `PROOF_LOG_LEVEL`: Logging level

### n8n Integration
Provides workflow automation capabilities.

#### Architecture
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

#### Key Components
- **Workflow Manager**: Creates/manages workflows, handles execution
- **API Client**: Handles API communication, manages authentication
- **Node Handler**: Manages nodes, handles configuration, processes data

#### Usage
```python
from n8n import WorkflowManager
manager = WorkflowManager()
workflow = manager.create_workflow(definition)
```

#### Configuration
- `N8N_API_URL`: API endpoint
- `N8N_API_KEY`: API authentication
- `N8N_WEBHOOK_URL`: Webhook endpoint

## Usage

### Basic Usage
```bash
python run_orchestrator.py
```

### Running Specific Phases
```bash
# Run strategic goal setting
python run_orchestrator.py --phase strategic-goals

# Run kickoff meeting
python run_orchestrator.py --phase kickoff

# Run project creation
python run_orchestrator.py --phase project-creation

# Run worker collaboration
python run_orchestrator.py --phase worker-collaboration

# Run work loop
python run_orchestrator.py --phase work-loop

# Run deliverable presentation
python run_orchestrator.py --phase present-deliverables
```

### Milestone Review
```bash
python run_orchestrator.py --phase milestone-review --milestone "Phase 1"
```

### Upward Communication
```bash
python run_orchestrator.py --message "Need clarification" --sender "User"
```

## Configuration

### Environment Variables
- Set in `.env` file
- Required for API access
- Configuration settings

### Goals File
- Located in `.goals`
- Defines project objectives
- Can be overridden via command line

## Logging

- Logs stored in `logs/` directory
- Real-time console output
- Timestamped entries
- Phase-specific logging

## Development

### Adding New Features
1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Submit pull request

### Testing
- Unit tests in `tests/` directory
- Integration tests for workflows
- Performance testing

## Troubleshooting

### Common Issues
1. Missing dependencies
2. Configuration errors
3. API connection issues
4. File permission problems

### Solutions
1. Check installation
2. Verify configuration
3. Test API connections
4. Check file permissions

## Support

For issues and questions:
1. Check documentation
2. Review logs
3. Contact support 