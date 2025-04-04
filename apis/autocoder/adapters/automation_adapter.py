from typing import Dict, Optional
from pathlib import Path
from ..agent_build_cycle import AgentBuildCycle

class AutomationAdapter:
    """Adapter that bridges ragers automation requirements with autocoder's AgentBuildCycle"""
    
    def __init__(self):
        self.agent_cycle = AgentBuildCycle()
        
    def generate_workflow(self, requirements: Dict, specifications: Dict) -> Optional[Path]:
        """Generate workflow using AgentBuildCycle based on ragers requirements"""
        try:
            # Create task for AgentBuildCycle
            task = {
                "type": "n8n_workflow",
                "requirements": requirements,
                "specifications": specifications
            }
            
            # Run AgentBuildCycle to generate workflow
            result = self.agent_cycle.run(task)
            
            if not result or "workflow_file" not in result:
                self.logger.error("AgentBuildCycle failed to generate workflow")
                return None
                
            return Path(result["workflow_file"])
            
        except Exception as e:
            self.logger.error(f"Error generating workflow: {str(e)}")
            return None 