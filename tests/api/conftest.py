"""
Fixtures для API тестов.
"""

import pytest
from api.admin_api import AdminAPI
from config import config


@pytest.fixture
async def authenticated_admin():
    """
    API клиент с авторизацией.
    Специфично для API тестов.
    """
    api = config.api.get
    token = await api.login()
    api.set_token(token)

    yield api

    # Cleanup (опционально)
    await api.logout()


