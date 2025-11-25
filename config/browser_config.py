from dataclasses import dataclass
from typing import Optional, List
from config.environment import get_env_bool, get_env_int, get_env


# @dataclass
class BrowserConfig:
    """Конфигурация браузера"""

    # === Основные настройки ===
    headless: bool = get_env_bool("HEADLESS", True)  # Видимость браузера
    browser_type: str = get_env("BROWSER", "chromium")  # chromium, firefox, webkit
    slow_mo: int = get_env_int("SLOW_MO", 0)  # Замедление в миллисекундах (для отладки)

    # === Viewport (размер окна) ===
    viewport_width: int = get_env_int("VIEWPORT_WIDTH", 1920)
    viewport_height: int = get_env_int("VIEWPORT_HEIGHT", 1080)

    # === Timeouts (ожидания) ===
    timeout: int = get_env_int("TIMEOUT", 30000)  # 30 сек - глобальный timeout
    navigation_timeout: int = get_env_int("NAVIGATION_TIMEOUT", 30000)  # Timeout навигации

    # === Браузер аргументы ===
    args: List[str] = None
    proxy: Optional[dict] = None
    downloads_path: Optional[str] = get_env("DOWNLOADS_PATH", None)

    # === Emulation (эмуляция устройств) ===
    user_agent: Optional[str] = get_env("USER_AGENT", None)
    locale: str = get_env("LOCALE", "en-US")
    timezone: str = get_env("TIMEZONE", "UTC")

    # === Трассировка и запись ===
    trace: str = get_env("TRACE", "off")  # off, on, retain-on-failure
    screenshot: str = get_env("SCREENSHOT", "off")  # off, only-on-failure, on
    video: str = get_env("VIDEO", "off")  # off, retain-on-failure, on

    def __post_init__(self):
        """Инициализация после создания dataclass"""
        # Если args не установлены, создаем пустой список
        if self.args is None:
            self.args = []

        # Добавляем аргументы для корпоративного прокси (если есть)
        if self.proxy:
            self.args.append(f"--proxy-server={self.proxy['server']}")

    @property
    def launch_options(self) -> dict:
        """Опции для browser.launch()"""
        return {
            "headless": self.headless,
            "slow_mo": self.slow_mo,
            "args": self.args,
            "proxy": self.proxy,
            "downloads_path": self.downloads_path,
        }

    @property
    def context_options(self) -> dict:
        """Опции для browser.new_context()"""
        options = {
            "viewport": {
                "width": self.viewport_width,
                "height": self.viewport_height,
            },
            "user_agent": self.user_agent,
            "locale": self.locale,
            "timezone_id": self.timezone,
        }

        # Добавляем опции трассировки
        if self.trace != "off":
            options["record_video_dir"] = "videos/" if self.video != "off" else None

        return options

    def get_viewport(self) -> dict:
        """Получить viewport размер"""
        return {
            "width": self.viewport_width,
            "height": self.viewport_height,
        }

    def get_device_emulation(self, device_name: str = None) -> dict:
        """
        Получить опции для эмуляции устройства

        Args:
            device_name: Название устройства (iPhone 12, Pixel 5 и т.д.)
        """
        devices = {
            "iPhone 12": {
                "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
                "viewport": {"width": 390, "height": 844},
                "device_scale_factor": 3,
                "is_mobile": True,
                "has_touch": True,
            },
            "Pixel 5": {
                "user_agent": "Mozilla/5.0 (Linux; Android 12; Pixel 5 Build/..)",
                "viewport": {"width": 393, "height": 851},
                "device_scale_factor": 2.75,
                "is_mobile": True,
                "has_touch": True,
            },
            "Desktop": {
                "viewport": self.get_viewport(),
                "user_agent": self.user_agent,
            },
        }

        return devices.get(device_name, devices["Desktop"])
