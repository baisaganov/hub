import pytest

from pages.base import ArmBasePage
from pages.account_page import AccountPage
from pages.accreditation_page import AccreditationPage

from pages.auth_page import AuthPage
from pages.business_plan_page import BusinessPlanPage
from api.admin_api import AdminAPI

from pages import *
from pages.events_page import EventPage

from config import config

from datetime import date, datetime

from pages.main_page import MainPage


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


@pytest.fixture
def main_page(page):
    return MainPage(page)


# @pytest.fixture
# def admin_api():
#     return AdminAPI()


@pytest.fixture
def email_test_user():
    """Тестовый пользователь почтой"""
    return {
        "email": config.app.test_user_email,
        "password": config.app.test_user_email,
        "company_id": 16226,
    }


@pytest.fixture
def email_test_user_registration():
    """Тестовый юзер для регистрации"""

    return {
        "email": f"{date.today()}-{datetime.now().hour}-{datetime.now().minute}@test.hub",
        "password": config.app.test_user_password,
        "name": "Autotest",
        "surname": f"{date.today()}_{datetime.now().hour}",
    }


@pytest.fixture()
def phone_test_user():
    return {
        "phone": 87777777777,
        "password": config.app.test_user_email,
    }
