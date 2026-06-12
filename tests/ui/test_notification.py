import allure
import pytest

from playwright.sync_api import Page
from config import config
from pages import notification_page
from pages.auth_page import AuthPage
from pages.notification_page import NotificationPage


@allure.title("Переход в уведомления")
def test_notification_page(page, auth_page: AuthPage, base_user_creds, main_page, notification_page):
    with allure.step("Авторизация"):
        auth_page.email_auth(base_user_creds['email'], password=base_user_creds['password'])

    with allure.step("Переход к Уведомлению"):
        notification_page.NOTIFICATION_BTN.click()
        assert "/notifications/" in page.url, f"Не перешли на страницу уведомлений, текущий URL: {page.url}"


