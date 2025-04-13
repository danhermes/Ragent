from .base import BaseMode
from .plan import PlanMode
from .automate import AutomateMode
from .proof import ProofMode

__all__ = ['BaseMode', 'PlanMode', 'AutomateMode', 'ProofMode']

# Set default mode
DEFAULT_MODE = PlanMode 