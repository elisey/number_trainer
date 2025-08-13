"""
Tests for core module of mathematical trainer.

Contains tests for MathTrainer, Exercise, Result, and Operation classes.
"""

import pytest

from src.number_trainer.core.models import Exercise, Operation, Result
from src.number_trainer.core.trainer import MathTrainer


class TestMathTrainer:
    """Tests for MathTrainer class"""

    def test_init_default_params(self):
        """Test initialization with default parameters"""
        trainer = MathTrainer()
        assert trainer.min_digits == 1
        assert trainer.max_digits == 3
        assert trainer.current_exercise is None
        assert trainer.stats["total_exercises"] == 0
        assert trainer.stats["correct_answers"] == 0
        assert trainer.stats["incorrect_answers"] == 0

    def test_init_custom_params(self):
        """Test initialization with custom parameters"""
        trainer = MathTrainer(min_digits=2, max_digits=3)
        assert trainer.min_digits == 2
        assert trainer.max_digits == 3

    def test_init_invalid_params(self):
        """Test initialization with invalid parameters"""
        # Check parameter correction
        trainer = MathTrainer(min_digits=0, max_digits=5)
        assert trainer.min_digits == 1  # Fixed to minimum
        assert trainer.max_digits == 3  # Fixed to maximum

        # Check case when min > max
        trainer = MathTrainer(min_digits=3, max_digits=1)
        assert trainer.min_digits == 1  # Should be fixed
        assert trainer.max_digits == 1

    def test_generate_number_one_digit(self):
        """Test generation of single digit number"""
        trainer = MathTrainer()
        for _ in range(10):  # Check multiple times
            number = trainer._generate_number(1)
            assert 1 <= number <= 9

    def test_generate_number_two_digits(self):
        """Test generation of two digit number"""
        trainer = MathTrainer()
        for _ in range(10):
            number = trainer._generate_number(2)
            assert 10 <= number <= 99

    def test_generate_number_three_digits(self):
        """Test generation of three digit number"""
        trainer = MathTrainer()
        for _ in range(10):
            number = trainer._generate_number(3)
            assert 100 <= number <= 999

    def test_generate_number_invalid_digits(self):
        """Test generation of number with invalid number of digits"""
        trainer = MathTrainer()
        with pytest.raises(ValueError):
            trainer._generate_number(0)
        with pytest.raises(ValueError):
            trainer._generate_number(4)

    def test_generate_exercise(self):
        """Test exercise generation"""
        trainer = MathTrainer(min_digits=1, max_digits=2)
        exercise = trainer.generate_exercise()

        # Check that exercise is created
        assert exercise is not None
        assert isinstance(exercise, Exercise)
        assert trainer.current_exercise == exercise

        # Check data correctness
        assert exercise.first_number > 0
        assert exercise.second_number > 0
        assert exercise.operation in [Operation.ADDITION, Operation.SUBTRACTION]

        # Check answer calculation correctness
        if exercise.operation == Operation.ADDITION:
            expected = exercise.first_number + exercise.second_number
        else:  # SUBTRACTION
            expected = exercise.first_number - exercise.second_number

        assert exercise.correct_answer == expected
        assert exercise.correct_answer >= 0  # Result should not be negative

    def test_generate_exercise_subtraction_positive_result(self):
        """Test that subtraction always gives positive result"""
        trainer = MathTrainer()

        # Generate many exercises to check different cases
        for _ in range(50):
            exercise = trainer.generate_exercise()
            if exercise.operation == Operation.SUBTRACTION:
                assert exercise.correct_answer >= 0
                assert exercise.first_number >= exercise.second_number

    def test_check_answer_correct(self):
        """Test checking correct answer"""
        trainer = MathTrainer()
        exercise = trainer.generate_exercise()

        result = trainer.check_answer(exercise, exercise.correct_answer)

        assert isinstance(result, Result)
        assert result.is_correct is True
        assert result.user_answer == exercise.correct_answer
        assert result.correct_answer == exercise.correct_answer
        assert "Correct" in result.message

        # Check statistics update
        assert trainer.stats["total_exercises"] == 1
        assert trainer.stats["correct_answers"] == 1
        assert trainer.stats["incorrect_answers"] == 0

    def test_check_answer_incorrect(self):
        """Test checking incorrect answer"""
        trainer = MathTrainer()
        exercise = trainer.generate_exercise()
        wrong_answer = exercise.correct_answer + 1

        result = trainer.check_answer(exercise, wrong_answer)

        assert isinstance(result, Result)
        assert result.is_correct is False
        assert result.user_answer == wrong_answer
        assert result.correct_answer == exercise.correct_answer
        assert "Incorrect" in result.message
        assert str(exercise.correct_answer) in result.message

        # Check statistics update
        assert trainer.stats["total_exercises"] == 1
        assert trainer.stats["correct_answers"] == 0
        assert trainer.stats["incorrect_answers"] == 1

    def test_check_answer_no_exercise(self):
        """Test checking answer with None exercise"""
        trainer = MathTrainer()

        # Now API requires exercise as parameter, so test with None
        with pytest.raises(AttributeError):
            trainer.check_answer(None, 42)

    def test_get_current_exercise_text(self):
        """Test getting current exercise text"""
        trainer = MathTrainer()

        # Without exercise
        assert trainer.get_current_exercise_text() == "No active exercise"

        # With exercise
        exercise = trainer.generate_exercise()
        text = trainer.get_current_exercise_text()
        assert str(exercise.first_number) in text
        assert str(exercise.second_number) in text
        assert exercise.operation.value in text
        assert "=" in text
        assert "?" in text

    def test_get_stats_empty(self):
        """Test getting statistics without exercises"""
        trainer = MathTrainer()
        stats = trainer.get_stats()

        assert stats["total_exercises"] == 0
        assert stats["correct_answers"] == 0
        assert stats["incorrect_answers"] == 0
        assert stats["accuracy"] == 0.0

    def test_get_stats_with_exercises(self):
        """Test getting statistics with exercises"""
        trainer = MathTrainer()

        # Solve several exercises
        for _ in range(4):
            exercise = trainer.generate_exercise()
            trainer.check_answer(exercise, exercise.correct_answer)  # Correct answer

        exercise = trainer.generate_exercise()
        trainer.check_answer(exercise, exercise.correct_answer + 1)  # Incorrect answer

        stats = trainer.get_stats()
        assert stats["total_exercises"] == 5
        assert stats["correct_answers"] == 4
        assert stats["incorrect_answers"] == 1
        assert stats["accuracy"] == 80.0

    def test_reset_stats(self):
        """Test resetting statistics"""
        trainer = MathTrainer()

        # Create some statistics
        exercise = trainer.generate_exercise()
        trainer.check_answer(exercise, exercise.correct_answer)

        assert trainer.stats["total_exercises"] == 1

        # Reset
        trainer.reset_stats()

        assert trainer.stats["total_exercises"] == 0
        assert trainer.stats["correct_answers"] == 0
        assert trainer.stats["incorrect_answers"] == 0

    def test_set_difficulty(self):
        """Test setting difficulty"""
        trainer = MathTrainer()

        trainer.set_difficulty(2, 3)
        assert trainer.min_digits == 2
        assert trainer.max_digits == 3

        # Test correction of invalid values
        trainer.set_difficulty(0, 5)
        assert trainer.min_digits == 1
        assert trainer.max_digits == 3

        # Test case min > max
        trainer.set_difficulty(3, 1)
        assert trainer.min_digits == 1
        assert trainer.max_digits == 1


