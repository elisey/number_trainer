"""
Modern GUI interface for mathematical trainer.

Minimalist design with intuitive interface and beautiful animations.
"""

import time
import tkinter as tk
from enum import Enum
from tkinter import ttk
from typing import Optional

from ..core.models import Exercise, Result
from ..core.trainer import MathTrainer
from .styles import get_colors, setup_styles


class AppState(Enum):
    """Application states"""

    WELCOME = "welcome"
    EXERCISE = "exercise"
    RESULT = "result"


class NumberTrainerApp:
    """Modern GUI class for mathematical trainer"""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        # Type annotations for dynamically created attributes
        self.total_exercises_label: ttk.Label
        self.correct_answers_label: ttk.Label
        self.incorrect_answers_label: ttk.Label
        self.trainer = MathTrainer()
        self.current_exercise: Optional[Exercise] = None
        self.current_state = AppState.WELCOME
        self.colors = get_colors()

        # Window setup
        self.setup_window()

        # Style setup
        setup_styles()

        # Interface creation
        self.create_main_interface()

        # Keyboard shortcuts binding
        self.bind_keyboard_shortcuts()

    def setup_window(self) -> None:
        """Setup main application window"""
        self.root.title("Number Trainer")
        self.root.geometry("900x700")
        self.root.minsize(600, 500)
        self.root.configure(bg=self.colors["background"])

        # Center window
        self.center_window()

    def center_window(self) -> None:
        """Centers window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_main_interface(self) -> None:
        """Creates main application interface"""
        # Main container
        main_container = ttk.Frame(self.root, style="Main.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Header
        self.create_header(main_container)

        # Main content area
        self.create_content_area(main_container)

        # Statistics panel
        self.create_stats_panel(main_container)

        # Show welcome screen
        self.show_welcome_screen()

    def create_header(self, parent: tk.Widget) -> None:
        """Creates application header"""
        header_frame = ttk.Frame(parent, style="Main.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 30))

        # Title
        title_label = ttk.Label(header_frame, text="Number Trainer", style="Title.TLabel")
        title_label.pack()

        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Mental Math Trainer", style="Subtitle.TLabel")
        subtitle_label.pack(pady=(5, 0))

    def create_content_area(self, parent: tk.Widget) -> None:
        """Creates main content area"""
        # Content card
        self.content_card = ttk.Frame(parent, style="Card.TFrame")
        self.content_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Inner container with padding
        self.content_container = ttk.Frame(self.content_card, style="Card.TFrame")
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

    def create_stats_panel(self, parent: tk.Widget) -> None:
        """Creates statistics panel"""
        stats_frame = ttk.Frame(parent, style="Card.TFrame")
        stats_frame.pack(fill=tk.X, pady=(10, 0))

        # Inner statistics container
        stats_container = ttk.Frame(stats_frame, style="Card.TFrame")
        stats_container.pack(fill=tk.X, padx=30, pady=20)

        # Create statistics columns
        self.create_stat_column(stats_container, "Total", "total_exercises", 0)
        self.create_stat_column(stats_container, "Correct", "correct_answers", 1)
        self.create_stat_column(stats_container, "Incorrect", "incorrect_answers", 2)
        self.create_accuracy_column(stats_container, 3)

        # Grid setup
        for i in range(4):
            stats_container.columnconfigure(i, weight=1)

    def create_stat_column(self, parent: tk.Widget, title: str, stat_key: str, column: int) -> None:
        """Creates statistics column"""
        col_frame = ttk.Frame(parent, style="Card.TFrame")
        col_frame.grid(row=0, column=column, padx=20, sticky="ew")

        # Value
        value_label = ttk.Label(col_frame, text="0", style="StatsValue.TLabel")
        value_label.pack()
        setattr(self, f"{stat_key}_label", value_label)

        # Title
        title_label = ttk.Label(col_frame, text=title, style="Stats.TLabel")
        title_label.pack()

    def create_accuracy_column(self, parent: tk.Widget, column: int) -> None:
        """Creates accuracy column"""
        col_frame = ttk.Frame(parent, style="Card.TFrame")
        col_frame.grid(row=0, column=column, padx=20, sticky="ew")

        # Accuracy value
        self.accuracy_label = ttk.Label(col_frame, text="0%", style="StatsValue.TLabel")
        self.accuracy_label.pack()

        # Title
        title_label = ttk.Label(col_frame, text="Accuracy", style="Stats.TLabel")
        title_label.pack()

    def show_welcome_screen(self) -> None:
        """Shows welcome screen"""
        self.current_state = AppState.WELCOME
        self.clear_content()

        # Welcome message
        welcome_label = ttk.Label(
            self.content_container,
            text="Welcome to Number Trainer!",
            style="Exercise.TLabel",
        )
        welcome_label.pack(pady=(50, 20))

        # Description
        desc_label = ttk.Label(
            self.content_container,
            text="Train your mental math skills\nwith exercises of varying difficulty",
            style="Result.TLabel",
        )
        desc_label.pack(pady=(0, 40))

        # Difficulty selection buttons
        difficulty_frame = ttk.Frame(self.content_container, style="Card.TFrame")
        difficulty_frame.pack(pady=20)

        ttk.Label(difficulty_frame, text="Select difficulty:", style="Result.TLabel").pack(pady=(0, 15))

        button_frame = ttk.Frame(difficulty_frame, style="Card.TFrame")
        button_frame.pack()

        # Difficulty buttons
        difficulties = [
            ("Easy (1 digit)", 1, 1),
            ("Medium (1-2 digits)", 1, 2),
            ("Hard (2-3 digits)", 2, 3),
        ]

        for text, min_digits, max_digits in difficulties:
            btn = ttk.Button(
                button_frame,
                text=text,
                style="Primary.TButton",
                command=lambda m=min_digits, mx=max_digits: self.start_training(m, mx),  # type: ignore[misc]
            )
            btn.pack(side=tk.LEFT, padx=10)

    def start_training(self, min_digits: int = 1, max_digits: int = 2) -> None:
        """Starts training with specified difficulty"""
        self.trainer = MathTrainer(min_digits, max_digits)
        self.show_exercise()

    def show_exercise(self) -> None:
        """Shows new exercise"""
        self.current_state = AppState.EXERCISE
        self.clear_content()

        # Generate exercise
        self.current_exercise = self.trainer.generate_exercise()

        # Remember exercise start time
        self.exercise_start_time = time.time()

        # Display exercise
        exercise_label = ttk.Label(
            self.content_container,
            text=(
                f"{self.current_exercise.first_number} {self.current_exercise.operation.value} "
                f"{self.current_exercise.second_number} = ?"
            ),
            style="Exercise.TLabel",
        )
        exercise_label.pack(pady=(80, 40))

        # Answer input field
        self.answer_var = tk.StringVar()
        self.answer_entry = ttk.Entry(
            self.content_container,
            textvariable=self.answer_var,
            style="Modern.TEntry",
            justify="center",
            width=8,
            font=("SF Pro Display", 24),
        )
        self.answer_entry.pack(pady=20)
        self.answer_entry.focus()

        # Action buttons
        button_frame = ttk.Frame(self.content_container, style="Card.TFrame")
        button_frame.pack(pady=30)

        check_btn = ttk.Button(
            button_frame,
            text="Check",
            style="Primary.TButton",
            command=self.check_answer,
        )
        check_btn.pack(side=tk.LEFT, padx=(0, 15))

        skip_btn = ttk.Button(
            button_frame,
            text="Skip",
            style="Secondary.TButton",
            command=self.skip_exercise,
        )
        skip_btn.pack(side=tk.LEFT, padx=(0, 15))

        new_btn = ttk.Button(
            button_frame,
            text="New Game",
            style="Secondary.TButton",
            command=self.show_welcome_screen,
        )
        new_btn.pack(side=tk.LEFT)

    def check_answer(self) -> None:
        """Checks user answer"""
        if not self.current_exercise:
            return

        try:
            user_answer = int(self.answer_var.get().strip())
        except ValueError:
            self.show_error_message("Please enter a number")
            return

        # Calculate execution time
        time_taken = time.time() - self.exercise_start_time

        # Check answer
        result = self.trainer.check_answer(self.current_exercise, user_answer, time_taken)
        self.show_result(result)

        # Update statistics
        self.update_stats()

    def skip_exercise(self) -> None:
        """Skips current exercise"""
        if self.current_exercise:
            # Calculate execution time
            time_taken = time.time() - self.exercise_start_time

            # Count skip as incorrect answer
            result = self.trainer.check_answer(self.current_exercise, -999999, time_taken)
            self.show_result(result, skipped=True)
            self.update_stats()

    def show_result(self, result: Result, skipped: bool = False) -> None:
        """Shows answer check result"""
        self.current_state = AppState.RESULT
        self.clear_content()

        if skipped:
            status_text = "Exercise skipped"
        elif result.is_correct:
            status_text = "Correct! 🎉"
        else:
            status_text = "Incorrect 😔"

        # Status
        status_label = ttk.Label(self.content_container, text=status_text, style="Exercise.TLabel")
        status_label.pack(pady=(60, 20))

        # Correct answer
        if not result.is_correct:
            correct_label = ttk.Label(
                self.content_container,
                text=f"Correct answer: {result.correct_answer}",
                style="Result.TLabel",
            )
            correct_label.pack(pady=10)

        # Solution time
        time_label = ttk.Label(
            self.content_container,
            text=f"Time: {result.time_taken:.1f} sec",
            style="Result.TLabel",
        )
        time_label.pack(pady=5)

        # Continue button
        continue_btn = ttk.Button(
            self.content_container,
            text="Next Exercise",
            style="Success.TButton",
            command=self.show_exercise,
        )
        continue_btn.pack(pady=40)
        continue_btn.focus()

    def show_error_message(self, message: str) -> None:
        """Shows error message"""
        # Can add popup notification
        self.answer_entry.configure(style="Error.TEntry")
        self.root.after(1000, lambda: self.answer_entry.configure(style="Modern.TEntry"))

    def update_stats(self) -> None:
        """Updates statistics display"""
        stats = self.trainer.get_stats()

        self.total_exercises_label.config(text=str(stats["total_exercises"]))
        self.correct_answers_label.config(text=str(stats["correct_answers"]))
        self.incorrect_answers_label.config(text=str(stats["incorrect_answers"]))

        # Calculate accuracy
        if stats["total_exercises"] > 0:
            accuracy = (stats["correct_answers"] / stats["total_exercises"]) * 100
            self.accuracy_label.config(text=f"{accuracy:.0f}%")
        else:
            self.accuracy_label.config(text="0%")

    def clear_content(self) -> None:
        """Clears content area"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

    def bind_keyboard_shortcuts(self) -> None:
        """Binds keyboard shortcuts"""
        self.root.bind("<Return>", lambda e: self.handle_enter_key())
        self.root.bind("<Escape>", lambda e: self.handle_exit_key())
        self.root.bind("<Control-n>", lambda e: self.show_exercise())

    def handle_enter_key(self) -> None:
        """Handles Enter key press depending on current state"""
        if self.current_state == AppState.EXERCISE:
            self.check_answer()
        elif self.current_state == AppState.RESULT:
            self.show_exercise()

    def handle_exit_key(self) -> None:
        """Handles Escape key press depending on current state"""
        if self.current_state == AppState.WELCOME:
            # On welcome screen - exit program
            self.exit_application()
        else:
            # During exercise or result - return to welcome screen
            self.show_welcome_screen()

    def exit_application(self) -> None:
        """Closes application"""
        self.root.quit()
        self.root.destroy()
