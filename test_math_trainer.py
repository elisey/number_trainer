# import pytest
# from math_trainer import MathTrainer, Operation, Exercise, Result


# class TestMathTrainer:
#     """Тесты для класса MathTrainer"""
    
#     def test_init_default_params(self):
#         """Тест инициализации с параметрами по умолчанию"""
#         trainer = MathTrainer()
#         assert trainer.min_digits == 1
#         assert trainer.max_digits == 3
#         assert trainer.current_exercise is None
#         assert trainer.stats['total_exercises'] == 0
#         assert trainer.stats['correct_answers'] == 0
#         assert trainer.stats['incorrect_answers'] == 0
    
#     def test_init_custom_params(self):
#         """Тест инициализации с пользовательскими параметрами"""
#         trainer = MathTrainer(min_digits=2, max_digits=3)
#         assert trainer.min_digits == 2
#         assert trainer.max_digits == 3
    
#     def test_init_invalid_params(self):
#         """Тест инициализации с некорректными параметрами"""
#         # Проверяем коррекцию параметров
#         trainer = MathTrainer(min_digits=0, max_digits=5)
#         assert trainer.min_digits == 1  # Исправлено до минимума
#         assert trainer.max_digits == 3  # Исправлено до максимума
        
#         # Проверяем случай когда min > max
#         trainer = MathTrainer(min_digits=3, max_digits=1)
#         assert trainer.min_digits == 1  # Должно быть исправлено
#         assert trainer.max_digits == 1
    
#     def test_generate_number_one_digit(self):
#         """Тест генерации однозначного числа"""
#         trainer = MathTrainer()
#         for _ in range(10):  # Проверяем несколько раз
#             number = trainer._generate_number(1)
#             assert 1 <= number <= 9
    
#     def test_generate_number_two_digits(self):
#         """Тест генерации двузначного числа"""
#         trainer = MathTrainer()
#         for _ in range(10):
#             number = trainer._generate_number(2)
#             assert 10 <= number <= 99
    
#     def test_generate_number_three_digits(self):
#         """Тест генерации трёхзначного числа"""
#         trainer = MathTrainer()
#         for _ in range(10):
#             number = trainer._generate_number(3)
#             assert 100 <= number <= 999
    
#     def test_generate_number_invalid_digits(self):
#         """Тест генерации числа с некорректным количеством цифр"""
#         trainer = MathTrainer()
#         with pytest.raises(ValueError, match="Количество цифр должно быть от 1 до 3"):
#             trainer._generate_number(4)
        
#         with pytest.raises(ValueError, match="Количество цифр должно быть от 1 до 3"):
#             trainer._generate_number(0)
    
#     def test_generate_exercise(self):
#         """Тест генерации упражнения"""
#         trainer = MathTrainer(min_digits=1, max_digits=2)
#         exercise = trainer.generate_exercise()
        
#         # Проверяем, что упражнение создано
#         assert isinstance(exercise, Exercise)
#         assert trainer.current_exercise == exercise
        
#         # Проверяем диапазоны чисел
#         assert 1 <= exercise.first_number <= 99
#         assert 1 <= exercise.second_number <= 99
        
#         # Проверяем операцию
#         assert exercise.operation in [Operation.ADDITION, Operation.SUBTRACTION]
        
#         # Проверяем правильность вычисления
#         if exercise.operation == Operation.ADDITION:
#             expected = exercise.first_number + exercise.second_number
#         else:
#             expected = exercise.first_number - exercise.second_number
        
#         assert exercise.correct_answer == expected
        
#         # Для вычитания результат должен быть неотрицательным
#         if exercise.operation == Operation.SUBTRACTION:
#             assert exercise.correct_answer >= 0
    
#     def test_generate_multiple_exercises(self):
#         """Тест генерации нескольких упражнений подряд"""
#         trainer = MathTrainer()
#         exercises = []
        
#         for _ in range(5):
#             exercise = trainer.generate_exercise()
#             exercises.append(exercise)
#             assert trainer.current_exercise == exercise
        
