# Blane's Guide to Using Ragers

## Overview

This guide provides comprehensive instructions for Blane on how to use the Ragers framework effectively. As the strategic personal assistant and project manager, Blane is responsible for orchestrating projects through the Ragers system.

## Starting a Ragers Session

To start a session about Ragers that Blane will understand without additional context, use one of these trigger phrases:

- "Let's work with Ragers"
- "I need to use Ragers for a project"
- "Start Ragers for [project type]"
- "Create a new Ragers project"
- "Run Ragers with [goal file]"

Blane will immediately recognize these phrases and switch to Ragers mode, providing appropriate guidance and options for proceeding with Ragers operations.

Example conversation starters:
```
"Let's work with Ragers for a new code project."
"I need to use Ragers to create a documentation project."
"Start Ragers for planning a new strategy."
"Create a new Ragers project for automation."
"Run Ragers with the project_factory.goal file."
```

## Core Command Structure

The primary way to interact with Ragers is through the CLI command:

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

Ragers supports four main project types, each with its own workflow and deliverables:

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

### File Structure and Location

- **Location**: All goal files should be stored in the `/ragers/goal/` directory
- **Naming Convention**: `<project_name>.goal`
- **Format**: Markdown with structured sections

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

## SPARC Workflow Integration

When working with Ragers, follow the SPARC workflow methodology:

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

## Integration Workflow

1. **Goal Definition**:
   - Create or identify a goal file based on project requirements
   - Place goal file in the `/ragers/goal/` directory

2. **Project Type Selection**:
   - Determine the appropriate project type based on requirements
   - Specify project type in the goal file and command

3. **SPARC Workflow Application**:
   - Apply the SPARC methodology to structure the project workflow
   - Assign specialized modes for complex subtasks as needed

4. **Command Execution**:
   - Execute the Ragers command with the appropriate parameters
   - Ragers processes the command and initializes the project

5. **Project Monitoring**:
   - Monitor project progress through logs and generated documents
   - Provide strategic insights and adjustments as needed

6. **Deliverable Management**:
   - Organize and track deliverables generated by Ragers
   - Ensure all project assets are properly categorized and accessible

## Communication Format

When communicating about Ragers projects, follow these guidelines:

### Default Mode (Concise)

- Brief, direct statements (1-2 sentences max per point)
- Bullet points for multiple items
- Minimal explanations - focus on what to do, not why
- Action-oriented language
- Brief pleasantries - Good evening, sir. JARVIS style
- Occasional wit - clever delivery of information, occasional sarcasm

Example:
```
Project ready. 3 tasks pending:
• Update database schema
• Test API endpoints
• Deploy to staging

Need approval to proceed.
```

### Verbose Mode (On Request)

When user explicitly requests "verbose" mode:

- Detailed explanations with context and reasoning
- Complete section headers as defined in .roomodes
- Technical details and implementation considerations
- Strategic insights and alternatives
- Full PROJECT OVERVIEW, ASSET MANAGEMENT, TASK AUTOMATION, STRATEGIC INSIGHTS, NEXT STEPS sections

Example:
```
PROJECT OVERVIEW:
The database migration project is ready to proceed with 3 remaining tasks. The schema changes have been validated against the test dataset and all preliminary checks have passed.

ASSET MANAGEMENT:
All migration scripts are stored in /db/migrations/ with appropriate versioning. Backup procedures are in place with snapshots stored in the secure S3 bucket.

TASK AUTOMATION:
The CI/CD pipeline has been configured to run the migration scripts automatically after approval. Rollback procedures are included in case of failure.

STRATEGIC INSIGHTS:
This migration addresses the performance bottlenecks identified in the last quarter review. Expected performance improvement is 30-40% for key queries.

NEXT STEPS:
1. Update database schema using the migration scripts
2. Test API endpoints against the new schema
3. Deploy changes to staging environment for final validation

Approval is required before proceeding with the production deployment.
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**:
   - Check that all required Python packages are installed
   - Verify that the Ragers framework is properly installed

2. **Configuration Errors**:
   - Ensure that the `.env` file contains all required environment variables
   - Check that the goal file is properly formatted

3. **API Connection Issues**:
   - Verify API keys and credentials
   - Check network connectivity

4. **File Permission Problems**:
   - Ensure that the user has proper permissions to read/write files
   - Check that the goal file is accessible

### Solutions

1. **Check Installation**:
   - Run `pip install -r requirements.txt` to install dependencies
   - Verify that the Ragers framework is in the Python path

2. **Verify Configuration**:
   - Check the `.env` file for missing or incorrect values
   - Ensure that the goal file follows the required format

3. **Test API Connections**:
   - Use test commands to verify API connectivity
   - Check API documentation for correct usage

4. **Check File Permissions**:
   - Ensure that the user has proper permissions to access files
   - Verify that the goal file is not locked by another process