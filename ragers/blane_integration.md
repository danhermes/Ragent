# Blane Integration with Ragers Framework

This document outlines how Blane (the strategic personal assistant and project manager) integrates with and calls the Ragers framework.

## Documentation Reference

- **Primary Documentation**: `ragers/readme.md`
- **Additional Resources**: See `docs/ragers.md` for more detailed documentation

## Communication Format

Blane should use a concise, friendly director format by default, providing minimal but actionable information. When users specifically request "verbose" mode, Blane can switch to providing detailed explanations with full section headers.

- **Default Mode**: Concise, direct statements with minimal explanation
- **Verbose Mode**: Triggered when user requests "verbose", "more detail", "explain more", etc.
- **Toggle Mechanism**: Returns to concise mode for next interaction unless verbose is requested again

See `HQ/blane_ui_design.md` for complete communication format guidelines.

## Core Commands

To call Ragers from Blane, use the following command structure:

```bash
python -m ragers.cli --goal <goal_file> --type <project_type>
```

### Command Parameters:

- `--goal`: Path to the goal file (optional, defaults to searching in /goal directory)
- `--type`: Project type (optional, defaults to "code")

### Example Commands:

```bash
# Run a specific goal file with a specific project type
python -m ragers.cli --goal goal/my_project.goal --type code

# Run with default project type (code)
python -m ragers.cli --goal goal/my_project.goal

# Run all goal files in the /goal directory
python -m ragers.cli
```

## Project Types

Ragers supports the following project types:

1. **code**: Software development projects
   - Focus: Software development
   - Phases: Strategy → Kickoff → Architecture → Modules → Review
   - Outputs: Technical designs, code modules, tests

2. **write**: Documentation and content creation
   - Focus: Documentation and content creation
   - Phases: Planning → Outline → Draft → Review → Final
   - Outputs: Project outlines, content drafts, final documents

3. **plan**: Strategic planning
   - Focus: Strategic planning and project management
   - Phases: Discovery → Analysis → Strategy → Roadmap → Review
   - Outputs: Project plans, strategy documents, roadmaps

4. **automate**: Automation workflows
   - Focus: Workflow automation and integration
   - Phases: Requirements → Design → Implementation → Testing → Deployment
   - Outputs: Workflow definitions, integration scripts, documentation

## Goal File Management

### File Structure and Naming Convention

- **Location**: All goal files should be stored in the `/ragers/goal/` directory
- **Naming Convention**: `<project_name>.goal`
- **Format**: Markdown with YAML-like sections

### Goal File Template

```markdown
# Project Name
[Project Name]

## Summary
[Brief project description]

## Project Type
[code|write|plan|automate]

## Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Deliverables
- [Deliverable 1]
- [Deliverable 2]
- [Deliverable 3]

## Known Constraints
- [Constraint 1]
- [Constraint 2]

## Definition of Done
- [Completion criteria]

## Phases and Milestones
- Phase 1: [Description]
- Phase 2: [Description]
- Phase 3: [Description]

## Preferred Meeting Format
[Meeting format preference]

## Review Requirements
[Review process details]
```

### Goal File Creation Process

1. Create a new file in the `/ragers/goal/` directory with the `.goal` extension
2. Use the template above to define project parameters
3. Ensure all required sections are completed
4. Save the file with a descriptive project name

## Ragers Directory Structure

```
ragers/
├── templates/           # Project and document templates
│   ├── code/           # Software development templates
│   ├── write/          # Documentation templates
│   ├── plan/           # Planning templates
│   ├── automate/       # Automation templates
│   └── project_types.yaml
├── goal/               # Project goal definitions
├── projects/           # Active projects
├── logs/               # System and project logs
├── utils/              # Framework utilities
├── cli.py              # Command-line interface
├── main.py             # Main orchestration logic
├── project_start.py    # Project initialization
└── project_work.py     # Project execution
```

## SPARC Workflow Integration

Blane should integrate the SPARC workflow methodology when working with Ragers:

### SPARC Workflow Steps

1. **Specification**:
   - Clarify goals, scope, constraints, and acceptance criteria
   - Create detailed goal files with clear objectives and deliverables
   - Never hard-code environment variables or sensitive information

2. **Pseudocode**:
   - Request high-level logic with TDD anchors
   - Identify core functions and data structures
   - Create pseudocode documentation before implementation

3. **Architecture**:
   - Design extensible diagrams and clear service boundaries
   - Define interfaces between components
   - Ensure proper separation of concerns

4. **Refinement**:
   - Iterate with TDD, debugging, security checks, and optimization loops
   - Refactor for maintainability
   - Ensure code quality and performance

5. **Completion**:
   - Integrate, document, monitor, and schedule continuous improvement
   - Verify against acceptance criteria
   - Ensure all deliverables meet requirements

### SPARC Mode Assignment

When working with complex projects, Blane can assign specialized subtasks using the appropriate modes:

- **spec-pseudocode**: For initial specification and pseudocode development
- **architect**: For system architecture and design
- **code**: For implementation and coding
- **tdd**: For test-driven development
- **debug**: For troubleshooting and fixing issues
- **security-review**: For security analysis and hardening
- **docs-writer**: For documentation creation
- **integration**: For system integration
- **post-deployment-monitoring**: For monitoring deployed systems
- **refinement-optimization**: For performance optimization

## Integration Workflow

1. **Goal Definition**:
   - Blane creates or identifies a goal file based on project requirements
   - Goal file is placed in the `/ragers/goal/` directory

2. **Project Type Selection**:
   - Blane determines the appropriate project type based on requirements
   - Project type is specified in the goal file and command

3. **SPARC Workflow Application**:
   - Apply the SPARC methodology to structure the project workflow
   - Assign specialized modes for complex subtasks as needed

4. **Command Execution**:
   - Blane executes the Ragers command with the appropriate parameters
   - Ragers processes the command and initializes the project

5. **Project Monitoring**:
   - Blane monitors project progress through logs and generated documents
   - Provides strategic insights and adjustments as needed

6. **Deliverable Management**:
   - Blane organizes and tracks deliverables generated by Ragers
   - Ensures all project assets are properly categorized and accessible