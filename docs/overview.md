# Ragents System Documentation

## Overview

Ragents is a comprehensive AI development platform that combines multiple components to create, test, and deploy AI solutions. The system consists of several main components:

1. **Ragers** - The core orchestration system
2. **Picar** - Robotics control system
3. **APIs** - Various integration points including:
   - Autocoder
   - n8n
   - Proof

## System Architecture

```
ragents/
├── ragers/           # Core orchestration system
├── picar/            # Robotics control
├── apis/             # API integrations
│   ├── autocoder/    # Code generation
│   ├── n8n/          # Workflow automation
│   └── proof/        # Verification system
├── docs/             # Documentation
└── tests/            # Test suite
```

## Component Details

### Ragers
The core orchestration system that manages the entire development lifecycle. It includes:
- Strategic goal setting
- Project management
- Worker collaboration
- Deliverable generation
- Milestone tracking

### Picar
A robotics control system for Raspberry Pi that provides:
- Motor control
- Sensor integration
- Audio capabilities
- GPIO management

### APIs

#### Autocoder
An AI-powered code generation system that:
- Generates Python code from requirements
- Creates n8n workflows
- Handles testing and validation

#### n8n
Workflow automation integration that:
- Creates and manages workflows
- Handles API integrations
- Manages automation tasks

#### Proof
A verification system that:
- Validates generated code
- Ensures requirements are met
- Provides quality assurance

## Getting Started

1. Clone the repository
2. Install dependencies
3. Configure environment variables
4. Run the orchestrator

For detailed setup instructions, see the individual component documentation.

## Development Workflow

1. Set strategic goals
2. Run kickoff meeting
3. Create projects
4. Review milestones
5. Run work loop
6. Present deliverables

## Support and Resources

- Documentation: /docs
- Examples: /examples
- Tests: /tests 