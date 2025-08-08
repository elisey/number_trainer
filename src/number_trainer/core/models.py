"""
Модели данных для математического тренажера.

Содержит основные структуры данных:
- Operation: перечисление математических операций
- Exercise: модель математического упражнения
- Result: модель результата проверки ответа
"""

from enum import Enum
from dataclasses import dataclass


class Operation(Enum):
    """Математические операции"""
    ADDITION = "+"
    SUBTRACTION = "-"


@dataclass
class Exercise:
    """Математическое упражнение"""
    first_number: int
    second_number: int
    operation: Operation
    correct_answer: int
    
    def __str__(self) -> str:
        return f"{self.first_number} {self.operation.value} {self.second_number} = ?"


@dataclass
class Result:
    """Результат проверки ответа"""
    is_correct: bool
    user_answer: int
    correct_answer: int
    message: str
