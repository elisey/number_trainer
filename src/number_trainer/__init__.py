"""
Number Trainer - Математический тренажер для изучения арифметики.

Основные компоненты:
- core: бизнес-логика и модели данных
- gui: графический интерфейс на tkinter
- cli: консольный интерфейс
"""

__version__ = "0.1.0"
__author__ = "Number Trainer Team"

from .core.models import Exercise, Result, Operation
from .core.trainer import MathTrainer

__all__ = ["Exercise", "Result", "Operation", "MathTrainer"]
