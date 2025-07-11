# Prompt Groups Integration

## Overview

This document explains how prompt groups are integrated into the Ragers framework to ensure alignment between project goals and deliverables without requiring code changes.

## Integration Approach

The prompt groups are integrated directly into the existing prompt structure that Ragers already processes, rather than requiring new code to handle them separately. This approach maintains backward compatibility while enhancing the quality and completeness of project deliverables.

### Key Integration Points

1. **Direct Template Embedding**
   - Prompt groups are embedded directly in phase-specific templates in `code_prompts.yaml`
   - This allows them to be processed by the existing code without modifications

2. **Alignment Section in YAML**
   - A dedicated `alignment_prompt_groups` section in `code_prompts.yaml` contains all prompt groups
   - This section serves as a reference and documentation for the prompt groups

3. **Checkpoint Configuration**
   - An `alignment_checkpoints` section defines when prompt groups should be applied
   - These checkpoints correspond to existing phase transitions in the Ragers workflow

## Implementation Details

### 1. Prompt Groups Structure

Each prompt group in the `alignment_prompt_groups` section includes:
- A name and description
- A set of specific prompts
- Applicable phases where the prompts should be applied

Example:
```yaml
file_format_specification:
  name: "File Format Specification Prompts"
  description: "Ensure detailed specifications for all file formats mentioned in goals"
  applicable_phases: ["kickoff", "design"]
  prompts:
    - "Define the complete schema for {file_format} including all required and optional fields"
    - "Provide sample JSON/YAML for {file_format} showing typical usage patterns"
    # Additional prompts...
```

### 2. Integration into Phase Templates

The prompt groups are integrated into phase templates by including the relevant prompts directly in the template content. For example, in the `design` phase template:

```yaml
design:
  description: "Technical design meeting"
  # Other configuration...
  template: |
    # Technical Design Meeting
    
    ## Goals
      {goal_summary}
    
    # ... other template content ...
    
    ## Technical Components
    
    For each component, provide:
    
    1. **Component Specification**
      - Define the complete schema for each file format including all required and optional fields
      - Provide sample JSON/YAML for each file format showing typical usage patterns
      - Specify validation rules for each file format to ensure data integrity
    
    # ... other template content ...
```

### 3. Checkpoint Configuration

The `alignment_checkpoints` section defines when specific prompt groups should be applied:

```yaml
alignment_checkpoints:
  pre_phase_transition:
    required: true
    prompt_groups:
      - consistency_verification
  
  pre_deliverable_completion:
    required: true
    prompt_groups:
      - deliverable_validation
```

These checkpoints correspond to existing phase transitions in the Ragers workflow, so they can be processed without code changes.

## How It Works in Practice

When a meeting is run:

1. The system loads the appropriate prompt template for the current phase from `code_prompts.yaml`
2. The template already contains the relevant prompt groups embedded within it
3. The template is formatted with context data and sent to the appropriate agent
4. The agent processes the prompt (including the embedded prompt groups) and returns a response
5. The response is used to generate meeting documents

This approach ensures that prompt groups are applied at the appropriate phases without requiring changes to the code that processes prompts.

## Benefits of This Approach

1. **No Code Changes Required**
   - Utilizes the existing prompt processing mechanism
   - Maintains backward compatibility

2. **Flexibility**
   - Prompt groups can be easily modified or extended in the YAML file
   - New prompt groups can be added without code changes

3. **Documentation**
   - The `alignment_prompt_groups` section serves as documentation for the prompt groups
   - The structure makes it clear which prompts apply to which phases

4. **Improved Alignment**
   - Ensures comprehensive coverage of all aspects needed for successful project delivery
   - Addresses gaps between project goals and deliverables

## Conclusion

By embedding prompt groups directly in the phase templates, they become an integral part of the meeting process without requiring code changes. This approach maintains backward compatibility while significantly improving the quality and completeness of project deliverables.