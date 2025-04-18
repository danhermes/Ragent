import logging
from typing import Dict, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)
VALID_ROLES = ["python_dev", "n8n_dev", "writer", "proofreader", "dev_writer"]

def __init__(self, test_layer=None):
    self.test_layer = test_layer

@dataclass
class RolePrompt:
    name: str
    description: str
    system_message: str
    temperature: float
    max_tokens: int
    api_tool: Optional[str] = None
    test_layer: Optional[object] = None 

    @classmethod
    def get_instance(cls, key: str, test_layer=None) -> "RolePrompt":
        try:
            logger.debug(f"[RolePrompt] Initializing role: {key}")
            data = ROLES[key]
            return cls(**data, test_layer=test_layer)
        except KeyError:
            raise ValueError(f"No such role: {key}")

ROLES = {
    "python_dev": {
        "name": "Python Developer",
        "description": "Expert Python programmer for code generation",
        "system_message": """You are a precise, efficient, and modern Python programmer.
Include appropriate function definitions, docstrings, and any required imports. Use simple, maintainable structures.
Output only the Python code block, no explanation or commentary.
""",
        "temperature": 0.3,
        "max_tokens": 1000,
        "api_tool": "python"
    },
    "n8n_dev": {
        "name": "n8n Developer",
        "description": "Expert in n8n workflow automation",
        "system_message": "You are an expert n8n workflow developer specializing in automation and integration.",
        "temperature": 0.3,
        "max_tokens": 1000,
        "api_tool": "n8n"
    },
    "writer": {
        "name": "Content Writer",
        "description": "Expert content writer and author",
        "system_message": "You are an expert content writer and author specializing in engaging, well-structured content.",
        "temperature": 0.7,
        "max_tokens": 4000,
        "api_tool": "content"
    },
    "proofreader": {
        "name": "Proofreader",
        "description": "Expert in editing and proofreading",
        "system_message": "You are an expert proofreader specializing in improving clarity, grammar, and style.",
        "temperature": 0.3,
        "max_tokens": 2000,
        "api_tool": "content"
    },
    "dev_writer": {
        "name": "Developer Writer",
        "description": "Expert in both development and content creation",
        "system_message": """You are a Developer Writer, uniquely skilled in both software development and content creation.
Your primary focus is on generating high-quality written content, but you understand that code is often the tool needed to create that content.

The code you create must reflect a publishing pipeline, where:
1. Your technical architecture will be a means to creating a structured publication comprised of high quality writing. 
2. Each class or method represents part of the publication's content structure.
3. Your code will be a means to write text: sentences, paragraphs, chapters, and publications.  
4. The pipeline's sole purpose is to produce high-quality copy
5. Code organization mirrors the structure of the final publication
6. Technical implementation serves the narrative flow
7. Classes work together to maintain consistency and quality

When generating content:
1. Quality and accuracy of the writing is paramount
2. Code is a means to an end - it exists to serve the content
3. Technical implementation details should be clean and efficient
4. The final deliverable must be engaging, well-structured, and error-free

You excel at:
- Creating engaging, well-structured content
- Writing clean, efficient code to support content generation
- Ensuring technical accuracy while maintaining readability
- Balancing technical requirements with narrative flow
- Maintaining consistent tone and style throughout
- Structuring code to reflect the publication's organization
- Building a pipeline that enhances content quality

Remember: The code you write exists to serve the content. While the code must be correct and efficient, the quality of the written output is the ultimate measure of success. The class structure should be a direct reflection of the publication's organization, with each component working together to produce the highest quality copy possible.""",
        "temperature": 0.5,
        "max_tokens": 1000,
        "api_tool": "content"
    }
}

def determine_role(task: str, test_layer=None) -> RolePrompt:
    """Determine the appropriate role based on the task description
    
    Args:
        task: The task description
        
    Returns:
        Role: The most appropriate role for the task
    """
    task_lower = task.lower()
    
    # Check for role-specific keywords
    role_keywords = {
        "python_dev": ["python", "code", "script", "function", "class", "module"],
        "n8n_dev": ["n8n", "workflow", "automation", "integration"],
        "writer": ["book", "chapter", "story", "narrative", "content", "write", "author"],
        "proofreader": ["edit", "proofread", "review", "improve", "polish"],
        "dev_writer": [
            "book", "chapter", "story", "narrative", "content", "write", "author",
            "pipeline prompt", "chapter_1", "chapter_2", "front matter", "back matter",
            "customer experience", "process automation", "transformational story",
            "python", "code", "script", "function", "class", "module",
            "publish", "publication", "pipeline", "structure", "organization"
        ]
    }
    
    # Count matches for each role
    role_matches = {
        role_name: sum(1 for keyword in keywords if keyword in task_lower)
        for role_name, keywords in role_keywords.items()
    }
    
    # Get role with most matches
    best_role = max(role_matches.items(), key=lambda x: x[1])[0]
    
    # If no matches found, default to python_dev
    if role_matches[best_role] == 0:
        return RolePrompt(**ROLES["python_dev"], test_layer=test_layer)
        
    role_config = ROLES[best_role]

    return RolePrompt(**role_config, test_layer=test_layer)

def get_code_generation_prompt(task: str, test_layer=None) -> str:
    """Generate a prompt based on the task and determined role
    
    Args:
        task: The task description
        
    Returns:
        str: The generated prompt
    """
    logger.debug(f"Generating prompt for task: {task}")

    test_note = ""
    if test_layer and test_layer.enabled:
        test_note = """

Note: In test mode, assume a `test_layer` object is available. Use these methods for simulated results:
- `test_layer.chatgpt(prompt)`
- `test_layer.db_read(query)`
- `test_layer.db_write(query, result)`
- `test_layer.file_read(key)`
- `test_layer.file_write(key, content)`
- `test_layer.put(key, value)`
- `test_layer.get(key)`
Use these in place of live I/O, external APIs, or GPT calls when possible.
"""  
    # Determine the appropriate role
    role = determine_role(task)
    logger.debug(f"Selected role: {role.name}")
    
    # Generate role-specific prompt
    prompt = f"""
{role.system_message}

IMPORTANT: The output MUST follow these rules:
1. Follow the exact structure and requirements specified
2. Maintain the specified tone and style throughout
3. Use the exact language and examples provided in the specification
4. Ensure proper formatting and organization
5. Include all required sections and elements
6. Maintain consistency in voice and perspective
7. Follow any specific formatting or style guidelines provided
8. Ensure proper transitions between sections
9. Include all necessary details while maintaining readability
10. Adhere to any word count or length requirements

You will create content based on this specification:

{task}{test_note}
"""
    
    logger.debug(f"Generated prompt length: {len(prompt)}")
    return prompt

