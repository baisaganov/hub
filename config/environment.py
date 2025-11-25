import os
from dotenv import load_dotenv

load_dotenv()


class Environment:
    """Класс для управления переменными окружения"""

    @staticmethod
    def get(key: str, default: str = None) -> str:
        """
        Получить переменную окружения.

        Args:
            key: Название переменной
            default: Значение по умолчанию

        Returns:
            Значение переменной или default
        """
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Значение переменной окружения '{key}' не установлено")
        return value

    @staticmethod
    def get_int(key: str, default: int = None) -> int:
        """Получить целое число из переменной окружения"""
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"Значение переменной окружения '{key}' не установлено")
        return int(value)

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        """Получить true/false из переменной окружения"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')


def get_env(key: str, default: str = None) -> str:
    return Environment.get(key, default)


def get_env_int(key: str, default: int = None) -> int:
    return Environment.get_int(key, default)


def get_env_bool(key: str, default: bool = False) -> bool:
    return Environment.get_bool(key, default)
