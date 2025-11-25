import pytest

from pages.base import ArmBasePage
from pages.account_page import AccountPage
from pages.accreditation_page import AccreditationPage

from pages.auth_page import AuthPage
from pages.business_plan_page import BusinessPlanPage
from api.admin_api import AdminAPI

from pages import *
from pages.events_page import EventPage


@pytest.fixture
def auth_page(page):
    return AuthPage(page)


@pytest.fixture
def admin():
    return AdminAPI()


@pytest.fixture
def account_page(page):
    return AccountPage(page)


@pytest.fixture
def accreditation_page(page):
    return AccreditationPage(page)


@pytest.fixture
def arm_base_page(page):
    return ArmBasePage(page)


@pytest.fixture
def business_plan_page(page):
    return BusinessPlanPage(page)


@pytest.fixture
def ecp_page(page):
    return EcpPage(page)


@pytest.fixture
def event_page(page):
    return EventPage(page)


# @pytest.fixture
# def admin_api():
#     return AdminAPI()


@pytest.fixture
def test_user():
    """Тестовый пользователь"""
    from config import Config
    return {
        "email": Config.app.test_user_email,
        "password": Config.app.test_user_password,
        "company_id": 16226,
    }