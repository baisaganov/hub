import pytest

from config import config


@pytest.fixture(scope='session')
def api_base_url():
    """Базовый URL для API-тестов."""
    return config.api.base_url.rstrip('/')


@pytest.fixture(scope='session')
def api_headers():
    """Заголовки по умолчанию для API-запросов."""
    headers = config.api.default_headers.copy() if config.api.default_headers else {}
    headers.setdefault('Accept', 'application/json')
    return headers
