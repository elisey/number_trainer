"""Modern styles and themes for GUI application.

Contains interface appearance settings in minimalist style.
"""

from tkinter import ttk

# Modern color palette
COLORS = {
    "primary": "#2563eb",  # Blue
    "primary_hover": "#1d4ed8",  # Darker blue
    "success": "#10b981",  # Green
    "error": "#ef4444",  # Red
    "warning": "#f59e0b",  # Orange
    "background": "#f8fafc",  # Light gray background
    "surface": "#ffffff",  # White
    "text_primary": "#1e293b",  # Dark gray text
    "text_secondary": "#64748b",  # Gray text
    "border": "#e2e8f0",  # Light gray border
    "shadow": "#00000010",  # Light shadow
}


def setup_styles() -> None:
    """Sets up modern styles for the application"""
    style = ttk.Style()
    style.theme_use("clam")

    # Main styles for frames
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

    # Styles for headers
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

    # Styles for exercises
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

    # Styles for buttons
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
        background=[
            ("active", COLORS["primary_hover"]),
            ("pressed", COLORS["primary_hover"]),
        ],
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

    # Styles for input fields
    style.configure(
        "Modern.TEntry",
        font=("SF Pro Display", 24),
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

    # Style for input field with error
    style.configure(
        "Error.TEntry",
        font=("SF Pro Display", 24),
        foreground=COLORS["error"],
        fieldbackground=COLORS["surface"],
        borderwidth=2,
        relief="flat",
        insertcolor=COLORS["primary"],
        padding=(16, 12),
    )

    style.map(
        "Error.TEntry",
        focuscolor=[("focus", COLORS["error"])],
        bordercolor=[("focus", COLORS["error"]), ("!focus", COLORS["error"])],
    )

    # Styles for statistics
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
    Returns a dictionary with font settings

    Returns:
        Dictionary with font settings for different elements
    """
    return {
        "title": ("SF Pro Display", 32, "bold"),
        "subtitle": ("SF Pro Display", 16),
        "exercise": ("SF Pro Display", 28, "bold"),
        "button": ("SF Pro Display", 14, "bold"),
        "text": ("SF Pro Display", 14),
        "input": ("SF Pro Display", 24),
        "stats": ("SF Pro Display", 14),
        "stats_value": ("SF Pro Display", 20, "bold"),
    }


def get_colors() -> dict:
    """Returns the application color palette"""
    return COLORS.copy()
