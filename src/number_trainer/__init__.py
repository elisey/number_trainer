"""
Number Trainer - Mathematical trainer for learning arithmetic.

Main components:
- core: business logic and data models
- gui: graphical interface on tkinter
- cli: console interface
- web: web interface with FastAPI
"""

__version__ = "0.1.0"
__author__ = "Number Trainer Team"

from .core.models import Exercise, Operation, Result
from .core.trainer import MathTrainer

__all__ = ["Exercise", "Result", "Operation", "MathTrainer"]
