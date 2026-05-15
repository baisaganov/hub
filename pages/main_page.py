import random

import allure
import playwright._impl._errors

from playwright.sync_api import Page, expect

from commons.types import AdminFuncTypes, AdminAccountChangeType
from api.admin_api import AdminAPI
from pages.base import BasePage
from config import config


# Главная страница портала
class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.LOGIN_BTN = page.locator("a[href*='/login/?next=/']")
        self.SIGNUP_BTN = page.locator("a[href*='/signup/?next=/']")
        self.INTRO_TOUR_CLOSE = page.locator("#intro-tour-modal_close")
        self.EVENTS_LINK = page.locator("a[href*='event']").nth(1)

        # ===== USER MENU DROPDOWN =====
        self.USER_MENU_DROPDOWN_OPEN = page.locator("#user-menu-dropdown-click")
        self.USER_MENU_DROPDOWN = page.locator("#user-menu-dropdown")

    def navigate(self):
        self.page.set_default_timeout(90000)

        with self.page.expect_response(f'{config.app.app_url}/ru') as resp:
            self.page.goto(f'{config.app.app_url}/ru', wait_until='domcontentloaded')

        assert resp.value.status in [200, 301], f'MainPage: Страница не доступна {resp.value.status}'

        self.page.set_default_timeout(5000)
        if self.INTRO_TOUR_CLOSE.is_visible():
            self.INTRO_TOUR_CLOSE.click()

        self.page.set_default_timeout(30000)

    def login_click(self):
        self.page.set_default_timeout(90000)

        with self.page.expect_response('**/login/**') as resp:
            self.LOGIN_BTN.click()

        self.page.set_default_timeout(30000)

        assert resp.value.status in [200, 302], f'MainPage: Страница не доступна {resp.value.status}'
        cookies = resp.value.request.header_value('cookie')
        assert (cookies is None
                or cookies.find('csrftoken') == -1), f"Auth page: Юзер уже авторизован"

    def open_user_profile(self):
        self.USER_MENU_DROPDOWN_OPEN.click()
        expect(self.USER_MENU_DROPDOWN).to_be_visible()

        with self.page.expect_response('**/profile/activity/') as response:
            self.USER_MENU_DROPDOWN.locator('a').first.click()

        assert response.value.status == 200



