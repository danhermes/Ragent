from typing import Dict, Tuple, Optional, List
import logging
from agents.agent_blane import AgentBlane
import json

logger = logging.getLogger(__name__)

class NLPProcessor:
    """Handles natural language processing for command interpretation."""
    
    def __init__(self, api_key: str):
        """Initialize the NLP processor with OpenAI API key."""
        self.blane = AgentBlane()
        self.system_prompt = """You are a command parser for the Ragent dispatch system. 
        Your job is to interpret natural language commands and convert them into structured commands.
        
        Available commands:
        - assign/start/run <type> <project> - Start a new task
        - status/? <task_id> - Check task status
        - pause <task_id> - Pause a running task
        - stop/abort <task_id> - Stop a task
        - resume <task_id> - Resume a paused task
        - where <task_id> - Get task location/context
        - get <task_id> - Retrieve task information
        - code <project> - Start a coding task
        - write <project> - Start a writing task
        - plan <project> - Start a planning task
        - ask <task_id> <question> - Ask a question about a task
        - give <task_id> <information> - Provide information for a task
        
        Task types:
        - code: For coding/development tasks
        - write: For writing/documentation tasks
        - plan: For planning/strategy tasks
        
        Respond in JSON format with:
        {
            "command": "the command name",
            "args": "the arguments string",
            "confidence": 0.0-1.0,
            "explanation": "why you chose this interpretation"
        }"""
    
    def parse_command(self, user_input: str) -> Tuple[str, Optional[str], float, str]:
        """Parse natural language input into command and arguments."""
        try:
            response = self.blane.get_chat_response(
                [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            # Log the response fields
            logger.info(f"OpenAI Response - parse_command:")
            logger.info(f"  Model: {response.model}")
            logger.info(f"  Usage: {response.usage}")
            logger.info(f"  Finish Reason: {response.choices[0].finish_reason}")
            logger.info(f"  Role: {response.choices[0].message.role}")
            
            content = response.choices[0].message.content
            logger.info(f"  Content: {content}")
            
            # Parse the response
            try:
                result = json.loads(content)
                return (
                    result.get("command", ""),
                    result.get("args", None),
                    result.get("confidence", 0.0),
                    result.get("explanation", "")
                )
            except json.JSONDecodeError:
                logger.error(f"Failed to parse OpenAI response as JSON: {content}")
                return "", None, 0.0, "Failed to parse response"

        except Exception as e:
            logger.error(f"Error in parse_command: {e}")
            return "", None, 0.0, str(e)
    
    def get_command_suggestions(self, partial_input: str) -> List[str]:
        """Get command suggestions based on partial input."""
        try:
            response = self.blane.get_chat_response(
                [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Suggest commands for: {partial_input}"}
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            # Log the response fields
            logger.info(f"OpenAI Response:")
            logger.info(f"  Model: {response.model}")
            logger.info(f"  Usage: {response.usage}")
            logger.info(f"  Finish Reason: {response.choices[0].finish_reason}")
            logger.info(f"  Role: {response.choices[0].message.role}")
            
            content = response.choices[0].message.content
            logger.info(f"  Content: {content}")
            
            try:
                suggestions = json.loads(content)
                return suggestions.get("suggestions", [])
            except json.JSONDecodeError:
                logger.error(f"Failed to parse OpenAI response as JSON: {content}")
                return []

        except Exception as e:
            logger.error(f"Error in get_command_suggestions: {e}")
            return [] 