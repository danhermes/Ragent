# Ragers Prompt System Documentation

## Overview

The Ragers framework uses a sophisticated prompt system to guide AI agents through structured project meetings and ensure alignment between project goals and deliverables. This document explains how prompts are used across different project modes and how the prompt groups integration enhances project outcomes.

## Core Prompt Architecture

### 1. Project Mode Configuration

Each project mode (code, plan, write, automate) has its own configuration file:
- `ragers/templates/{mode}/{mode}_mode.yaml` - Defines project structure, meetings, phases, and roles
- `ragers/templates/{mode}/{mode}_prompts.yaml` - Contains the prompts used in meetings

### 2. Meeting Templates

Meetings are the primary mechanism for project progression in Ragers. Each meeting:
- Has a specific phase (e.g., discovery, design, implementation)
- Uses templates to structure agent interactions
- Produces output documents that become inputs to subsequent meetings

### 3. Prompt Processing Flow

When a meeting is run:
1. The system loads the appropriate prompt template for the current phase
2. Context data (goals, history, files) is gathered and injected into the template
3. The formatted prompt is sent to the appropriate agent(s)
4. Responses are collected and used to generate meeting documents

## Prompt Groups Integration

### Purpose

Prompt groups are structured sets of prompts designed to address specific aspects of project alignment. They ensure that:
- All file formats mentioned in goals have detailed specifications
- Project phases map directly to technical components
- Integration specifications are complete
- Implementation details are concrete
- Security considerations are comprehensive
- Consistency is maintained across documents
- Deliverables are implementation-ready

### Structure

Each prompt group contains:
- A name and description
- A set of specific prompts
- Applicable phases where the prompts should be applied
- Project type applicability (which modes should use the group)

### Integration Method

The prompt groups are integrated into the Ragers framework through:

1. **Direct Template Integration**
   - Prompt groups are embedded directly in phase-specific templates in `code_prompts.yaml`
   - This allows them to be processed by the existing code without modifications

2. **Checkpoint Configuration**
   - Checkpoints are defined for key transition points:
     - Pre-phase transition
     - Pre-deliverable completion
     - Post-review
   - Each checkpoint specifies which prompt groups should be applied

## Project Mode-Specific Prompt Usage

### Code Mode

Code mode uses the most comprehensive set of prompt groups:
- File format specification (kickoff, design phases)
- Phase-component mapping (design, implementation phases)
- Integration specification (design, implementation phases)
- Implementation detail (implementation phase)
- Security model (design, implementation phases)
- Consistency verification (review phase)
- Deliverable validation (implementation, review phases)

### Plan Mode

Plan mode focuses on strategic alignment:
- Phase-component mapping
- Consistency verification
- Deliverable validation

### Write Mode

Write mode emphasizes document consistency:
- Consistency verification
- Deliverable validation

### Automate Mode

Automate mode prioritizes integration and implementation:
- File format specification
- Integration specification
- Implementation detail
- Security model
- Consistency verification
- Deliverable validation

## How Prompts Are Processed

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

## Conclusion

The Ragers prompt system provides a structured approach to guiding AI agents through project development. The integration of prompt groups enhances this system by ensuring comprehensive coverage of all aspects needed for successful project delivery, particularly the alignment between goals and deliverables.

By embedding prompt groups directly in the phase templates, they become an integral part of the meeting process without requiring code changes. This approach maintains backward compatibility while significantly improving the quality and completeness of project deliverables.