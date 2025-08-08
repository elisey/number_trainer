"""
Консольный интерфейс для математического тренажера.

Предоставляет простой текстовый интерфейс для работы с тренажером.
"""

from ..core.trainer import MathTrainer


def run_console_trainer(
    min_digits: int = 1, max_digits: int = 2, num_exercises: int = 3
) -> None:
    """
    Запускает консольную версию математического тренажера

    Args:
        min_digits: Минимальное количество цифр в числах
        max_digits: Максимальное количество цифр в числах
        num_exercises: Количество упражнений для решения
    """
    print("=== Математический тренажер ===")
    print(f"Сложность: {min_digits}-{max_digits} цифры")
    print(f"Количество упражнений: {num_exercises}")
    print("-" * 30)

    trainer = MathTrainer(min_digits=min_digits, max_digits=max_digits)

    # Генерируем и решаем упражнения
    for i in range(num_exercises):
        exercise = trainer.generate_exercise()
        print(f"\nУпражнение {i + 1}: {exercise}")

        try:
            user_answer = int(input("Ваш ответ: "))
            result = trainer.check_answer(user_answer)
            print(f"Результат: {result.message}")
        except ValueError:
            print("Ошибка: введите целое число")
            continue
        except KeyboardInterrupt:
            print("\nТренировка прервана пользователем")
            break

    # Показываем статистику
    stats = trainer.get_stats()
    print(f"\n{'=' * 30}")
    print("Статистика:")
    print(f"Всего упражнений: {stats['total_exercises']}")
    print(f"Правильных ответов: {stats['correct_answers']}")
    print(f"Неправильных ответов: {stats['incorrect_answers']}")
    print(f"Точность: {stats['accuracy']}%")


if __name__ == "__main__":
    # Демонстрация работы консольного интерфейса
    run_console_trainer()
