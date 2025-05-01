# LitLegos

LitLegos is an AI-powered book generation system that creates structured, engaging content based on provided outlines and style specifications. It's designed to produce high-quality written content with consistent tone, style, and narrative flow.

 Ragers -> [YAMLgen Adapters,  Autocode, APIs]  -> Deliverable (raw or upload to destination app)

## Overview

LitLegos transforms a table of contents and style specifications into a complete book. It's particularly useful for:
- Business and technical documentation
- Educational materials
- Thought leadership content
- Automated content generation

Key features:
- Customizable writing style and tone
- Consistent narrative flow
- Chapter-by-chapter generation
- Progress tracking and callbacks
- Test mode for quick validation

## Future Features - /todo
Full yaml spec for in-dpeth, nuanced specification of book.(litlegos.yaml) This requires development of generator.py.

## Architecture

```
apis/litlegos/
├── core/             # Core functionality
│   ├── generator.py  # Main generation logic
│   └── __init__.py
├── run_autocoder_book.py  # Example usage script
└── __init__.py
```

### Core Components

#### Generator
The main class that handles book generation with the following capabilities:
- Paragraph generation
- Chapter creation
- Full book assembly
- Style and tone management
- Progress tracking

## Usage

### Basic Usage

```python
from litlegos.core.generator import Generator

# Initialize generator
gen = Generator(
    style_profile="Genius poet with an MBA",
    narrative_rhythm="Confusion > clarity > empowerment",
    target_reader="Skeptical but open-minded executive",
    arc="pedagogical progression",
    flavor="startup rebel with enterprise polish"
)

# Generate a book
toc = [
    "Introduction",
    "Core Concepts",
    "Advanced Topics",
    "Conclusion"
]

prompt = "Write in a professional yet engaging tone, focusing on practical applications."

full_book = gen.generate_book(
    toc=toc,
    prompt=prompt,
    on_chapter_complete=lambda i, title, text: print(f"✅ Chapter {i}: {title} generated.")
)
```

### Configuration Options

The Generator class accepts several configuration parameters:

- `style_profile`: Writing style (default: "Genius poet with an MBA")
- `narrative_rhythm`: Story progression (default: "Confusion > clarity > empowerment")
- `target_reader`: Intended audience (default: "Skeptical but open-minded executive")
- `arc`: Narrative structure (default: "pedagogical progression")
- `flavor`: Overall tone (default: "startup rebel with enterprise polish")
- `test_mode`: Enable test mode for shorter outputs (default: False)

### Using tech_spec

The `tech_spec` parameter is a dictionary that allows you to define the complete book generation specification in one place. It's particularly useful when working with Ragers or other automated systems.

```python
tech_spec = {
    # Required: List of chapter titles
    "toc": [
        "Introduction",
        "Core Concepts",
        "Advanced Topics",
        "Conclusion"
    ],
    
    # Required: Main writing prompt/instructions
    "prompt": "Write in a professional yet engaging tone, focusing on practical applications.",
    
    # Optional: Enable test mode for shorter outputs
    "test_mode": False,
    
    # Optional: Style overrides
    "style_profile": "Technical writer with storytelling flair",
    "narrative_rhythm": "Problem > Solution > Implementation",
    "target_reader": "Technical team lead",
    "arc": "Technical progression",
    "flavor": "Clear and concise with practical examples"
}

# Initialize generator with tech_spec
gen = Generator(
    style_profile=tech_spec.get("style_profile"),
    narrative_rhythm=tech_spec.get("narrative_rhythm"),
    target_reader=tech_spec.get("target_reader"),
    arc=tech_spec.get("arc"),
    flavor=tech_spec.get("flavor"),
    test_mode=tech_spec.get("test_mode", False)
)

# Generate book using tech_spec
full_book = gen.generate_book(
    toc=tech_spec["toc"],
    prompt=tech_spec["prompt"],
    on_chapter_complete=lambda i, title, text: print(f"✅ Chapter {i}: {title} generated.")
)
```

#### tech_spec Parameters

1. **Required Parameters**:
   - `toc`: List of chapter titles (strings)
   - `prompt`: Main writing instructions/guidelines

2. **Optional Parameters**:
   - `test_mode`: Boolean to enable test mode (default: False)
   - `style_profile`: Override default writing style
   - `narrative_rhythm`: Override default story progression
   - `target_reader`: Override default audience
   - `arc`: Override default narrative structure
   - `flavor`: Override default tone

3. **Best Practices**:
   - Always include `toc` and `prompt`
   - Use test_mode=True for initial validation
   - Keep style parameters consistent
   - Consider chapter flow in TOC order

### Example Script

See `run_autocoder_book.py` for a complete example of book generation:

```python
from litlegos.core.generator import Generator

tech_spec = {
    "toc": [
        "Customer Experience",
        "Process Automation",
        "Data-Driven Decision Making",
        # ... more chapters
    ],
    "prompt": "Channel Obama + Jobs + Ziglar. Tone must be presidential, poetic, strategic.",
    "test_mode": False
}

gen = Generator(test_mode=tech_spec["test_mode"])
full_book = gen.generate_book(
    toc=tech_spec["toc"],
    prompt=tech_spec["prompt"],
    on_chapter_complete=lambda i, title, text: print(f"✅ Chapter {i}: {title} generated.")
)
```

## Help

### Common Issues

1. **Style Consistency**
   - Ensure your style profile and prompt are well-defined
   - Use consistent terminology throughout the TOC

2. **Chapter Generation**
   - Each chapter title should be clear and specific
   - Consider the logical flow between chapters

3. **Output Formatting**
   - Generated content includes markdown formatting
   - Use appropriate markdown viewers for preview

### Best Practices

1. **Planning**
   - Create a detailed TOC before generation
   - Define clear style parameters
   - Consider your target audience

2. **Generation**
   - Start with test_mode=True for quick validation
   - Use the on_chapter_complete callback for progress tracking
   - Review each chapter as it's generated

3. **Post-Processing**
   - Review generated content for consistency
   - Add any necessary formatting or structure
   - Consider adding a table of contents

## Development

### Adding Features

1. Create a feature branch
2. Implement changes in the Generator class
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

### Testing

- Use test_mode=True for quick validation
- Verify style consistency across chapters
- Check formatting and structure
- Validate against different TOC structures 