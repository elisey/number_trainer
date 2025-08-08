"""
Основной класс GUI приложения для математического тренажера.

Содержит интерфейс на tkinter и интеграцию с бизнес-логикой.
"""

import tkinter as tk
from tkinter import ttk

from .styles import setup_styles, get_fonts


class NumberTrainerApp:
    """Основной класс GUI приложения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Number Trainer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        self.setup_styles()
        
        # Create main interface
        self.create_widgets()
    
    def setup_styles(self):
        """Configure the application styles"""
        setup_styles()
    
    def create_widgets(self):
        """Create and arrange the main widgets"""
        fonts = get_fonts()
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="Number Trainer", 
            font=fonts['title']
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Content area
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Placeholder content
        welcome_label = ttk.Label(
            content_frame,
            text="Добро пожаловать в Number Trainer!\nЗдесь будет ваше приложение.",
            font=fonts['text'],
            justify=tk.CENTER
        )
        welcome_label.grid(row=0, column=0, pady=50)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(20, 0))
        
        # Sample button
        start_button = ttk.Button(
            button_frame,
            text="Начать тренировку",
            command=self.start_training
        )
        start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Exit button
        exit_button = ttk.Button(
            button_frame,
            text="Выход",
            command=self.root.quit
        )
        exit_button.pack(side=tk.LEFT)
    
    def start_training(self):
        """Handle start training button click"""
        print("Начинаем тренировку...")
        # TODO: Implement training logic
