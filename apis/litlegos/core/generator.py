# generator.py
# Core generation logic for LitLegos publishing system

from datetime import datetime

class Generator:
    def __init__(self, style_profile=None, narrative_rhythm=None, target_reader=None, arc=None, flavor=None, test_mode=False):
        self.style_profile = style_profile or "Genius poet with an MBA"
        self.narrative_rhythm = narrative_rhythm or "Confusion > clarity > empowerment"
        self.target_reader = target_reader or "Skeptical but open-minded executive"
        self.arc = arc or "pedagogical progression"
        self.flavor = flavor or "startup rebel with enterprise polish"
        self.test_mode = test_mode
        self.history = []

    def generate_paragraph(self, topic):
        """Generates a standalone paragraph from a given topic."""
        prompt = f"Write a paragraph about {topic} in the style of {self.style_profile}, with rhythm: {self.narrative_rhythm}. Tone: {self.flavor}."
        if self.test_mode:
            prompt += " Limit to 100 words."
        return self._mock_gpt_response(prompt)

    def generate_chapter(self, chapter_title, format_type="classic", rag_docs=None):
        """Generates a full chapter based on title and format."""
        prompt = f"Write a chapter titled '{chapter_title}' in the '{format_type}' format. Audience: {self.target_reader}. Style: {self.style_profile}. Arc: {self.arc}. Flavor: {self.flavor}."
        if rag_docs:
            prompt += f" Incorporate references from: {', '.join(rag_docs)}."
        if self.test_mode:
            prompt += " Limit to 300 words."
        return self._mock_gpt_response(prompt)

    def generate_book(self, toc, prompt, on_chapter_complete=None):
        """Generates an entire book from a given TOC list of chapter titles."""
        self.history.append(f"Book generation started at {datetime.now().isoformat()}")
        book = []
        for i, chapter in enumerate(toc, 1):
            book.append(f"# Chapter {i}: {chapter}\n")
            chapter_text = self.generate_chapter(chapter)
            book.append(chapter_text + "\n\n\\newpage\n")
        return "\n".join(book)

    def _mock_gpt_response(self, prompt):
        """Mock GPT response for scaffolding and test mode."""
        return f"[Generated Text based on Prompt: {prompt}]"
