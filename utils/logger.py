"""
Centralized logging configuration.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

from config import config


class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Настройка корневого логгера
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        # === File handler ===
        file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        match config.app.log_level:
            case 'DEBUG':
                root_logger.setLevel(logging.DEBUG)
                file_handler.setLevel(logging.DEBUG)
            case 'INFO':
                root_logger.setLevel(logging.INFO)
                file_handler.setLevel(logging.DEBUG)
            case 'WARNING':
                root_logger.setLevel(logging.WARNING)
                file_handler.setLevel(logging.DEBUG)
            case 'ERROR':
                root_logger.setLevel(logging.ERROR)
                file_handler.setLevel(logging.DEBUG)

        # === Console handler (только INFO+) ===
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)-8s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)

        # Добавляем handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        # Отключаем verbose логи от сторонних библиотек
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("selenium").setLevel(logging.WARNING)
        logging.getLogger("playwright").setLevel(logging.WARNING)

    def get_logger(self, name: str):
        """Get logger instance for specific module"""
        return logging.getLogger(name)
