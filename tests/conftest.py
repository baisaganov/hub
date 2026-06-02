import pytest


from pages.auth_page import AuthPage

from pages import *
from pages.company_profile_page import CompanyProfilePage
from pages.events_page import EventsPage

from config import config

from datetime import date, datetime

from pages.main_page import MainPage
from pages.user_profile_page import UserProfilePage
from pages.vacancy_page import VacancyPage


@pytest.fixture(scope="session")
def registration_user_creds():
    """Тестовый юзер для регистрации"""
    return {
        "email": f"{date.today()}-{datetime.now().hour}-{datetime.now().minute}@test.hub",
        "password": config.app.test_user_password,
        "name": "Autotest",
        "surname": f"{date.today()}_{datetime.now().hour}",
        "phone": f"8705"
        f"{datetime.now().month if datetime.now().month > 9 else f'0{datetime.now().month}'}"
        f"{datetime.now().day if datetime.now().day > 9 else f'0{datetime.now().day}'}"
        f"{datetime.now().microsecond//1000}",
        "company_name": f"Autotest company {date.today()}-{datetime.now().hour}-{datetime.now().minute}",
    }


@pytest.fixture(scope="session")
def base_user_creds():
    """Зарегестрированный юзер"""
    return {
        "email": config.app.test_user_email,
        "password": config.app.test_user_password,
    }


@pytest.fixture
def auth_page(page):
    """Страница авторизации"""
    return AuthPage(page)


# @pytest.fixture
# def event_page(page):
#     return EventPage(page)


@pytest.fixture
def events_page(page):
    return EventsPage(page)


@pytest.fixture
def main_page(page):
    """Главная страница"""
    return MainPage(page)


@pytest.fixture
def user_profile_page(page):
    return UserProfilePage(page)


@pytest.fixture
def company_profile_page(page):
    return CompanyProfilePage(page)

@pytest.fixture
def vacancy_page(page):
    return VacancyPage(page)