#         # Проверяем, что упражнения разные (с высокой вероятностью)
#         unique_exercises = set(str(ex) for ex in exercises)
#         assert len(unique_exercises) >= 3  # Должно быть хотя бы 3 разных
    
#     def test_check_answer_correct(self):
#         """Тест проверки правильного ответа"""
#         trainer = MathTrainer()
#         exercise = trainer.generate_exercise()
        
#         result = trainer.check_answer(exercise.correct_answer)
        
#         assert isinstance(result, Result)
#         assert result.is_correct is True
#         assert result.user_answer == exercise.correct_answer
#         assert result.correct_answer == exercise.correct_answer
#         assert "Правильно" in result.message
        
#         # Проверяем обновление статистики
#         assert trainer.stats['total_exercises'] == 1
#         assert trainer.stats['correct_answers'] == 1
#         assert trainer.stats['incorrect_answers'] == 0
    
#     def test_check_answer_incorrect(self):
#         """Тест проверки неправильного ответа"""
#         trainer = MathTrainer()
#         exercise = trainer.generate_exercise()
#         wrong_answer = exercise.correct_answer + 1
        
#         result = trainer.check_answer(wrong_answer)
        
#         assert result.is_correct is False
#         assert result.user_answer == wrong_answer
#         assert result.correct_answer == exercise.correct_answer
#         assert "Неправильно" in result.message
#         assert str(exercise.correct_answer) in result.message
        
#         # Проверяем обновление статистики
#         assert trainer.stats['total_exercises'] == 1
#         assert trainer.stats['correct_answers'] == 0
#         assert trainer.stats['incorrect_answers'] == 1
    
#     def test_check_answer_no_exercise(self):
#         """Тест проверки ответа без активного упражнения"""
#         trainer = MathTrainer()
        
#         with pytest.raises(ValueError, match="Нет активного упражнения"):
#             trainer.check_answer(42)
    
#     def test_get_current_exercise_text(self):
#         """Тест получения текста текущего упражнения"""
#         trainer = MathTrainer()
        
#         # Без упражнения
#         assert trainer.get_current_exercise_text() == "Нет активного упражнения"
        
#         # С упражнением
#         exercise = trainer.generate_exercise()
#         text = trainer.get_current_exercise_text()
#         expected = f"{exercise.first_number} {exercise.operation.value} {exercise.second_number} = ?"
#         assert text == expected
    
#     def test_get_stats_empty(self):
#         """Тест получения статистики без упражнений"""
#         trainer = MathTrainer()
#         stats = trainer.get_stats()
        
#         assert stats['total_exercises'] == 0
#         assert stats['correct_answers'] == 0
#         assert stats['incorrect_answers'] == 0
#         assert stats['accuracy'] == 0.0
    
#     def test_get_stats_with_exercises(self):
#         """Тест получения статистики с упражнениями"""
#         trainer = MathTrainer()
        
#         # Делаем несколько упражнений
#         for i in range(4):
#             exercise = trainer.generate_exercise()
#             if i < 3:  # 3 правильных ответа
#                 trainer.check_answer(exercise.correct_answer)
#             else:  # 1 неправильный ответ
#                 trainer.check_answer(exercise.correct_answer + 1)
        
#         stats = trainer.get_stats()
#         assert stats['total_exercises'] == 4
#         assert stats['correct_answers'] == 3
#         assert stats['incorrect_answers'] == 1
#         assert stats['accuracy'] == 75.0
    
#     def test_reset_stats(self):
#         """Тест сброса статистики"""
#         trainer = MathTrainer()
        
#         # Делаем упражнение
#         exercise = trainer.generate_exercise()
#         trainer.check_answer(exercise.correct_answer)
        
#         # Проверяем, что статистика не пустая
#         assert trainer.stats['total_exercises'] == 1
        
#         # Сбрасываем статистику
#         trainer.reset_stats()
        
#         # Проверяем, что статистика сброшена
#         assert trainer.stats['total_exercises'] == 0
#         assert trainer.stats['correct_answers'] == 0
#         assert trainer.stats['incorrect_answers'] == 0
    
