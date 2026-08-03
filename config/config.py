from dataclasses import dataclass
from config.browser_config import BrowserConfig
from config.environment import get_env
from dataclasses import dataclass, field


class APIConfig:
    """Конфигурация для API тестов"""

    timeout: int = int(get_env("API_TIMEOUT", "30000"))
    retry_attempts: int = int(get_env("API_RETRY_ATTEMPTS", "3"))
    retry_delay: int = int(get_env("API_RETRY_DELAY", "10000"))

    # Headers
    default_headers: dict | None = None

    def __init__(self):
        """Инициализация заголовков по умолчанию"""
        if self.default_headers is None:
            self.default_headers = {
                "Content-Type": "application/json",
                "User-Agent": "PlaywrightTestBot/1.0",
            }


class AppConfig:
    """Конфигурация приложения"""

    base_domain: str = get_env("BASE_DOMAIN", "astanahub.com")
    subdomain: str = get_env("ENV", "dev")


    # URLs
    app_url: str = f"https://{'' if subdomain == 'prod' else subdomain + '.'}astanahub.com"
    admin_url: str = get_env("ADMIN_URL", "astanahub.com/secretadmin")

    # Окружение
    env: str = get_env("ENV", "dev")  # dev, qa, staging, prod

    # Логирование
    log_level: str = get_env("LOG_LEVEL", "INFO")  # DEBUG, INFO, WARNING, ERROR

    # Тестовые учетные данные (для локальной разработки!)
    test_user_email: str = get_env("TEST_USER_EMAIL", "test@example.com")
    test_user_password: str = get_env("TEST_USER_PASSWORD", "Pass1234!")

    _users_raw: str = get_env("TEST_USERS", "")

    # API токены
    api_token: str = get_env("API_TOKEN", None)
    admin_token: str = get_env("ADMIN_TOKEN", None)


    @property
    def user_pool(self) -> list[tuple[str, str]]:
        if not self._users_raw:
            # Пул не задан — работаем как раньше, с одним пользователем
            return [(self.test_user_email, self.test_user_password)]
        return [
            tuple(pair.split(":", 1))
            for pair in self._users_raw.split(",")
        ]

    def set_subdomain(self, subdomain: str):
        self.subdomain = subdomain
        self.env = subdomain
        self.update_app_url()

    def update_app_url(self):
        """
        Обновить полный URL приложения с учетом поддомена.
        """
        domain = self.base_domain.removeprefix("https://").removeprefix("http://")
        if self.subdomain and self.env != 'prod':
            self.app_url = f"https://{self.subdomain}.{domain}"
            return
        self.app_url = f"https://{domain}"


@dataclass
class Config:
    """
    Главный класс конфигурации
    Используется везде в проекте.

    Usage:
        from config import Config

        browser_config = Config.browser
        app_url = Config.app.app_url
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
    def print_config(cls) -> None:
        """Вывести конфиг"""
        print("\n" + "=" * 50)
        print("PLAYWRIGHT TEST CONFIGURATION")
        print("=" * 50)
        print(f"Environment: {cls.app.env}")
        print(f"Subdomain: {cls.app.subdomain}")
        print(f"App URL: {cls.app.app_url}")
        print(f"API timeout: {cls.api.timeout}ms")
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
