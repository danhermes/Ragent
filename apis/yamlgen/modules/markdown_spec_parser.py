from typing import Dict
from pathlib import Path

class MarkdownSpecParser:
    """Parses a Markdown Automation Tech Spec into a structured section dictionary."""

    def __init__(self, path: str):
        self.path = Path(path)
        self.sections: Dict[str, str] = {}

    def load(self) -> Dict[str, str]:
        current_heading = None
        content_buffer = []

        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if line.startswith("## "):  # New heading
                    if current_heading:
                        self.sections[current_heading] = "\n".join(content_buffer).strip()
                        content_buffer = []
                    current_heading = line.replace("##", "").strip()

                elif current_heading:
                    content_buffer.append(line)

        if current_heading:
            self.sections[current_heading] = "\n".join(content_buffer).strip()

        return self.sections
