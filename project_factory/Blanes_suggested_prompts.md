# RECOMMENDED PROMPT GROUPS

To address the gaps between original goals and project deliverables, I recommend implementing these structured prompt groups for future projects:

## 1. File Format Specification Prompts

**Purpose**: Ensure detailed specifications for all file formats mentioned in goals

**Prompt Group**:
- "Define the complete schema for {file_format} including all required and optional fields"
- "Provide sample JSON/YAML for {file_format} showing typical usage patterns"
- "Specify validation rules for {file_format} to ensure data integrity"
- "Document the relationship between {file_format} and other system file formats"
- "Create a migration path for evolving {file_format} as requirements change"

## 2. Phase-to-Component Mapping Prompts

**Purpose**: Ensure direct alignment between project phases and technical components

**Prompt Group**:
- "For Phase {phase_name}, identify all required technical components and their interactions"
- "Map each component in the technical design to its corresponding project phase"
- "Ensure each phase has concrete implementation details in the technical specification"
- "Verify that transitions between phases are explicitly defined in the component interfaces"
- "Document how each phase's outputs become inputs to subsequent phases"

## 3. Integration Specification Prompts

**Purpose**: Create detailed integration specifications for external systems

**Prompt Group**:
- "Define the complete API contract for integration with {external_system}"
- "Document authentication and authorization requirements for {external_system} integration"
- "Specify data transformation rules between system formats and {external_system} formats"
- "Create error handling protocols for {external_system} integration failures"
- "Develop monitoring and logging requirements for {external_system} interactions"

## 4. Implementation Detail Prompts

**Purpose**: Move from conceptual design to concrete implementation details

**Prompt Group**:
- "Provide complete method signatures for all classes in the {component_name} component"
- "Define internal data structures used by the {component_name} component"
- "Document state transitions and persistence requirements for {component_name}"
- "Specify performance requirements and optimization strategies for {component_name}"
- "Create comprehensive error handling and recovery procedures for {component_name}"

## 5. Security Model Prompts

**Purpose**: Ensure comprehensive security considerations

**Prompt Group**:
- "Define the authentication and authorization model for all system interfaces"
- "Document data protection requirements for sensitive information"
- "Specify audit logging requirements for security-relevant operations"
- "Create a threat model identifying potential vulnerabilities and mitigations"
- "Define security testing procedures to validate implementation"

## 6. Consistency Verification Prompts

**Purpose**: Ensure consistency across all project documents

**Prompt Group**:
- "Verify that all component names are used consistently across all documents"
- "Ensure file paths and directory structures are consistent between design and implementation"
- "Confirm that all interfaces mentioned in one document are fully specified in appropriate documents"
- "Validate that all requirements from the original goals have corresponding design elements"
- "Check that terminology is used consistently throughout all project documentation"

## 7. Concrete Deliverable Validation Prompts

**Purpose**: Ensure deliverables are implementation-ready

**Prompt Group**:
- "For each [TODO] item, provide the specific information needed to complete it"
- "Replace all placeholder code with actual implementation code"
- "Convert all conceptual descriptions to concrete specifications with measurable criteria"
- "Ensure each checklist item has a clear definition of done with verification steps"
- "Provide actual examples for all file formats, APIs, and interfaces"

## Implementation Strategy

These prompt groups should be:
1. Integrated into the Ragers framework as mandatory checkpoints
2. Applied at each phase transition to ensure completeness
3. Used as validation criteria before considering a deliverable complete
4. Incorporated into review processes to identify gaps early

By systematically applying these prompt groups, future projects will maintain stronger alignment between goals and deliverables, with fewer omissions and inconsistencies.