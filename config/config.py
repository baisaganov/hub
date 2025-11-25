from dataclasses import dataclass
from config.browser_config import BrowserConfig
from config.environment import get_env
from dataclasses import dataclass, field


# @dataclass
class APIConfig:
    """Конфигурация для API тестов"""

    base_url: str = get_env("API_BASE_URL", "https://dev.astanahub.com")
    timeout: int = int(get_env("API_TIMEOUT", "30000"))
    retry_attempts: int = int(get_env("API_RETRY_ATTEMPTS", "3"))
    retry_delay: int = int(get_env("API_RETRY_DELAY", "10000"))

    # Headers
    default_headers: dict = None

    def __post_init__(self):
        """Инициализация заголовков по умолчанию"""
        if self.default_headers is None:
            self.default_headers = {
                "Content-Type": "application/json",
                "User-Agent": "PlaywrightTestBot/1.0",
            }


# @dataclass
class AppConfig:
    """Конфигурация приложения"""

    base_domain: str = get_env("BASE_DOMAIN", "astanahub.com")
    subdomain: str = ""


    # URLs
    app_url: str = None
    admin_url: str = get_env("ADMIN_URL", "astanahub.com/secretadmin")

    # Окружение
    env: str = get_env("ENV", "dev")  # dev, qa, staging, prod

    # Логирование
    log_level: str = get_env("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR

    # Тестовые учетные данные (для локальной разработки!)
    test_user_email: str = get_env("TEST_USER_EMAIL", "test@example.com")
    test_user_password: str = get_env("TEST_USER_PASSWORD", "password123")

    # API токены
    api_token: str = get_env("API_TOKEN", None)
    admin_token: str = get_env("ADMIN_TOKEN", None)

    def set_subdomain(self, subdomain: str):
        self.subdomain = subdomain

    def update_app_url(self):
        """
        Обновить полный URL приложения с учетом поддомена.
        """
        if self.subdomain:
            self.app_url = f"https://{self.subdomain}.{self.base_domain}"
            return
        self.app_url = f"https://{self.base_domain}"


@dataclass
class Config:
    """
    Главный класс конфигурации
    Используется везде в проекте.

    Usage:
        from config import Config

        browser_config = Config.browser
        app_url = Config.app.app_url
        api_base_url = Config.api.base_url
    """

    browser: BrowserConfig = BrowserConfig()  # field(default_factory=BrowserConfig)
    api: APIConfig = APIConfig()  # field(default_factory=APIConfig)
    app: AppConfig = AppConfig()  # field(default_factory=AppConfig)

    @classmethod
    def is_production(cls) -> bool:
        """Проверить что это production окружение"""
        return cls.app.env == "prod"

    @classmethod
    def is_local(cls) -> bool:
        """Проверить что это dev разработка"""
        return cls.app.env == "dev"

    @classmethod
    def is_qa(cls) -> bool:
        """Проверить что это qa разработка"""
        return cls.app.env == "qa"

    @classmethod
    def get_base_url(cls) -> str:
        """Получить базовый URL приложения"""
        return cls.app.app_url

    @classmethod
    def get_api_base_url(cls) -> str:
        """Получить базовый URL API"""
        return cls.api.base_url

    @classmethod
    def print_config(cls) -> None:
        """Вывести конфиг"""
        print("\n" + "=" * 50)
        print("PLAYWRIGHT TEST CONFIGURATION")
        print("=" * 50)
        print(f"Environment: {cls.app.env}")
        print(f"App URL: {cls.app.app_url}")
        print(f"API URL: {cls.api.base_url}")
        print(f"Browser: {cls.browser.browser_type}")
        print(f"Headless: {cls.browser.headless}")
        print(f"Viewport: {cls.browser.viewport_width}x{cls.browser.viewport_height}")
        print(f"Timeout: {cls.browser.timeout}ms")
        print("=" * 50 + "\n")

# === Быстрый доступ ===
# Можно импортировать как:
# from config.config import Config
# Config.browser.headless
# Config.app.app_url
# Config.api.base_url
