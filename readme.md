# RAgent Framework

A framework for AI-powered project management and collaboration.

## RAgents So Far

1. **The Ragers**: An autonomous organization of agents, loosely configured in a hierarchy (director, manager, worker, SME), that take a goal, discuss it, and develop it into a written deliverable such as a business strategy or a technical specification.
2. **Cliff**: A PC-based web agent that listens to conversations ambiently and provides a browser-based HUD for technical terms employing a local STT (Whisper/Vosk) and ChatGPT.
3. **Nevil**: A talking PiCar robot built using a Raspberry Pi (8GB RAM) and onboard SST and LLM (TinyLlama). Converses wittily, plays autonomously, and has a basic RAG architecture whereby it can stay abreast of your schedule and goals for the week, acting as a nominally helpful digital assistant.

## Human Interfaces

- **Voice**: mic/speaker w/ STT/TTS - OpenAI Whisper API, Whisper local, and Vosk
- **Text**: web browser or mobile device
- **Command line**

## Brains: GPTs and LLMs

- ChatGPT
- Gemma2b, TinyLlama (for Raspberry Pi-driven robots)

## RAgents Toys - Agentic APIs

RAgents have specialized tools (toys) at their disposal:

1. **AutoCoder**: Codes (Python), tests (pytest), and debugs (in temp Docker containers) against a technical spec
2. **LitLegos**: Writes a book given a book title and Table of Contents
3. **Proofer**: Proofreads a manuscript
4. **n8n**: Creates and uploads autonomous n8n workflows

## Project Management Framework

The RAgent framework provides a structured approach to project management through three main components:

1. **ProjectStart**: Handles project initialization and configuration
2. **ProjectWork**: Manages project meetings and team interactions
3. **ProjectDocuments**: Handles document generation and management

### Project Types

The framework supports different project types, each with its own configuration and templates:

1. **Code Project**
   - Purpose: Software development projects
   - Phases: Strategy, Kickoff, Architecture, Modules, Review
   - Roles: Supervisor, Manager, Developer, Tester
   - Outputs: Technical design, Architecture, Test plan, Code modules

2. **Writing Project**
   - Purpose: Documentation and content creation
   - Phases: Planning, Outline, Draft, Review, Final
   - Roles: Supervisor, Writer, Editor, Reviewer
   - Outputs: Project outline, Content draft, Final document

3. **Planning Project**
   - Purpose: Strategic planning and project management
   - Phases: Discovery, Analysis, Strategy, Roadmap, Review
   - Roles: Supervisor, Strategist, Analyst, Planner
   - Outputs: Project plan, Strategy document, Roadmap

### Getting Started

1. **Initialize a Project**
   ```bash
   python -m ragers.cli -------- with goal file in /goal populated from goal template in templates/{project_type}
   python -m ragers.cli --name "My Project" --type code
   ```

2. **Generate Project Documents**
   ```bash
   python -m ragers.cli --name "My Project" --type write
   ```

### Project Structure

Each project type follows a consistent structure:

```
project_name/
├── config/
│   └── project_config.yaml
├── meetings/
│   ├── phase_1/
│   ├── phase_2/
│   └── ...
├── deliverables/
│   ├── technical_design.md
│   ├── architecture.md
│   └── ...
└── goals.md
```

### Configuration

Project types are defined in `ragers/templates/project_types.yaml`, which specifies:
- Project type name and description
- Configuration file location
- Templates directory
- Project phases
- Required roles
- Output files

Each project type has its own configuration file in its respective templates directory.

### Usage

1. **Initialize a Project**
   ```python
   from ragers.project_start import ProjectStart
   
   project = ProjectStart()
   project.initialize_project("My Project", "code")
   ```

2. **Run Project Meetings**
   ```python
   from ragers.project_work import ProjectWork
   
   work = ProjectWork(project.project_path, "code")
   work.run_all_meetings()
   ```

3. **Generate Documents**
   ```python
   from ragers.project_documents import ProjectDocuments
   
   docs = ProjectDocuments()
   docs.load_document_config("code")
   docs.generate_document("technical_design", context)
   ```

### Requirements

- Python 3.8+
- PyYAML
- Pathlib

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### License

MIT License

### Command Line Interface

The framework provides a command-line interface for easy project management:

```bash
# Create a project with default type (code)
python -m ragers.cli --name "my_project"

# Create a project with specific type
python -m ragers.cli --name "my_project" --type "code"
```

#### Command Line Arguments

- `--name` or `-n`: Project name (required)
- `--type` or `-t`: Project type (optional, defaults to "code")

#### Example Workflow

1. Create a new code project:
   ```bash
   python -m ragers.cli --name "my_project" --type "code"
   ```

2. Create a writing project:
   ```bash
   python -m ragers.cli --name "my_document" --type "write"
   ```

3. Create a planning project:
   ```bash
   python -m ragers.cli --name "my_plan" --type "plan"
   ```

#### Project Types

The framework supports different project types, with "code" being the default:

1. **Code Project** (default) project_type: "code"
   - Purpose: Software development projects
   - Phases: Strategy, Kickoff, Architecture, Modules, Review
   - Roles: Supervisor, Manager, Developer, Tester
   - Outputs: Technical design, Architecture, Test plan, Code modules

2. **Writing Project** project_type: "write"
   - Purpose: Documentation and content creation
   - Phases: Planning, Outline, Draft, Review, Final
   - Roles: Supervisor, Writer, Editor, Reviewer
   - Outputs: Project outline, Content draft, Final document

3. **Planning Project**  project_type: "plan"
   - Purpose: Strategic planning and project management
   - Phases: Discovery, Analysis, Strategy, Roadmap, Review
   - Roles: Supervisor, Strategist, Analyst, Planner
   - Outputs: Project plan, Strategy document, Roadmap