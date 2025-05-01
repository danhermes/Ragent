**Template File:** `code_meeting_architecture.md`

### Meeting protocol — a consistent set of prompts or headings — that Ragers follow every time they write a report. Think of it as a technical version of Robert's Rules of Order, but for agent engineers.
Each topic becomes a section, and each section produces *atomic*, *reusable*, *agent-runnable* material.
---

# Ragent Meeting Agenda - Architecture Design
**Date:**  
**Phase:** Meeting | In Progress | Final  
**Owner:** 

---

## Goals
- What are we building or solving?
- What constraints or mandates exist?
- What will success look like?

---

## System Architecture
- System Overview
- Component Breakdown (with names)
- Data flow or control logic summary
- Known constraints (compute, file I/O, agent memory, etc.)

### Components
| Module | Role |
|--------|------|
|        |      |

## Handoff Notes to Implementation

- Each module described above should be implemented as a class or callable module.
- Prefer functional interfaces where shared state is avoided unless explicitly noted.
- Use consistent naming conventions across modules and methods.
- Maintain compatibility with JSON-based I/O and CLI interaction using `argparse`.
- Stub or placeholder methods must be marked with `[TODO]` and include comments describing expected behavior.
- Unit test stubs should be generated alongside each method, with edge cases listed or outlined.
- All inputs and outputs must be typed, documented, and validated where appropriate.

---

## Code Snippets
```python
def print():
    stuff = [
        "things and stuff"
    ]

    print(f"- {stuff}")
...
print()
```

```yaml
module:
  name: ""
  purpose: ""
  inputs: []
  outputs: []
  methods: []
  notes: ""
```

---

## Test Plan
- Test coverage requirements
- Testing approach
- Key test scenarios

---

## Risks & Constraints
- Technical risks
- Style/narrative constraints
- Test mode limitations
- Potential conflicts or edge cases

---

## Blockers & Decisions
- Any unresolved technical or creative blockers?
- Any forks in direction that need resolution?

---

## Files
| Type | Path |
|------|------|
|      |      |

---

## Assignments
| Agent | Task | Due |
|-------|------|-----|
|       |      |     |

---

## Next Steps
- Who's doing what?
- What's the next deliverable?
- When's the next checkpoint?

---

Extra Meeting Prompt (to enforce this during meetings)
> "Please conduct this design meeting using the following structure: Goals, Architecture, Code Specs, Risks, Blockers, and Next Steps. Use tight formatting, eliminate narrative fluff, and keep code clean and executable."