import logging
from typing import Dict, Any, List
from pathlib import Path

class BaseMode:
    """Base class for all ragent modes"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"mode.{name}")
        self.deliverables_dir = Path("deliverables")
        self.deliverables_dir.mkdir(exist_ok=True)
        
    def initialize(self) -> None:
        """Initialize the mode"""
        self.logger.info(f"Initializing {self.name} mode")
        
    def run_meeting(self, orchestrator: Any) -> None:
        """Run a mode-specific meeting
        
        Args:
            orchestrator: The orchestrator instance
        """
        raise NotImplementedError("Subclasses must implement run_meeting")
        
    def review_deliverables(self, orchestrator: Any) -> None:
        """Review deliverables with managers and workers
        
        Args:
            orchestrator: The orchestrator instance
        """
        raise NotImplementedError("Subclasses must implement review_deliverables")
        
    def generate_deliverable(self, orchestrator: Any) -> Path:
        """Generate and save the mode's deliverable
        
        Args:
            orchestrator: The orchestrator instance
            
        Returns:
            Path to the generated deliverable
        """
        raise NotImplementedError("Subclasses must implement generate_deliverable") 