# Ragers Framework

## Overview
Ragers is a template-driven framework for managing and executing AI-powered projects. It provides a structured approach to project management, team collaboration, and document generation through a system of templates, goals, and automated workflows.

Start up. Create a .goal file and place in /goal directory (see 2. below)
Move into /ragers directory: cd /ragers
Call ragers: 
  python -m ragers.cli --name "code_project_1.goal" --type code
  python -m ragers.cli --type code

## Command Line Interface (CLI)

The Ragers framework provides a command-line interface for project management:

### Basic Usage
```bash
python -m ragers.cli --goal <goal_file> --type <project_type>
```

### Arguments
- `--goal`: Path to the goal file (optional, defaults to searching in /goal directory)
- `--type`: Project type (optional, defaults to "code")

### Project Types
Available project types are defined in `templates/project_types.yaml`:
- `code`: Software development projects
- `write`: Documentation and content creation
- `plan`: Strategic planning
- `automate`: Automation workflows

### Example Commands
```bash
# Run a specific goal file
python -m ragers.cli --goal goal/my_project.goal --type code

# Run with default project type (code)
python -m ragers.cli --goal goal/my_project.goal

# Run all goal files in the /goal directory
python -m ragers.cli
```

### Logging
The CLI automatically creates logs in the `/logs` directory with timestamps:
- Format: `logs/cli_YYYYMMDD_HHMMSS.log`
- Includes debug information and execution status

## Core Components

### 1. Templates
The framework is built around a template system located in `/templates/` with the following structure:
- `project_types.yaml`: Defines available project types and their configurations
- `/code/`: Templates for software development projects
- `/write/`: Templates for documentation and content creation
- `/plan/`: Templates for strategic planning
- `/automate/`: Templates for automation workflows

Each project type defines:
- Required roles
- Project phases
- Expected output files
- Configuration settings

### 2. Goals
Goals are defined in the `/goal/` directory using `.goal` files. These files specify:
- Project name and summary
- Project type
- Objectives and deliverables
- Required tooling
- Stakeholder information
- Constraints and success criteria

### 3. Projects
Projects are managed in the `/projects/` directory. Each project follows a standardized structure:
- Project-specific configuration
- Generated documents
- Logs and outputs
- Team interactions and meeting records

## How to Use the Framework

### 1. Creating a New Project

1. Create a goal file in `/goal/`:
    User the template format found in your /templates/(project type) folder. For project type "code" use code_project_template.goal in the templates /code folder. Copy and fill out the template and move into the /ragers/goal file with a .goal suffix.  The body of the filename will become the project name and project folder name in /projects.

    ex only - see actual .goal template per your project type.
   ```yaml
   # Project Name
   Your Project Name

   ## Summary
   Brief project description

   ## Project Type
   [code|write|plan|automate]

   ## Objectives
   - Objective 1
   - Objective 2

   ## Deliverables
   - Deliverable 1
   - Deliverable 2
   ```

2. The framework will automatically:
   - Create a project directory
   - Initialize required templates
   - Set up logging and documentation structure

### 2. Project Execution

Projects follow a phase-based approach defined in the project type template:

1. **Initialization**
   - Load project configuration
   - Initialize team members
   - Set up logging and documentation

2. **Phase Execution**
   - Each phase has defined agent participants and templates
   - Automated meetings and document generation
   - Progress tracking and validation

3. **Documentation**
   - Automatic generation of required documents
   - Meeting summaries and decisions
   - Progress reports

### 3. Templates

Templates drive the entire framework:

1. **Project Type Templates**
   - Define project structure
   - Specify required roles
   - Outline phases and deliverables

2. **Document Templates**
   - Standardized formats for outputs
   - Automated generation based on project phase
   - Consistent documentation structure

3. **Meeting Templates**
   - Structured team interactions
   - Automated documentation
   - Progress tracking

## Directory Structure

```
ragers/
├── templates/           # Project and document templates
│   ├── code/           # Software development templates
│   ├── write/          # Documentation templates
│   ├── plan/           # Planning templates
│   └── project_types.yaml
├── goal/               # Project goal definitions
├── projects/           # Active projects
├── logs/              # System and project logs
└── utils/             # Framework utilities
```

## Best Practices

1. **Goal Definition**
   - Be specific in objectives
   - Define clear deliverables
   - Specify required tooling and constraints

2. **Template Usage**
   - Follow template structure
   - Maintain consistency in documentation
   - Use appropriate project type

3. **Project Management**
   - Regular progress updates
   - Document all decisions
   - Follow phase structure

## Support

For issues or questions:
1. Check project logs in `/logs/`
2. Review template documentation
3. Consult project-specific documentation 