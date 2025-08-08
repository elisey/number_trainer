"""
Стили и темы оформления для GUI приложения.

Содержит настройки внешнего вида интерфейса.
"""

from tkinter import ttk


def setup_styles() -> None:
    """Настраивает стили для приложения"""
    style = ttk.Style()
    style.theme_use("clam")

    # Можно добавить кастомные стили здесь
    # Например:
    # style.configure('Title.TLabel', font=('Arial', 24, 'bold'))
    # style.configure('Exercise.TLabel', font=('Arial', 18))


def get_fonts() -> dict:
    """
    Возвращает словарь с настройками шрифтов

    Returns:
        Словарь с настройками шрифтов для разных элементов
    """
    return {
        "title": ("Arial", 24, "bold"),
        "exercise": ("Arial", 18),
        "button": ("Arial", 12),
        "text": ("Arial", 14),
    }
