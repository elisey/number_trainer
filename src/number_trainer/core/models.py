"""
Data models for mathematical trainer.

Contains main data structures:
- Operation: enumeration of mathematical operations
- Exercise: exercise data structure
- Result: result data structure
"""

from dataclasses import dataclass
from enum import Enum


class Operation(Enum):
    """Mathematical operations"""

    ADDITION = "+"
    SUBTRACTION = "-"


@dataclass
class Exercise:
    """Mathematical exercise"""

    first_number: int
    second_number: int
    operation: Operation
    correct_answer: int

    def __str__(self) -> str:
        return f"{self.first_number} {self.operation.value} {self.second_number} = ?"


@dataclass
class Result:
    """Answer check result"""

    is_correct: bool
    user_answer: int
    correct_answer: int
    message: str
    time_taken: float = 0.0
