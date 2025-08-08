"""
Core модуль - содержит основную бизнес-логику математического тренажера.

Компоненты:
- models: модели данных (Exercise, Result, Operation)
- trainer: основной класс MathTrainer
"""

from .models import Exercise, Operation, Result
from .trainer import MathTrainer

__all__ = ["Exercise", "Result", "Operation", "MathTrainer"]
