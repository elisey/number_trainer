"""
Тесты для модуля core математического тренажера.

Содержит тесты для классов MathTrainer, Exercise, Result и Operation.
"""

import pytest

from src.number_trainer.core.models import Exercise, Operation, Result
from src.number_trainer.core.trainer import MathTrainer


class TestMathTrainer:
    """Тесты для класса MathTrainer"""

    def test_init_default_params(self):
        """Тест инициализации с параметрами по умолчанию"""
        trainer = MathTrainer()
        assert trainer.min_digits == 1
        assert trainer.max_digits == 3
        assert trainer.current_exercise is None
        assert trainer.stats["total_exercises"] == 0
        assert trainer.stats["correct_answers"] == 0
        assert trainer.stats["incorrect_answers"] == 0

    def test_init_custom_params(self):
        """Тест инициализации с пользовательскими параметрами"""
        trainer = MathTrainer(min_digits=2, max_digits=3)
        assert trainer.min_digits == 2
        assert trainer.max_digits == 3

    def test_init_invalid_params(self):
        """Тест инициализации с некорректными параметрами"""
        # Проверяем коррекцию параметров
        trainer = MathTrainer(min_digits=0, max_digits=5)
        assert trainer.min_digits == 1  # Исправлено до минимума
        assert trainer.max_digits == 3  # Исправлено до максимума

        # Проверяем случай когда min > max
        trainer = MathTrainer(min_digits=3, max_digits=1)
        assert trainer.min_digits == 1  # Должно быть исправлено
        assert trainer.max_digits == 1

    def test_generate_number_one_digit(self):
        """Тест генерации однозначного числа"""
        trainer = MathTrainer()
        for _ in range(10):  # Проверяем несколько раз
            number = trainer._generate_number(1)
            assert 1 <= number <= 9

    def test_generate_number_two_digits(self):
        """Тест генерации двузначного числа"""
        trainer = MathTrainer()
        for _ in range(10):
            number = trainer._generate_number(2)
            assert 10 <= number <= 99

    def test_generate_number_three_digits(self):
        """Тест генерации трехзначного числа"""
        trainer = MathTrainer()
        for _ in range(10):
            number = trainer._generate_number(3)
            assert 100 <= number <= 999

    def test_generate_number_invalid_digits(self):
        """Тест генерации числа с некорректным количеством цифр"""
        trainer = MathTrainer()
        with pytest.raises(ValueError):
            trainer._generate_number(0)
        with pytest.raises(ValueError):
            trainer._generate_number(4)

    def test_generate_exercise(self):
        """Тест генерации упражнения"""
        trainer = MathTrainer(min_digits=1, max_digits=2)
        exercise = trainer.generate_exercise()

        # Проверяем что упражнение создано
        assert exercise is not None
        assert isinstance(exercise, Exercise)
        assert trainer.current_exercise == exercise

        # Проверяем корректность данных
        assert exercise.first_number > 0
        assert exercise.second_number > 0
        assert exercise.operation in [Operation.ADDITION, Operation.SUBTRACTION]

        # Проверяем правильность вычисления ответа
        if exercise.operation == Operation.ADDITION:
            expected = exercise.first_number + exercise.second_number
        else:  # SUBTRACTION
            expected = exercise.first_number - exercise.second_number

        assert exercise.correct_answer == expected
        assert exercise.correct_answer >= 0  # Результат не должен быть отрицательным

    def test_generate_exercise_subtraction_positive_result(self):
        """Тест что вычитание всегда дает положительный результат"""
        trainer = MathTrainer()

        # Генерируем много упражнений чтобы проверить разные случаи
        for _ in range(50):
            exercise = trainer.generate_exercise()
            if exercise.operation == Operation.SUBTRACTION:
                assert exercise.correct_answer >= 0
                assert exercise.first_number >= exercise.second_number

    def test_check_answer_correct(self):
        """Тест проверки правильного ответа"""
        trainer = MathTrainer()
        exercise = trainer.generate_exercise()

        result = trainer.check_answer(exercise, exercise.correct_answer)

        assert isinstance(result, Result)
        assert result.is_correct is True
        assert result.user_answer == exercise.correct_answer
        assert result.correct_answer == exercise.correct_answer
        assert "Правильно" in result.message

        # Проверяем обновление статистики
        assert trainer.stats["total_exercises"] == 1
        assert trainer.stats["correct_answers"] == 1
        assert trainer.stats["incorrect_answers"] == 0

    def test_check_answer_incorrect(self):
        """Тест проверки неправильного ответа"""
        trainer = MathTrainer()
        exercise = trainer.generate_exercise()
        wrong_answer = exercise.correct_answer + 1

        result = trainer.check_answer(exercise, wrong_answer)

        assert isinstance(result, Result)
        assert result.is_correct is False
        assert result.user_answer == wrong_answer
        assert result.correct_answer == exercise.correct_answer
        assert "Неправильно" in result.message
        assert str(exercise.correct_answer) in result.message

        # Проверяем обновление статистики
        assert trainer.stats["total_exercises"] == 1
        assert trainer.stats["correct_answers"] == 0
        assert trainer.stats["incorrect_answers"] == 1

    def test_check_answer_no_exercise(self):
        """Тест проверки ответа с None упражнением"""
        trainer = MathTrainer()

        # Теперь API требует упражнение как параметр, поэтому тестируем с None
        with pytest.raises(AttributeError):
            trainer.check_answer(None, 42)

    def test_get_current_exercise_text(self):
        """Тест получения текста текущего упражнения"""
        trainer = MathTrainer()

        # Без упражнения
        assert trainer.get_current_exercise_text() == "Нет активного упражнения"

        # С упражнением
        exercise = trainer.generate_exercise()
        text = trainer.get_current_exercise_text()
        assert str(exercise.first_number) in text
        assert str(exercise.second_number) in text
        assert exercise.operation.value in text
        assert "=" in text
        assert "?" in text

    def test_get_stats_empty(self):
        """Тест получения статистики без упражнений"""
        trainer = MathTrainer()
        stats = trainer.get_stats()

        assert stats["total_exercises"] == 0
        assert stats["correct_answers"] == 0
        assert stats["incorrect_answers"] == 0
        assert stats["accuracy"] == 0.0

    def test_get_stats_with_exercises(self):
        """Тест получения статистики с упражнениями"""
        trainer = MathTrainer()

        # Решаем несколько упражнений
        for _ in range(4):
            exercise = trainer.generate_exercise()
            trainer.check_answer(exercise, exercise.correct_answer)  # Правильный ответ

        exercise = trainer.generate_exercise()
        trainer.check_answer(
            exercise, exercise.correct_answer + 1
        )  # Неправильный ответ

        stats = trainer.get_stats()
        assert stats["total_exercises"] == 5
        assert stats["correct_answers"] == 4
        assert stats["incorrect_answers"] == 1
        assert stats["accuracy"] == 80.0

    def test_reset_stats(self):
        """Тест сброса статистики"""
        trainer = MathTrainer()

        # Создаем некоторую статистику
        exercise = trainer.generate_exercise()
        trainer.check_answer(exercise, exercise.correct_answer)

        assert trainer.stats["total_exercises"] == 1

        # Сбрасываем
        trainer.reset_stats()

        assert trainer.stats["total_exercises"] == 0
        assert trainer.stats["correct_answers"] == 0
        assert trainer.stats["incorrect_answers"] == 0

    def test_set_difficulty(self):
        """Тест установки сложности"""
        trainer = MathTrainer()

        trainer.set_difficulty(2, 3)
        assert trainer.min_digits == 2
        assert trainer.max_digits == 3

        # Тест коррекции некорректных значений
        trainer.set_difficulty(0, 5)
        assert trainer.min_digits == 1
        assert trainer.max_digits == 3

        # Тест случая min > max
        trainer.set_difficulty(3, 1)
        assert trainer.min_digits == 1
        assert trainer.max_digits == 1


