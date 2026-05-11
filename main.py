#!/usr/bin/env python3
"""
Настольное приложение для A/B тестирования.
Точка входа в приложение.

Приложение предоставляет графический интерфейс для анализа результатов
A/B тестов с использованием статистических методов и интерактивных
визуализаций. Реализовано в процедурном стиле без использования классов.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import main_window


def main():
    """Главная точка входа в приложение."""
    try:
        main_window.build_app()
        main_window.run()
    except ImportError as e:
        print("Ошибка: отсутствуют необходимые зависимости.")
        print("Установите требуемые пакеты командой:")
        print("pip install -r requirements.txt")
        print(f"\nПодробности ошибки: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при запуске приложения: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
