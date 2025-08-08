"""Современные стили и темы оформления для GUI приложения.

Содержит настройки внешнего вида интерфейса в минималистичном стиле.
"""

import tkinter as tk
from tkinter import ttk


# Современная цветовая палитра
COLORS = {
    "primary": "#2563eb",      # Синий
    "primary_hover": "#1d4ed8", # Темнее синий
    "success": "#10b981",     # Зеленый
    "error": "#ef4444",       # Красный
    "warning": "#f59e0b",     # Оранжевый
    "background": "#f8fafc",  # Светло-серый фон
    "surface": "#ffffff",     # Белый
    "text_primary": "#1e293b", # Темно-серый текст
    "text_secondary": "#64748b", # Серый текст
    "border": "#e2e8f0",      # Светло-серая граница
    "shadow": "#00000010",    # Легкая тень
}


def setup_styles() -> None:
    """Настраивает современные стили для приложения"""
    style = ttk.Style()
    style.theme_use("clam")
    
    # Основные стили для фреймов
    style.configure(
        "Card.TFrame",
        background=COLORS["surface"],
        relief="flat",
        borderwidth=1,
    )
    
    style.configure(
        "Main.TFrame",
        background=COLORS["background"],
        relief="flat",
    )
    
    # Стили для заголовков
    style.configure(
        "Title.TLabel",
        font=("SF Pro Display", 32, "bold"),
        foreground=COLORS["text_primary"],
        background=COLORS["background"],
        anchor="center",
    )
    
    style.configure(
        "Subtitle.TLabel",
        font=("SF Pro Display", 16),
        foreground=COLORS["text_secondary"],
        background=COLORS["background"],
        anchor="center",
    )
    
    # Стили для упражнений
    style.configure(
        "Exercise.TLabel",
        font=("SF Pro Display", 28, "bold"),
        foreground=COLORS["text_primary"],
        background=COLORS["surface"],
        anchor="center",
    )
    
    style.configure(
        "Result.TLabel",
        font=("SF Pro Display", 18),
        foreground=COLORS["text_secondary"],
        background=COLORS["surface"],
        anchor="center",
    )
    
    # Стили для кнопок
    style.configure(
        "Primary.TButton",
        font=("SF Pro Display", 14, "bold"),
        foreground="white",
        background=COLORS["primary"],
        borderwidth=0,
        focuscolor="none",
        relief="flat",
        padding=(20, 12),
    )
    
    style.map(
        "Primary.TButton",
        background=[("active", COLORS["primary_hover"]), ("pressed", COLORS["primary_hover"])],
    )
    
    style.configure(
        "Success.TButton",
        font=("SF Pro Display", 14, "bold"),
        foreground="white",
        background=COLORS["success"],
        borderwidth=0,
        focuscolor="none",
        relief="flat",
        padding=(20, 12),
    )
    
    style.configure(
        "Secondary.TButton",
        font=("SF Pro Display", 14),
        foreground=COLORS["text_primary"],
        background=COLORS["surface"],
        borderwidth=1,
        focuscolor="none",
        relief="flat",
        padding=(20, 12),
    )
    
    # Стили для полей ввода
    style.configure(
        "Modern.TEntry",
        font=("SF Pro Display", 18),
        foreground=COLORS["text_primary"],
        fieldbackground=COLORS["surface"],
        borderwidth=2,
        relief="flat",
        insertcolor=COLORS["primary"],
        padding=(16, 12),
    )
    
    style.map(
        "Modern.TEntry",
        focuscolor=[("focus", COLORS["primary"])],
        bordercolor=[("focus", COLORS["primary"]), ("!focus", COLORS["border"])],
    )
    
    # Стили для статистики
    style.configure(
        "Stats.TLabel",
        font=("SF Pro Display", 14),
        foreground=COLORS["text_secondary"],
        background=COLORS["surface"],
    )
    
    style.configure(
        "StatsValue.TLabel",
        font=("SF Pro Display", 20, "bold"),
        foreground=COLORS["text_primary"],
        background=COLORS["surface"],
    )


def get_fonts() -> dict:
    """
    Возвращает словарь с настройками шрифтов

    Returns:
        Словарь с настройками шрифтов для разных элементов
    """
    return {
        "title": ("SF Pro Display", 32, "bold"),
        "subtitle": ("SF Pro Display", 16),
        "exercise": ("SF Pro Display", 28, "bold"),
        "button": ("SF Pro Display", 14, "bold"),
        "text": ("SF Pro Display", 14),
        "input": ("SF Pro Display", 18),
        "stats": ("SF Pro Display", 14),
        "stats_value": ("SF Pro Display", 20, "bold"),
    }


def get_colors() -> dict:
    """Возвращает цветовую палитру приложения"""
    return COLORS.copy()