class TestExercise:
    """Тесты для класса Exercise"""

    def test_exercise_str_addition(self):
        """Тест строкового представления упражнения на сложение"""
        exercise = Exercise(5, 3, Operation.ADDITION, 8)
        assert str(exercise) == "5 + 3 = ?"

    def test_exercise_str_subtraction(self):
        """Тест строкового представления упражнения на вычитание"""
        exercise = Exercise(10, 4, Operation.SUBTRACTION, 6)
        assert str(exercise) == "10 - 4 = ?"


class TestResult:
    """Тесты для класса Result"""

    def test_result_creation(self):
        """Тест создания объекта Result"""
        result = Result(
            is_correct=True, user_answer=8, correct_answer=8, message="Правильно!"
        )

        assert result.is_correct is True
        assert result.user_answer == 8
        assert result.correct_answer == 8
        assert result.message == "Правильно!"


class TestOperation:
    """Тесты для enum Operation"""

    def test_operation_values(self):
        """Тест значений операций"""
        assert Operation.ADDITION.value == "+"
        assert Operation.SUBTRACTION.value == "-"

    def test_operation_list(self):
        """Тест получения списка операций"""
        operations = list(Operation)
        assert len(operations) == 2
        assert Operation.ADDITION in operations
        assert Operation.SUBTRACTION in operations


# Интеграционные тесты
class TestIntegration:
    """Интеграционные тесты для полного цикла работы"""

    def test_full_training_session(self):
        """Тест полной сессии тренировки"""
        trainer = MathTrainer(min_digits=1, max_digits=2)

        # Симулируем сессию из 5 упражнений
        correct_count = 0
        for i in range(5):
            exercise = trainer.generate_exercise()
            assert exercise is not None

            # Иногда отвечаем правильно, иногда нет
            if i % 2 == 0:
                result = trainer.check_answer(exercise, exercise.correct_answer)
                assert result.is_correct is True
                correct_count += 1
            else:
                result = trainer.check_answer(exercise, exercise.correct_answer + 1)
                assert result.is_correct is False

        # Проверяем финальную статистику
        stats = trainer.get_stats()
        assert stats["total_exercises"] == 5
        assert stats["correct_answers"] == correct_count
        assert stats["incorrect_answers"] == 5 - correct_count

        expected_accuracy = round((correct_count / 5) * 100, 1)
        assert stats["accuracy"] == expected_accuracy

    def test_difficulty_affects_generation(self):
        """Тест влияния сложности на генерацию упражнений"""
        # Легкий уровень
        easy_trainer = MathTrainer(min_digits=1, max_digits=1)
        easy_exercises = [easy_trainer.generate_exercise() for _ in range(10)]

        # Сложный уровень
        hard_trainer = MathTrainer(min_digits=3, max_digits=3)
        hard_exercises = [hard_trainer.generate_exercise() for _ in range(10)]

        # Проверяем что числа в легких упражнениях меньше
        for exercise in easy_exercises:
            assert 1 <= exercise.first_number <= 9
            assert 1 <= exercise.second_number <= 9

        # Проверяем что числа в сложных упражнениях больше
        for exercise in hard_exercises:
            assert 100 <= exercise.first_number <= 999
            assert 100 <= exercise.second_number <= 999