#     def test_set_difficulty(self):
#         """Тест установки сложности"""
#         trainer = MathTrainer()
        
#         # Устанавливаем новую сложность
#         trainer.set_difficulty(2, 3)
#         assert trainer.min_digits == 2
#         assert trainer.max_digits == 3
        
#         # Проверяем коррекцию некорректных значений
#         trainer.set_difficulty(0, 5)
#         assert trainer.min_digits == 1
#         assert trainer.max_digits == 3
        
#         # Проверяем случай min > max
#         trainer.set_difficulty(3, 1)
#         assert trainer.min_digits == 1
#         assert trainer.max_digits == 1


# class TestExercise:
#     """Тесты для класса Exercise"""
    
#     def test_exercise_str_addition(self):
#         """Тест строкового представления упражнения на сложение"""
#         exercise = Exercise(15, 7, Operation.ADDITION, 22)
#         assert str(exercise) == "15 + 7 = ?"
    
#     def test_exercise_str_subtraction(self):
#         """Тест строкового представления упражнения на вычитание"""
#         exercise = Exercise(20, 8, Operation.SUBTRACTION, 12)
#         assert str(exercise) == "20 - 8 = ?"


# class TestResult:
#     """Тесты для класса Result"""
    
#     def test_result_creation(self):
#         """Тест создания объекта Result"""
#         result = Result(
#             is_correct=True,
#             user_answer=42,
#             correct_answer=42,
#             message="Правильно!"
#         )
        
#         assert result.is_correct is True
#         assert result.user_answer == 42
#         assert result.correct_answer == 42
#         assert result.message == "Правильно!"


# class TestOperation:
#     """Тесты для enum Operation"""
    
#     def test_operation_values(self):
#         """Тест значений операций"""
#         assert Operation.ADDITION.value == "+"
#         assert Operation.SUBTRACTION.value == "-"
    
#     def test_operation_list(self):
#         """Тест получения списка операций"""
#         operations = list(Operation)
#         assert len(operations) == 2
#         assert Operation.ADDITION in operations
#         assert Operation.SUBTRACTION in operations


# # Интеграционные тесты
# class TestIntegration:
#     """Интеграционные тесты для полного цикла работы"""
    
#     def test_full_training_session(self):
#         """Тест полной сессии тренировки"""
#         trainer = MathTrainer(min_digits=1, max_digits=2)
        
#         # Проводим несколько упражнений
#         correct_count = 0
#         total_count = 5
        
#         for _ in range(total_count):
#             exercise = trainer.generate_exercise()
            
#             # Иногда даем правильный ответ, иногда неправильный
#             if correct_count < 3:  # Первые 3 правильные
#                 result = trainer.check_answer(exercise.correct_answer)
#                 assert result.is_correct is True
#                 correct_count += 1
#             else:  # Остальные неправильные
#                 result = trainer.check_answer(exercise.correct_answer + 1)
#                 assert result.is_correct is False
        
#         # Проверяем итоговую статистику
#         stats = trainer.get_stats()
#         assert stats['total_exercises'] == total_count
#         assert stats['correct_answers'] == 3
#         assert stats['incorrect_answers'] == 2
#         assert stats['accuracy'] == 60.0
    
#     def test_difficulty_affects_generation(self):
#         """Тест влияния сложности на генерацию упражнений"""
#         # Легкая сложность - только однозначные числа
#         easy_trainer = MathTrainer(min_digits=1, max_digits=1)
        
#         for _ in range(10):
#             exercise = easy_trainer.generate_exercise()
#             assert 1 <= exercise.first_number <= 9
#             assert 1 <= exercise.second_number <= 9
        
#         # Сложная сложность - только трёхзначные числа
#         hard_trainer = MathTrainer(min_digits=3, max_digits=3)
        
#         for _ in range(10):
#             exercise = hard_trainer.generate_exercise()
#             assert 100 <= exercise.first_number <= 999
#             assert 100 <= exercise.second_number <= 999
