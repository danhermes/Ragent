# Running the Orchestrator

This document explains how to run the AI Agent Orchestrator with various options and configurations.

## Available Modes

The orchestrator supports different modes of operation:

### Plan Mode
```bash
python run_orchestrator.py --mode plan
```
- Focuses on strategic planning and goal setting
- Helps define project scope and requirements
- Generates high-level project plans

### Automate Mode
```bash
python run_orchestrator.py --mode automate
```
- Focuses on automation and workflow optimization
- Helps identify repetitive tasks for automation
- Generates automation scripts and workflows

### Proof Mode
```bash
python run_orchestrator.py --mode proof
```
- Focuses on testing and validation
- Helps verify requirements and functionality
- Generates test cases and validation reports

### Develop Mode
```bash
python run_orchestrator.py --mode develop
```
- Focuses on technical design and implementation
- Helps with architecture and code design
- Generates technical specifications and code examples
- Reviews technical requirements and challenges
- Designs system architecture and components
- Provides implementation details and testing strategies

## Basic Usage

### Run All Phases in Sequence
```bash
python run_orchestrator.py
```
This will run through all phases in order:
- Strategic goal setting
- Company kickoff
- Project creation
- Worker collaboration
- Work loop
- Present deliverables

### Run a Specific Phase
```bash
# Run just the strategic goal setting
python run_orchestrator.py --phase strategic-goals

# Run just the kickoff meeting
python run_orchestrator.py --phase kickoff

# Run just project creation
python run_orchestrator.py --phase project-creation

# Run just worker collaboration
python run_orchestrator.py --phase worker-collaboration

# Run just the work loop
python run_orchestrator.py --phase work-loop

# Run just deliverable presentation
python run_orchestrator.py --phase present-deliverables
```

### Run Milestone Review
```bash
python run_orchestrator.py --phase milestone-review --milestone "Phase 1"
```

### Handle Upward Communication
```bash
python run_orchestrator.py --message "Need clarification on requirements" --sender "Steve"
```

### Use Custom Goals
```bash
python run_orchestrator.py --goals "Build scalable AI system with $10K investment"
```

### Combine Options
```bash
# Run milestone review with custom goals
python run_orchestrator.py --phase milestone-review --milestone "Phase 1" --goals "Build scalable AI system"

# Handle upward communication during work loop
python run_orchestrator.py --phase work-loop --message "Need help" --sender "Bill"
```

### View Help
```bash
python run_orchestrator.py --help
```
This will show all available options and their descriptions.

## Important Notes

1. **Directory Structure**
   - Make sure you're in the directory containing `run_orchestrator.py`
   - The `.goals` file should be in the same directory

2. **Logging**
   - All logs will be written to `orchestrator.log`
   - Real-time output is visible in the console
   - Each phase is logged with timestamps

3. **Available Phases**
   - `all`: Run all phases in sequence
   - `strategic-goals`: Run strategic goal setting
   - `kickoff`: Run company kickoff
   - `project-creation`: Run project creation
   - `worker-collaboration`: Run worker collaboration
   - `milestone-review`: Run milestone review (requires --milestone)
   - `work-loop`: Run work loop
   - `present-deliverables`: Run deliverable presentation

4. **Required Arguments**
   - `--milestone`: Required for milestone review phase
   - `--message` and `--sender`: Required for upward communication

5. **Optional Arguments**
   - `--goals`: Override goals from .goals file
   - `--phase`: Specify which phase to run

## Example Workflows

### Complete Project Cycle
```bash
# 1. Set strategic goals
python run_orchestrator.py --phase strategic-goals

# 2. Run kickoff meeting
python run_orchestrator.py --phase kickoff

# 3. Create projects
python run_orchestrator.py --phase project-creation

# 4. Review milestone
python run_orchestrator.py --phase milestone-review --milestone "Initial Planning"

# 5. Run work loop
python run_orchestrator.py --phase work-loop

# 6. Present deliverables
python run_orchestrator.py --phase present-deliverables
```

### Quick Review and Update
```bash
# Review milestone and handle communication
python run_orchestrator.py --phase milestone-review --milestone "Phase 1" --message "Need clarification" --sender "Steve"
```

## Troubleshooting

1. **File Not Found**
   - Ensure you're in the correct directory
   - Check that all required files exist

2. **Missing Arguments**
   - Use `--help` to see required arguments
   - Provide all required arguments for the chosen phase

3. **Logging Issues**
   - Check file permissions for `orchestrator.log`
   - Ensure console output is not redirected 