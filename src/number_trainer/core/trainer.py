"""
Основной класс математического тренажера.

Содержит логику генерации упражнений, проверки ответов и ведения статистики.
Полностью независим от GUI - работает только с данными.
"""

import random
from typing import Dict, Optional, Union, cast

from .models import Exercise, Operation, Result


class MathTrainer:
    """
    Класс для генерации математических упражнений и проверки ответов.
    Полностью независим от GUI - работает только с данными.
    """

    def __init__(self, min_digits: int = 1, max_digits: int = 3):
        """
        Инициализация тренажера

        Args:
            min_digits: Минимальное количество цифр в числах (1-3)
            max_digits: Максимальное количество цифр в числах (1-3)
        """
        self.min_digits = max(1, min(min_digits, 3))
        self.max_digits = max(1, min(max_digits, 3))

        if self.min_digits > self.max_digits:
            self.min_digits = self.max_digits

        self.current_exercise: Optional[Exercise] = None
        self.stats = {
            "total_exercises": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
        }

    def _generate_number(self, digits: int) -> int:
        """
        Генерирует случайное число с заданным количеством цифр

        Args:
            digits: Количество цифр (1-3)

        Returns:
            Случайное число
        """
        if digits == 1:
            return random.randint(1, 9)
        elif digits == 2:
            return random.randint(10, 99)
        elif digits == 3:
            return random.randint(100, 999)
        else:
            raise ValueError("Количество цифр должно быть от 1 до 3")

    def generate_exercise(self) -> Exercise:
        """
        Генерирует новое математическое упражнение

        Returns:
            Объект Exercise с новым упражнением
        """
        # Случайное количество цифр для чисел
        digits1 = random.randint(self.min_digits, self.max_digits)
        digits2 = random.randint(self.min_digits, self.max_digits)

        # Генерируем числа
        first_number = self._generate_number(digits1)
        second_number = self._generate_number(digits2)

        # Случайная операция
        operation = random.choice(list(Operation))

        # Для вычитания убеждаемся, что результат положительный
        if operation == Operation.SUBTRACTION and first_number < second_number:
            first_number, second_number = second_number, first_number

        # Вычисляем правильный ответ
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
        Проверяет ответ пользователя

        Args:
            exercise: Упражнение для проверки
            user_answer: Ответ пользователя
            time_taken: Время выполнения в секундах

        Returns:
            Объект Result с результатом проверки
        """
        is_correct = user_answer == exercise.correct_answer

        # Обновляем статистику
        self.stats["total_exercises"] += 1
        if is_correct:
            self.stats["correct_answers"] += 1
            message = "Правильно! Отличная работа!"
        else:
            self.stats["incorrect_answers"] += 1
            message = (
                f"Неправильно. Правильный ответ: {exercise.correct_answer}"
            )

        return Result(
            is_correct=is_correct,
            user_answer=user_answer,
            correct_answer=exercise.correct_answer,
            message=message,
            time_taken=time_taken,
        )

    def get_current_exercise_text(self) -> str:
        """
        Возвращает текстовое представление текущего упражнения

        Returns:
            Строка с упражнением или сообщение об отсутствии упражнения
        """
        if self.current_exercise is None:
            return "Нет активного упражнения"
        return str(self.current_exercise)

    def get_stats(self) -> Dict[str, Union[int, float]]:
        """
        Возвращает статистику тренировок

        Returns:
            Словарь со статистикой
        """
        stats: Dict[str, Union[int, float]] = cast(
            Dict[str, Union[int, float]], self.stats.copy()
        )
        if stats["total_exercises"] > 0:
            stats["accuracy"] = round(
                (stats["correct_answers"] / stats["total_exercises"]) * 100, 1
            )
        else:
            stats["accuracy"] = 0.0
        return stats

    def reset_stats(self) -> None:
        """Сбрасывает статистику тренировок"""
        self.stats = {
            "total_exercises": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
        }

    def set_difficulty(self, min_digits: int, max_digits: int) -> None:
        """
        Устанавливает сложность упражнений

        Args:
            min_digits: Минимальное количество цифр (1-3)
            max_digits: Максимальное количество цифр (1-3)
        """
        self.min_digits = max(1, min(min_digits, 3))
        self.max_digits = max(1, min(max_digits, 3))

        if self.min_digits > self.max_digits:
            self.min_digits = self.max_digits