class TestExercise:
    """Tests for Exercise class"""

    def test_exercise_str_addition(self):
        """Test string representation of addition exercise"""
        exercise = Exercise(5, 3, Operation.ADDITION, 8)
        assert str(exercise) == "5 + 3 = ?"

    def test_exercise_str_subtraction(self):
        """Test string representation of subtraction exercise"""
        exercise = Exercise(10, 4, Operation.SUBTRACTION, 6)
        assert str(exercise) == "10 - 4 = ?"


class TestResult:
    """Tests for Result class"""

    def test_result_creation(self):
        """Test creating Result object"""
        result = Result(is_correct=True, user_answer=8, correct_answer=8, message="Correct!")

        assert result.is_correct is True
        assert result.user_answer == 8
        assert result.correct_answer == 8
        assert result.message == "Correct!"


class TestOperation:
    """Tests for Operation enum"""

    def test_operation_values(self):
        """Test operation values"""
        assert Operation.ADDITION.value == "+"
        assert Operation.SUBTRACTION.value == "-"

    def test_operation_list(self):
        """Test getting operation list"""
        operations = list(Operation)
        assert len(operations) == 2
        assert Operation.ADDITION in operations
        assert Operation.SUBTRACTION in operations


# Integration tests
class TestIntegration:
    """Integration tests for full workflow"""

    def test_full_training_session(self):
        """Test full training session"""
        trainer = MathTrainer(min_digits=1, max_digits=2)

        # Simulate session of 5 exercises
        correct_count = 0
        for i in range(5):
            exercise = trainer.generate_exercise()
            assert exercise is not None

            # Sometimes answer correctly, sometimes not
            if i % 2 == 0:
                result = trainer.check_answer(exercise, exercise.correct_answer)
                assert result.is_correct is True
                correct_count += 1
            else:
                result = trainer.check_answer(exercise, exercise.correct_answer + 1)
                assert result.is_correct is False

        # Check final statistics
        stats = trainer.get_stats()
        assert stats["total_exercises"] == 5
        assert stats["correct_answers"] == correct_count
        assert stats["incorrect_answers"] == 5 - correct_count

        expected_accuracy = round((correct_count / 5) * 100, 1)
        assert stats["accuracy"] == expected_accuracy

    def test_difficulty_affects_generation(self):
        """Test that difficulty affects exercise generation"""
        # Easy level
        easy_trainer = MathTrainer(min_digits=1, max_digits=1)
        easy_exercises = [easy_trainer.generate_exercise() for _ in range(10)]

        # Hard level
        hard_trainer = MathTrainer(min_digits=3, max_digits=3)
        hard_exercises = [hard_trainer.generate_exercise() for _ in range(10)]

        # Check that numbers in easy exercises are smaller
        for exercise in easy_exercises:
            assert 1 <= exercise.first_number <= 9
            assert 1 <= exercise.second_number <= 9

        # Check that numbers in hard exercises are larger
        for exercise in hard_exercises:
            assert 100 <= exercise.first_number <= 999
            assert 100 <= exercise.second_number <= 999
