import random

import playwright._impl._errors

from playwright.sync_api import Page

from commons.types import AdminFuncTypes, AdminAccountChangeType
from api.admin_api import AdminAPI
from pages.base import BasePage
from config import config


# Главная страница портала
class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.LOGIN_BTN = page.locator("a[href^='/s/auth/login/?']")
        self.SIGNUP_BTN = page.locator("a[href^='/s/auth/signup/?']")

    def navigate(self):
        self.page.set_default_timeout(90000)

        with self.page.expect_response(f'{config.app.app_url}/ru') as resp:
            self.page.goto(f'{config.app.app_url}/ru')

        assert resp.value.status in [200, 301], f'MainPage: Страница не доступна {resp.value.status}'

        self.page.set_default_timeout(30000)

    def login_click(self):
        self.page.set_default_timeout(90000)

        with self.page.expect_response('**/ru/s/auth/login/**') as resp:
            self.LOGIN_BTN.click()

        self.page.set_default_timeout(30000)

        assert resp.value.status == 200, f'MainPage: Страница не доступна {resp.value.status}'
        assert resp.value.request.header_value('cookie').find('csrftoken') == -1, f"Auth page: Юзер уже авторизован"
