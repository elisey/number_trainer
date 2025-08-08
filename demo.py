#!/usr/bin/env python3
"""
Демо-скрипт для Number Trainer.

Показывает возможности консольной версии математического тренажера.
"""

from src.number_trainer.cli.console import run_console_trainer


def main():
    """Запуск демо-версии тренажера"""
    print("🎯 Демо Number Trainer")
    print("=" * 30)
    
    # Запускаем консольную версию с настройками по умолчанию
    run_console_trainer(min_digits=1, max_digits=3, num_exercises=10)


if __name__ == "__main__":
    main()
