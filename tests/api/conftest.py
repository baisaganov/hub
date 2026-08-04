import httpx
import pytest

from clients.auth.auth_client import AuthClient
from clients.events_client import EventsClient
from config import config
from clients.user.user_client import UserClient

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
async def authorized_http_client(get_cookies):
    cookies = get_cookies

    async with httpx.AsyncClient(
        base_url=API_BASE_URL,
        timeout=REQUEST_TIMEOUT,
        cookies=cookies
    ) as client:
        yield client

@pytest.fixture
async def auth_client(anonymous_http_client):
    yield AuthClient(anonymous_http_client)


@pytest.fixture
async def get_cookies(auth_client):
    await auth_client.login(
        email=API_EMAIL,
        password=API_PASSWORD,
    )
    # login возвращает модель, куки сессии оседают в jar httpx-клиента
    return auth_client.client.cookies


@pytest.fixture 
async def user_client(authorized_http_client):
    yield UserClient(authorized_http_client)


@pytest.fixture
async def events_client(anonymous_http_client):
    yield EventsClient(anonymous_http_client)