# Ragent Dispatch System

The Dispatch System is the executive function of the Ragent ecosystem. It listens to the stakeholder (via Blaine CLI), parses intent, creates structured tasks, coordinates agents and tools, tracks execution, and delivers progress and insights back to the user.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Required Python packages:
  ```
  openai>=1.0.0
  ```

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup
1. Set your OpenAI API key (required by Blane for natural language processing):
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
   Or add it to your `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

### Starting the System

1. Make sure you're in the root directory of the project (where the `HQ` folder is located)

2. From the command line:
```bash
python HQ/workflow_cli.py
```

3. You should see the Blane CLI prompt:
```
(Blane) > Ready to receive tasks. Type 'help' for available commands.
```

4. Try some commands:
   - Natural language: "I need help with a coding task"
   - Traditional: "help"

### First Run
1. The system will greet you with:
   ```
   (Blaine) > Ready to receive tasks. Type 'help' for available commands.
   ```

2. Try a natural language command:
   ```
   (Blaine) > I need to create a new email notification system
   ```

3. Or use a traditional command:
   ```
   (Blaine) > assign code email notifier
   ```

## Core Components

### CodeTasker
The core task management system that:
- Manages task workflow and history
- Tracks active tasks and task history
- Integrates with DeveloperAdapter for task execution
- Provides status reporting
- Maintains task history with status and results

### DispatchSystem
The core dispatch system that handles:
- Task management and state tracking
- Workflow orchestration
- Tool and API integration
- Event/notification system

### WorkflowCLI
The command-line interface that:
- Provides a natural language interface
- Handles command parsing and routing
- Manages user interaction and feedback
- Supports task status queries

### NLPProcessor
Natural language processing component that:
- Interprets natural language commands
- Converts user intent into structured commands
- Provides command suggestions
- Handles ambiguity with confidence scoring

## Features

### Natural Language Processing
- OpenAI-powered command interpretation
- Confidence-based command validation
- Interactive clarification when needed
- Command suggestions for partial input
- Fallback to traditional command parsing

### Task Management
- Create and track tasks with unique IDs
- Support for different task types (code, write, plan)
- State persistence and recovery
- Detailed logging and status tracking

### Workflow Orchestration
- Integration with specialized workflow engines:
  - AutoCoder for coding tasks
  - LitLegos for writing tasks
  - Ragers for planning tasks
- Agent coordination and task delegation
- Phase tracking and progress monitoring

### Tool Integration
- Support for multiple tools and APIs:
  - AutoCoder
  - LitLegos
  - n8n
  - OpenAI Assistants
- Data source integration:
  - Gmail API
  - Cloud Doc Repo
  - GitHub
  - Local Docs
  - SQL DB
  - Vector DB

### Command Interface
Available commands:
- `assign/start/run` - Start a new task
- `status/?` - Check task status
- `pause` - Pause a running task
- `stop/abort` - Stop a task
- `resume` - Resume a paused task
- `where` - Get task location/context
- `get` - Retrieve task information
- `code` - Start a coding task
- `write` - Start a writing task
- `plan` - Start a planning task
- `ask` - Ask a question about a task
- `give` - Provide information for a task
- `help` - Show help information
- `exit` - Exit the program

## Usage Examples

1. Natural language command:
```
(Blaine) > I need to create a new email notification system
(Blaine) > I'm not very confident about this interpretation. This seems like a coding task.
(Blaine) > Did you mean: assign code email notification system? (y/n)
y
Task 0001 created: code email notification system
```

2. Traditional command:
```
(Blaine) > assign code email notifier
Task 0001 created: code email notifier
```

3. Check task status:
```
(Blaine) > status 0001
pending
```

4. Get help:
```
(Blaine) > help
Available commands:
  assign (start, run) - Assign a new task
  status (?) - Check current task status
  pause - Pause a running task
  stop (abort) - Stop/abort a task
  ...
```

## Implementation Details

### Natural Language Processing
- Uses OpenAI's GPT-3.5-turbo model
- System prompt defines available commands and task types
- Returns structured JSON with command, args, confidence, and explanation
- Interactive clarification for low-confidence interpretations
- Fallback to traditional parsing if NLP is unavailable

### Task State
Tasks are stored in JSON format in the `tasks/{task_id}/state.json` file, containing:
- Task ID
- Command
- Type
- Project
- Workflow engine
- Status
- Phase
- Agents
- Tools
- Logs
- Start time
- Question document (if any)

### Error Handling
- Graceful error recovery
- Clear error messages
- Status tracking for failed tasks
- Logging for debugging

### Future Enhancements
- Multi-step tasks
- Interruption queue
- Session memory
- Auto-summary
- Voice interface
- Dashboard GUI
- Plugin system
- Fallback classifier 