"""
Console interface for mathematical trainer.
"""

from ..core.trainer import MathTrainer


def run_console_trainer(min_digits: int = 1, max_digits: int = 2, num_exercises: int = 3) -> None:
    """
    Launches console version of mathematical trainer

    Args:
        min_digits: Minimum number of digits in numbers
        max_digits: Maximum number of digits in numbers
        num_exercises: Number of exercises to solve
    """
    print("=== Mathematical Trainer ===")
    print(f"Difficulty: {min_digits}-{max_digits} digits")
    print(f"Number of exercises: {num_exercises}")
    print("-" * 30)

    trainer = MathTrainer(min_digits=min_digits, max_digits=max_digits)

    # Generate and solve exercises
    for i in range(num_exercises):
        exercise = trainer.generate_exercise()
        print(f"\nExercise {i + 1}: {exercise}")

        try:
            user_answer = int(input("Your answer: "))
            result = trainer.check_answer(exercise, user_answer)
            print(f"Result: {result.message}")
        except ValueError:
            print("Error: enter an integer")
            continue
        except KeyboardInterrupt:
            print("\nTraining interrupted by user")
            break

    # Show statistics
    stats = trainer.get_stats()
    print(f"\n{'=' * 30}")
    print("Statistics:")
    print(f"Total exercises: {stats['total_exercises']}")
    print(f"Correct answers: {stats['correct_answers']}")
    print(f"Incorrect answers: {stats['incorrect_answers']}")
    print(f"Accuracy: {stats['accuracy']}%")


if __name__ == "__main__":
    # Demonstration of console interface work
    run_console_trainer()
