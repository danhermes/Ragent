**Template File:** `code_meeting_kickoff.md`

### 🧱 Meeting protocol — a consistent set of prompts or headings — that Ragers follow every time they write a report. Think of it as a technical version of Robert’s Rules of Order, but for agent engineers.
Each topic becomes a section, and each section produces *atomic*, *reusable*, *agent-runnable* material.
---

# Ragent Meeting Agenda - Kickoff
**Date:**  
**Phase:** Meeting | In Progress | Final  
**Owner:** 

---

## 🎯 GOALS
- What is our objective?
- What problems are we trying to solve?
- What will success look like?

---

## 🎯 Requirements  
- What are the business objectives?
- What are the outcomes, workflows, and end results desired?
- What are we building or solving?
- What constraints or mandates exist?

---

## 🧱 Technical Constraints and Limitations
### Overview
- Things that can't be done or will require significtion resources.
- IT and cloud limitations
= performance, latency, and other info

---
## 🧱 Design and Architecture Considerations 
### Overview
- System Overview  
- Component Breakdown (with names)  
- Data flow or control logic summary  
- Known constraints (compute, file I/O, agent memory, etc.)

### High-level Components 
Example: 
| Module         | Role                       |
|----------------|----------------------------|
| ChapterWriter  | Creates markdown chapters  |
| PromptRefactor | Refines structure and tone |
| Logger         | Writes to console + file   |

---

## 🧪 Test Plan  
- [ ] High Level Test Plan Approach
- [ ] Main Areas to test

---

#### 📊 **Risks & Constraints**
- Project risks
- Style/narrative constraints
- Test mode limitations
- Potential conflicts or edge cases

---

#### 🚦 **Blockers / Decisions Needed**
- Any unresolved technical or creative blockers?
- Any forks in direction that need resolution?

---

## 📂 Files  
EXAMPLES:
- Prompt source: `book.goal`  
- Script: `chapter_writer.py`  
- Output: `chapter_1.md`, `log_0418.txt`

---

## ✅ Assignments  
EXAMPLE:
| Agent | Task                   | Due   |
|-------|------------------------|--------|
| Dee   | Prompt breakdown       | Day 1 |
| Woz   | Script scaffolding     | Day 2 |
| Dum   | Style enforcement test | Day 3 |

---

#### ⏱️ **Next Steps**
- Who’s doing what?
- What’s the next deliverable?
- When’s the next checkpoint?

---

Extra Meeting Prompt (to enforce this during meetings)
> “Please conduct this design meeting using the following structure: Goals, Architecture, Code Specs, Risks, Blockers, and Next Steps. Use tight formatting, eliminate narrative fluff, and keep code clean and executable.”