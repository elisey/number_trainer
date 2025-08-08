"""
Точка входа для Number Trainer приложения.

Запускает GUI версию математического тренажера.
"""

import tkinter as tk
from src.number_trainer.gui.app import NumberTrainerApp


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = NumberTrainerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
