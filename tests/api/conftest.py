import httpx
import pytest

from clients.auth_client import AuthClient
from config import config

API_EMAIL = config.app.test_user_email
API_PASSWORD = config.app.test_user_password
API_BASE_URL = config.app.app_url
REQUEST_TIMEOUT = config.api.timeout


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
async def access_token(auth_client):
    token = await auth_client.login(
        email=API_EMAIL,
        password=API_PASSWORD,
    )
    return token


@pytest.fixture
def auth_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


@pytest.fixture
async def authorized_http_client(auth_headers):
    """Авторизованный клиент"""
    async with httpx.AsyncClient(
        base_url=API_BASE_URL,
        headers=auth_headers,
        timeout=REQUEST_TIMEOUT,
    ) as client:
        yield client


@pytest.fixture
async def users_client(authorized_http_client):
    yield AuthClient(authorized_http_client)


@pytest.fixture
async def created_user(users_client):
    user = await users_client.create_user(
        name="Test User",
        email="test_user@example.com",
        role="user",
    )

    yield user

    await users_client.delete_user(user["id"])
