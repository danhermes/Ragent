from .base import BaseMode
from .plan import PlanMode
from .automate import AutomateMode
from .proof import ProofMode
from .develop import DevelopMode

__all__ = ['BaseMode', 'PlanMode', 'AutomateMode', 'ProofMode', 'DevelopMode', 'DEFAULT_MODE']

# Set default mode
DEFAULT_MODE = PlanMode 