# Code – Topics review Template - Review

**Template File:** `meeting_topics_draft.md`

### Meeting protocol — a consistent set of prompts or headings — that Ragers follow every time they write a report. Think of it as a technical version of Robert’s Rules of Order, but for agent engineers.
Each topic becomes a section, and each section produces *atomic*, *reusable*, *agent-runnable* material.
---

# Ragent Meeting Agenda - Architecture
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
### Overview
- System Overview  
- Component Breakdown (with names)  
- Data flow or control logic summary  
- Known constraints (compute, file I/O, agent memory, etc.)

### Components 
Example: 
| Module         | Role                       |
|----------------|----------------------------|
| ChapterWriter  | Creates markdown chapters  |
| PromptRefactor | Refines structure and tone |
| Logger         | Writes to console + file   |

---

## Code Snippets  
Each subsystem should be described like this:
EXAMPLE: 
```yaml
- Module: ChapterWriter
  Purpose: Generates markdown chapter files based on a selected theme and prompt structure
  Inputs: chapter_number, theme, word_limit, template_options
  Outputs: Markdown file, console log, dated log file
  Methods:
    - setup_logging()
    - select_template()
    - generate_prompts()
    - write_chapter(test_mode)
  Notes: Ensures no template repeats between chapters

---

## Test Plan  
- [ ] 100-word test mode works  
- [ ] Template selection random, no repeats  
- [ ] Output files generated correctly

---

#### **Risks & Constraints**
- Technical risks
- Style/narrative constraints
- Test mode limitations
- Potential conflicts or edge cases

---

#### **Blockers / Decisions Needed**
- Any unresolved technical or creative blockers?
- Any forks in direction that need resolution?

---

## Files  
EXAMPLES:
- Prompt source: `book.goal`  
- Script: `chapter_writer.py`  
- Output: `chapter_1.md`, `log_0418.txt`

---

## Assignments  
EXAMPLE:
| Agent | Task                   | Due   |
|-------|------------------------|--------|
| Dee   | Prompt breakdown       | Day 1 |
| Woz   | Script scaffolding     | Day 2 |
| Dum   | Style enforcement test | Day 3 |

---

#### **Next Steps**
- Who’s doing what?
- What’s the next deliverable?
- When’s the next checkpoint?

---

Extra Meeting Prompt (to enforce this during meetings)
> “Please conduct this design meeting using the following structure: Goals, Architecture, Code Specs, Risks, Blockers, and Next Steps. Use tight formatting, eliminate narrative fluff, and keep code clean and executable.”