import httpx
import pytest

from clients.auth.auth_client import AuthClient
from config import config

API_EMAIL = config.app.test_user_email
API_PASSWORD = config.app.test_user_password
API_BASE_URL = config.app.app_url
REQUEST_TIMEOUT = config.api.timeout


# TODO: Fix
@pytest.fixture
async def anonymous_http_client():
    async with httpx.AsyncClient(
        base_url=API_BASE_URL,
        timeout=REQUEST_TIMEOUT,
    ) as client:
        yield client


@pytest.fixture
async def auth_client(anonymous_http_client):
    yield AuthClient(anonymous_http_client)


@pytest.fixture
async def get_cookies(auth_client):
    response = await auth_client.login(
        email=API_EMAIL,
        password=API_PASSWORD,
    )
    return response.client.cookies


@pytest.fixture
async def authorized_http_client(auth_client):
    """Авторизованный клиент"""
    await auth_client.login(
        email=config.app.test_user_email,
        password=config.app.test_user_password,
    )
    yield auth_client
