import os
import sys
from typing import Dict, Optional
from pathlib import Path
import logging

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from apis.autocoder.agent.build_cycle_agent import AgentBuildCycle

class AutomationAdapter:
    """Adapter that bridges ragers automation requirements with autocoder's AgentBuildCycle"""
    
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger("automation_adapter")
        # Initialize with empty task, will be updated in generate_workflow
        self.agent_cycle = AgentBuildCycle({
            "language": "n8n",
            "requirements": {},
            "specifications": {}
        })
        
    def generate_workflow(self, requirements: Dict, specifications: Dict) -> Optional[Path]:
        """Generate workflow using AgentBuildCycle based on ragers requirements"""
        try:
            # Update task for AgentBuildCycle
            self.agent_cycle.agent_task = {
                "language": "n8n",
                "requirements": requirements,
                "specifications": specifications
            }
            
            # Run AgentBuildCycle to generate workflow
            result = self.agent_cycle.run_cycle()
            
            if not result or "workflow_file" not in result:
                self.logger.error("AgentBuildCycle failed to generate workflow")
                return None
                
            return Path(result["workflow_file"])
            
        except Exception as e:
            self.logger.error(f"Error generating workflow: {str(e)}")
            return None 