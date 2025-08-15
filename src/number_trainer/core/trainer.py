"""
Main class of mathematical trainer.

Contains logic for generating exercises, checking answers, and maintaining statistics.
"""

import random
from typing import cast

from .models import Exercise, Operation, Result


class MathTrainer:
    """
    Class for generating mathematical exercises and checking answers.
    Completely independent of GUI - works only with data.
    """

    def __init__(self, min_digits: int = 1, max_digits: int = 3):
        """
        Trainer initialization

        Args:
            min_digits: Minimum number of digits in numbers (1-3)
            max_digits: Maximum number of digits in numbers (1-3)
        """
        self.min_digits = max(1, min(min_digits, 3))
        self.max_digits = max(1, min(max_digits, 3))

        if self.min_digits > self.max_digits:
            self.min_digits = self.max_digits

        self.current_exercise: Exercise | None = None
        self.stats = {
            "total_exercises": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
        }

    def _generate_number(self, digits: int) -> int:
        """
        Generates a random number with specified number of digits

        Args:
            digits: Number of digits (1-3)

        Returns:
            Random number
        """
        if digits == 1:
            return random.randint(1, 9)
        elif digits == 2:
            return random.randint(10, 99)
        elif digits == 3:
            return random.randint(100, 999)
        else:
            raise ValueError("Number of digits must be from 1 to 3")

    def generate_exercise(self) -> Exercise:
        """
        Generates a new mathematical exercise

        Returns:
            Exercise object with new exercise
        """
        # Random number of digits for numbers
        digits1 = random.randint(self.min_digits, self.max_digits)
        digits2 = random.randint(self.min_digits, self.max_digits)

        # Generate numbers
        first_number = self._generate_number(digits1)
        second_number = self._generate_number(digits2)

        # Random operation
        operation = random.choice(list(Operation))

        # For subtraction, ensure result is positive
        if operation == Operation.SUBTRACTION and first_number < second_number:
            first_number, second_number = second_number, first_number

        # Calculate correct answer
        if operation == Operation.ADDITION:
            correct_answer = first_number + second_number
        else:  # SUBTRACTION
            correct_answer = first_number - second_number

        self.current_exercise = Exercise(
            first_number=first_number,
            second_number=second_number,
            operation=operation,
            correct_answer=correct_answer,
        )

        return self.current_exercise

    def check_answer(self, exercise: Exercise, user_answer: int, time_taken: float = 0.0) -> Result:
        """
        Checks user answer

        Args:
            exercise: Exercise to check
            user_answer: User answer
            time_taken: Execution time in seconds

        Returns:
            Result object with check result
        """
        is_correct = user_answer == exercise.correct_answer

        # Update statistics
        self.stats["total_exercises"] += 1
        if is_correct:
            self.stats["correct_answers"] += 1
            message = "Correct! Great job!"
        else:
            self.stats["incorrect_answers"] += 1
            message = f"Incorrect. Correct answer: {exercise.correct_answer}"

        return Result(
            is_correct=is_correct,
            user_answer=user_answer,
            correct_answer=exercise.correct_answer,
            message=message,
            time_taken=time_taken,
        )

    def get_current_exercise_text(self) -> str:
        """
        Returns text representation of current exercise

        Returns:
            String with exercise or message about no active exercise
        """
        if self.current_exercise is None:
            return "No active exercise"
        return str(self.current_exercise)

    def get_stats(self) -> dict[str, int | float]:
        """
        Returns training statistics

        Returns:
            Dictionary with statistics
        """
        stats: dict[str, int | float] = cast(dict[str, int | float], self.stats.copy())
        if stats["total_exercises"] > 0:
            stats["accuracy"] = round((stats["correct_answers"] / stats["total_exercises"]) * 100, 1)
        else:
            stats["accuracy"] = 0.0
        return stats

    def reset_stats(self) -> None:
        """Resets training statistics"""
        self.stats = {
            "total_exercises": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
        }

    def set_difficulty(self, min_digits: int, max_digits: int) -> None:
        """
        Sets exercise difficulty

        Args:
            min_digits: Minimum number of digits (1-3)
            max_digits: Maximum number of digits (1-3)
        """
        self.min_digits = max(1, min(min_digits, 3))
        self.max_digits = max(1, min(max_digits, 3))

        if self.min_digits > self.max_digits:
            self.min_digits = self.max_digits
