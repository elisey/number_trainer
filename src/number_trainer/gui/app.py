"""
Современный GUI интерфейс для математического тренажера.

Минималистичный дизайн с интуитивным интерфейсом и красивой анимацией.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
import threading
import time

from ..core.trainer import MathTrainer
from ..core.models import Exercise, Result
from .styles import get_fonts, get_colors, setup_styles


class NumberTrainerApp:
    """Современный GUI класс для математического тренажера"""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.trainer = MathTrainer()
        self.current_exercise: Optional[Exercise] = None
        self.colors = get_colors()
        
        # Настройка окна
        self.setup_window()
        
        # Настройка стилей
        setup_styles()
        
        # Создание интерфейса
        self.create_main_interface()
        
        # Привязка горячих клавиш
        self.bind_keyboard_shortcuts()

    def setup_window(self) -> None:
        """Настройка основного окна приложения"""
        self.root.title("Number Trainer")
        self.root.geometry("900x700")
        self.root.minsize(600, 500)
        self.root.configure(bg=self.colors["background"])
        
        # Центрирование окна
        self.center_window()

    def center_window(self) -> None:
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_main_interface(self) -> None:
        """Создает основной интерфейс приложения"""
        # Основной контейнер
        main_container = ttk.Frame(self.root, style="Main.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Заголовок
        self.create_header(main_container)
        
        # Основная область контента
        self.create_content_area(main_container)
        
        # Панель статистики
        self.create_stats_panel(main_container)
        
        # Показать стартовый экран
        self.show_welcome_screen()

    def create_header(self, parent) -> None:
        """Создает заголовок приложения"""
        header_frame = ttk.Frame(parent, style="Main.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Заголовок
        title_label = ttk.Label(
            header_frame,
            text="Number Trainer",
            style="Title.TLabel"
        )
        title_label.pack()
        
        # Подзаголовок
        subtitle_label = ttk.Label(
            header_frame,
            text="Тренажер устного счета",
            style="Subtitle.TLabel"
        )
        subtitle_label.pack(pady=(5, 0))

    def create_content_area(self, parent) -> None:
        """Создает основную область контента"""
        # Карточка с контентом
        self.content_card = ttk.Frame(parent, style="Card.TFrame")
        self.content_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Внутренний контейнер с отступами
        self.content_container = ttk.Frame(self.content_card, style="Card.TFrame")
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

    def create_stats_panel(self, parent) -> None:
        """Создает панель статистики"""
        stats_frame = ttk.Frame(parent, style="Card.TFrame")
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Внутренний контейнер статистики
        stats_container = ttk.Frame(stats_frame, style="Card.TFrame")
        stats_container.pack(fill=tk.X, padx=30, pady=20)
        
        # Создание колонок статистики
        self.create_stat_column(stats_container, "Всего", "total_exercises", 0)
        self.create_stat_column(stats_container, "Правильно", "correct_answers", 1)
        self.create_stat_column(stats_container, "Неправильно", "incorrect_answers", 2)
        self.create_accuracy_column(stats_container, 3)
        
        # Настройка сетки
        for i in range(4):
            stats_container.columnconfigure(i, weight=1)

    def create_stat_column(self, parent, title: str, stat_key: str, column: int) -> None:
        """Создает колонку статистики"""
        col_frame = ttk.Frame(parent, style="Card.TFrame")
        col_frame.grid(row=0, column=column, padx=20, sticky="ew")
        
        # Значение
        value_label = ttk.Label(
            col_frame,
            text="0",
            style="StatsValue.TLabel"
        )
        value_label.pack()
        setattr(self, f"{stat_key}_label", value_label)
        
        # Заголовок
        title_label = ttk.Label(
            col_frame,
            text=title,
            style="Stats.TLabel"
        )
        title_label.pack()

    def create_accuracy_column(self, parent, column: int) -> None:
        """Создает колонку точности"""
        col_frame = ttk.Frame(parent, style="Card.TFrame")
        col_frame.grid(row=0, column=column, padx=20, sticky="ew")
        
        # Значение точности
        self.accuracy_label = ttk.Label(
            col_frame,
            text="0%",
            style="StatsValue.TLabel"
        )
        self.accuracy_label.pack()
        
        # Заголовок
        title_label = ttk.Label(
            col_frame,
            text="Точность",
            style="Stats.TLabel"
        )
        title_label.pack()

    def show_welcome_screen(self) -> None:
        """Показывает экран приветствия"""
        self.clear_content()
        
        # Приветственное сообщение
        welcome_label = ttk.Label(
            self.content_container,
            text="Добро пожаловать в Number Trainer!",
            style="Exercise.TLabel"
        )
        welcome_label.pack(pady=(50, 20))
        
        # Описание
        desc_label = ttk.Label(
            self.content_container,
            text="Тренируйте навыки устного счета\nс упражнениями разной сложности",
            style="Result.TLabel"
        )
        desc_label.pack(pady=(0, 40))
        
        # Кнопки настройки сложности
        difficulty_frame = ttk.Frame(self.content_container, style="Card.TFrame")
        difficulty_frame.pack(pady=20)
        
        ttk.Label(
            difficulty_frame,
            text="Выберите сложность:",
            style="Result.TLabel"
        ).pack(pady=(0, 15))
        
        button_frame = ttk.Frame(difficulty_frame, style="Card.TFrame")
        button_frame.pack()
        
        # Кнопки сложности
        difficulties = [
            ("Легко (1 цифра)", 1, 1),
            ("Средне (1-2 цифры)", 1, 2),
            ("Сложно (2-3 цифры)", 2, 3)
        ]
        
        for text, min_digits, max_digits in difficulties:
            btn = ttk.Button(
                button_frame,
                text=text,
                style="Primary.TButton",
                command=lambda m=min_digits, mx=max_digits: self.start_training(m, mx)
            )
            btn.pack(side=tk.LEFT, padx=10)

    def start_training(self, min_digits: int = 1, max_digits: int = 2) -> None:
        """Начинает тренировку с заданной сложностью"""
        self.trainer = MathTrainer(min_digits, max_digits)
        self.show_exercise()

    def show_exercise(self) -> None:
        """Показывает новое упражнение"""
        self.clear_content()
        
        # Генерируем упражнение
        self.current_exercise = self.trainer.generate_exercise()
        
        # Запоминаем время начала упражнения
        self.exercise_start_time = time.time()
        
        # Отображение упражнения
        exercise_label = ttk.Label(
            self.content_container,
            text=f"{self.current_exercise.first_number} {self.current_exercise.operation.value} {self.current_exercise.second_number} = ?",
            style="Exercise.TLabel"
        )
        exercise_label.pack(pady=(80, 40))
        
        # Поле ввода ответа
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(
            self.content_container,
            textvariable=self.answer_var,
            style="Modern.TEntry",
            justify="center",
            width=10
        )
        self.answer_entry.pack(pady=20)
        self.answer_entry.focus()
        
        # Кнопки действий
        button_frame = ttk.Frame(self.content_container, style="Card.TFrame")
        button_frame.pack(pady=30)
        
        check_btn = ttk.Button(
            button_frame,
            text="Проверить",
            style="Primary.TButton",
            command=self.check_answer
        )
        check_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        skip_btn = ttk.Button(
            button_frame,
            text="Пропустить",
            style="Secondary.TButton",
            command=self.skip_exercise
        )
        skip_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        new_btn = ttk.Button(
            button_frame,
            text="Новая игра",
            style="Secondary.TButton",
            command=self.show_welcome_screen
        )
        new_btn.pack(side=tk.LEFT)

    def check_answer(self) -> None:
        """Проверяет ответ пользователя"""
        if not self.current_exercise:
            return
            
        try:
            user_answer = int(self.answer_var.get().strip())
        except ValueError:
            self.show_error_message("Пожалуйста, введите число")
            return
        
        # Вычисляем время выполнения
        time_taken = time.time() - self.exercise_start_time
        
        # Проверяем ответ
        result = self.trainer.check_answer(self.current_exercise, user_answer, time_taken)
        self.show_result(result)
        
        # Обновляем статистику
        self.update_stats()

    def skip_exercise(self) -> None:
        """Пропускает текущее упражнение"""
        if self.current_exercise:
            # Вычисляем время выполнения
            time_taken = time.time() - self.exercise_start_time
            
            # Считаем пропуск как неправильный ответ
            result = self.trainer.check_answer(self.current_exercise, -999999, time_taken)
            self.show_result(result, skipped=True)
            self.update_stats()

    def show_result(self, result: Result, skipped: bool = False) -> None:
        """Показывает результат проверки ответа"""
        self.clear_content()
        
        if skipped:
            status_text = "Упражнение пропущено"
            status_color = self.colors["warning"]
        elif result.is_correct:
            status_text = "Правильно! 🎉"
            status_color = self.colors["success"]
        else:
            status_text = "Неправильно 😔"
            status_color = self.colors["error"]
        
        # Статус
        status_label = ttk.Label(
            self.content_container,
            text=status_text,
            style="Exercise.TLabel"
        )
        status_label.pack(pady=(60, 20))
        
        # Правильный ответ
        if not result.is_correct:
            correct_label = ttk.Label(
                self.content_container,
                text=f"Правильный ответ: {result.correct_answer}",
                style="Result.TLabel"
            )
            correct_label.pack(pady=10)
        
        # Время решения
        time_label = ttk.Label(
            self.content_container,
            text=f"Время: {result.time_taken:.1f} сек",
            style="Result.TLabel"
        )
        time_label.pack(pady=5)
        
        # Кнопка продолжения
        continue_btn = ttk.Button(
            self.content_container,
            text="Следующее упражнение",
            style="Success.TButton",
            command=self.show_exercise
        )
        continue_btn.pack(pady=40)
        continue_btn.focus()
        
        # Автопереход через 3 секунды
        self.root.after(3000, self.show_exercise)

    def show_error_message(self, message: str) -> None:
        """Показывает сообщение об ошибке"""
        # Можно добавить всплывающее уведомление
        self.answer_entry.configure(style="Error.TEntry")
        self.root.after(1000, lambda: self.answer_entry.configure(style="Modern.TEntry"))

    def update_stats(self) -> None:
        """Обновляет отображение статистики"""
        stats = self.trainer.get_stats()
        
        self.total_exercises_label.config(text=str(stats["total_exercises"]))
        self.correct_answers_label.config(text=str(stats["correct_answers"]))
        self.incorrect_answers_label.config(text=str(stats["incorrect_answers"]))
        
        # Вычисляем точность
        if stats["total_exercises"] > 0:
            accuracy = (stats["correct_answers"] / stats["total_exercises"]) * 100
            self.accuracy_label.config(text=f"{accuracy:.0f}%")
        else:
            self.accuracy_label.config(text="0%")

    def clear_content(self) -> None:
        """Очищает область контента"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

    def bind_keyboard_shortcuts(self) -> None:
        """Привязывает горячие клавиши"""
        self.root.bind('<Return>', lambda e: self.check_answer())
        self.root.bind('<Escape>', lambda e: self.show_welcome_screen())
        self.root.bind('<Control-n>', lambda e: self.show_exercise())
