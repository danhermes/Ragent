**Template File:** `code_meeting_modules.md`

### Meeting protocol — a consistent set of prompts or headings — that Ragers follow every time they write a report. Think of it as a technical version of Robert's Rules of Order, but for agent engineers.
Each topic becomes a section, and each section produces *atomic*, *reusable*, *agent-runnable* material.
---

Meeting approach: Define all modules. Loop thru and discuss each in turn.

---
# Ragent Meeting Agenda - Architecture Implementation - Modules
**Date:**  
**Phase:** Meeting | In Progress | Final  
**Owner:** 

---

## Module Name

## Purpose

## Inputs / Outputs

## Interfaces / Dependencies

## Core Methods or Logic (retain all code)

## Notes or Open Questions

---

EXAMPLES:

## Module: ChapterWriter

**Purpose:**  
Generates markdown content for a chapter using selected templates, themes, and word counts. Supports test mode.

**Inputs / Outputs:**  
- Inputs: `chapter_number`, `theme`, `word_limit`, `template_options`  
- Outputs: Markdown string (and optionally saved .md file)

**Interfaces / Dependencies:**  
- Uses: `random` for template selection  
- Depends on: Logger module for output tracking

**Core Methods or Logic:**  
```python
class ChapterWriter:
    def __init__(self, chapter_number, theme, word_limit, template_options):
        self.chapter_number = chapter_number
        self.theme = theme
        self.word_limit = word_limit
        self.template_options = template_options
        self.selected_template = None
        self.prompts = []
        self.logger = self.setup_logging()

    def setup_logging(self):
        # Logs to console and file
        ...

    def select_template(self):
        # Selects a template not previously used
        ...

    def generate_prompts(self, num_prompts=3):
        # Creates thematic prompts for GPT
        ...

    def write_chapter(self, test_mode=False):
        # Returns chapter text of specified word count
        ...
```

**Notes or Open Questions:**  
- Should formatting logic be separate from generation?
- How to persist template memory across longer books?


## Module: Logger

**Purpose:**  
Logs all system activity to console and to a dated log file for traceability.

**Inputs / Outputs:**  
- Inputs: Log messages (strings)  
- Outputs: Console output, file log entry

**Interfaces / Dependencies:**  
- Uses Python `logging` module  
- Writes to local filesystem

**Core Methods or Logic:**  
```python
def setup_logging(self):
    logging.basicConfig(filename=f'chapter_{self.chapter_number}_{datetime.now().strftime("%Y%m%d")}.log', level=logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging.getLogger('ChapterWriter')
```

**Notes or Open Questions:**  
- Should logs be JSON for later parsing?  
- Add logging level (DEBUG, INFO, ERROR)?

## Module: PromptRefactorer (Planned)

**Purpose:**  
To reshape master prompt structure into chapter-specific instructions while preserving voice and tone constraints.

**Inputs / Outputs:**  
- Inputs: Global prompt metadata, style rules, chapter goal  
- Outputs: Chapter prompt string

**Interfaces / Dependencies:**  
- Reads from `.goal` file or embedded prompt object  
- Works with memory/format selection logic

**Core Methods or Logic:**  
_Not yet implemented_

**Notes or Open Questions:**  
- Should this be a callable LLM tool?  
- Where should tone-checking live?


## Module: Main Runner

**Purpose:**  
Coordinates execution of chapters through ChapterWriter instances.

**Inputs / Outputs:**  
- Inputs: chapter configs  
- Outputs: Display and log output

**Interfaces / Dependencies:**  
- Orchestrates all modules above  
- Supports `test_mode`

**Core Methods or Logic:**  
```python
def main(test_mode=False):
    chapter_1 = ChapterWriter(1, "Customer Experience", 2500, templates)
    chapter_2 = ChapterWriter(2, "Process Automation", 3000, templates)

    for chapter in [chapter_1, chapter_2]:
        chapter.select_template()
        chapter.generate_prompts(3)
        text = chapter.write_chapter(test_mode)
        print(text)
```

**Notes or Open Questions:**  
- Should it validate outputs against a schema?  
- Add Markdown file writer method?

---
