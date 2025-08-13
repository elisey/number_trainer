# Entry point for Number Trainer application.

import tkinter as tk

from src.number_trainer.gui.app import NumberTrainerApp


def main() -> None:
    """Main application entry point"""
    root = tk.Tk()
    NumberTrainerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
