# Project Mode Prompts in Ragers

## Overview

Ragers supports multiple project modes, each with its own set of prompts tailored to the specific needs of that mode. This document explains how prompts are structured and used in each project mode.

## Common Prompt Structure

Regardless of the project mode, prompts in Ragers follow a common structure:

1. **Phase-specific templates** - Each project phase has a template that guides agent interactions
2. **Meeting rules** - Define how meetings should be conducted
3. **Document meeting prompts** - Used to generate meeting documents

## Project Modes and Their Prompts

### Code Mode

Code mode is focused on software development and uses the most comprehensive set of prompts.

#### Configuration Files
- `ragers/templates/code/code_mode.yaml` - Project structure, meetings, phases
- `ragers/templates/code/code_prompts.yaml` - Prompts for meetings

#### Key Phases
1. **Strategy** - High-level planning and goal setting
2. **Kickoff** - Project initialization and requirement gathering
3. **Design** - Technical design and architecture
4. **Implementation** - Code implementation and module development
5. **Review** - Final review and validation

#### Prompt Groups Used
- File format specification (kickoff, design phases)
- Phase-component mapping (design, implementation phases)
- Integration specification (design, implementation phases)
- Implementation detail (implementation phase)
- Security model (design, implementation phases)
- Consistency verification (review phase)
- Deliverable validation (implementation, review phases)

#### Example Prompt (Design Phase)
```
# Technical Design Meeting

## Goals
  {goal_summary}

## Input Document 
  {input}
### Project Charter:
  {input_files}

## Task
Create a comprehensive technical design document with a target length of {length}.

1. **System Architecture**
  - Define the overall system architecture and component relationships
  - Specify communication patterns between components
  - Document technology stack and framework choices
  - Create deployment architecture diagram

# ... additional sections ...

9. **Security Model**
  - Define the authentication and authorization model for all system interfaces
  - Document data protection requirements for sensitive information
  - Specify audit logging requirements for security-relevant operations
  - Create a threat model identifying potential vulnerabilities and mitigations
```

### Plan Mode

Plan mode is focused on strategic planning and project management.

#### Configuration Files
- `ragers/templates/plan/plan_mode.yaml` - Project structure, meetings, phases
- `ragers/templates/plan/plan_prompts.yaml` - Prompts for meetings

#### Key Phases
1. **Discovery** - Initial project discovery and requirements gathering
2. **Analysis** - Data analysis and findings
3. **Strategy** - Strategic planning and approach definition
4. **Roadmap** - Detailed roadmap and implementation planning
5. **Review** - Final strategy review and approval

#### Prompt Groups Used
- Phase-component mapping
- Consistency verification
- Deliverable validation

#### Example Prompt (Strategy Phase)
```
# Strategy Development Meeting

## Goals
  {goal_summary}

## Input Document 
  {input}
### Analysis Document:
  {input_files}

## Task
Create a comprehensive strategic approach document with a target length of {length}.

1. **Strategic Vision**
  - Define the long-term vision and strategic objectives
  - Align strategic goals with organizational mission
  - Identify key success metrics and outcomes

# ... additional sections ...

5. **Implementation Approach**
  - Map each strategic component to its corresponding project phase
  - Ensure each phase has concrete implementation details
  - Document how each phase's outputs become inputs to subsequent phases
```

### Write Mode

Write mode is focused on content creation and documentation.

#### Configuration Files
- `ragers/templates/write/write_mode.yaml` - Project structure, meetings, phases
- `ragers/templates/write/write_prompts.yaml` - Prompts for meetings

#### Key Phases
1. **Discovery** - Content requirements and audience analysis
2. **Outline** - Content structure and organization
3. **Draft** - Initial content creation
4. **Review** - Content review and refinement
5. **Finalize** - Final editing and publication preparation

#### Prompt Groups Used
- Consistency verification
- Deliverable validation

#### Example Prompt (Draft Phase)
```
# Content Draft Meeting

## Goals
  {goal_summary}

## Input Document 
  {input}
### Content Outline:
  {input_files}

## Task
Create a comprehensive draft document with a target length of {length}.

1. **Content Development**
  - Develop each section according to the approved outline
  - Ensure consistent tone and style throughout the document
  - Include all required information identified in the discovery phase

# ... additional sections ...

4. **Consistency Check**
  - Verify that all terminology is used consistently throughout the document
  - Ensure all references and citations are properly formatted
  - Check that all sections align with the original content requirements
```

### Automate Mode

Automate mode is focused on automation and workflow development.

#### Configuration Files
- `ragers/templates/automate/automate_mode.yaml` - Project structure, meetings, phases
- `ragers/templates/automate/automate_prompts.yaml` - Prompts for meetings

#### Key Phases
1. **Discovery** - Automation requirements and process analysis
2. **Design** - Workflow design and integration planning
3. **Implementation** - Automation implementation and testing
4. **Deployment** - Deployment planning and execution
5. **Review** - Performance review and optimization

#### Prompt Groups Used
- File format specification
- Integration specification
- Implementation detail
- Security model
- Consistency verification
- Deliverable validation

#### Example Prompt (Implementation Phase)
```
# Automation Implementation Meeting

## Goals
  {goal_summary}

## Input Document 
  {input}
### Automation Design:
  {input_files}

## Task
Create a comprehensive implementation document with a target length of {length}.

1. **Implementation Details**
  - Provide complete method signatures for all components
  - Define internal data structures used by each component
  - Document state transitions and persistence requirements
  - Specify performance requirements and optimization strategies

# ... additional sections ...

5. **Integration Implementation**
  - Define the complete API contract for each external system integration
  - Document authentication and authorization requirements
  - Specify data transformation rules between system formats
  - Create error handling protocols for integration failures
```

## How Prompts Are Processed

Regardless of the project mode, prompts are processed in the same way:

1. **Loading**
   - `ProjectWork.run_meeting()` loads prompts from `{mode}_prompts.yaml`
   - The template for the current phase is extracted

2. **Context Preparation**
   - Meeting context is assembled including:
     - Project goals
     - Conversation history
     - Input/output files
     - Phase-specific data

3. **Template Formatting**
   - The template is formatted with the context using a safe formatter
   - This includes any embedded prompt groups for the current phase

4. **Agent Interaction**
   - The formatted prompt is sent to the appropriate agent
   - The agent processes the prompt and returns a response

5. **Document Generation**
   - Responses are collected and used to generate meeting documents
   - These documents become inputs to subsequent meetings

## Prompt Groups Across Modes

The table below shows which prompt groups are used in each project mode:

| Prompt Group | Code | Plan | Write | Automate |
|--------------|------|------|-------|----------|
| File Format Specification | ✓ |  |  | ✓ |
| Phase-Component Mapping | ✓ | ✓ |  |  |
| Integration Specification | ✓ |  |  | ✓ |
| Implementation Detail | ✓ |  |  | ✓ |
| Security Model | ✓ |  |  | ✓ |
| Consistency Verification | ✓ | ✓ | ✓ | ✓ |
| Deliverable Validation | ✓ | ✓ | ✓ | ✓ |

## Conclusion

Ragers uses a flexible prompt system that adapts to the needs of different project modes. By structuring prompts according to project phases and incorporating appropriate prompt groups, Ragers ensures that each project mode receives the guidance needed to produce high-quality deliverables that align with project goals.

The integration of prompt groups enhances this system by ensuring comprehensive coverage of all aspects needed for successful project delivery, particularly the alignment between goals and deliverables.