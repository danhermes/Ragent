# run_autocoder_book.py
# AutoCoder-driven book generation using LitLegos

import sys
sys.path.append("F:/DEV/Ragent/apis")
from litlegos.core.generator import Generator

# Simulated tech_spec output from RAgent
tech_spec = {
    "toc": [
        "Customer Experience",
        "Process Automation",
        "Data-Driven Decision Making",
        "Innovation and Product Development",
        "Workforce Transformation",
        "Risk Management and Compliance",
        "Prompting AI Transformation"
    ],
    "prompt": "Channel Obama + Jobs + Ziglar. Tone must be presidential, poetic, strategic. Write to a skeptical but open-minded executive. No bullets. Let metaphor and example carry the lesson.",
    "test_mode": False
}

def run_book_production():
    gen = Generator(test_mode=tech_spec["test_mode"])
    full_book = gen.generate_book(
        toc=tech_spec["toc"],
        prompt=tech_spec["prompt"],
        on_chapter_complete=lambda i, title, text: print(f"✅ Chapter {i}: {title} generated.")
    )
    with open("ChatGPT_for_Business_FULL_BOOK.md", "w", encoding="utf-8") as f:
        f.write(full_book)
    print("\n🎉 Book generation complete. Draft saved to 'ChatGPT_for_Business_FULL_BOOK.md'.")

if __name__ == "__main__":
    run_book_production()
