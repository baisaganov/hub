

from playwright.sync_api import Page, expect


from pages.base import BasePage
from config import config


# Главная страница портала
class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.LOGIN_BTN = self.page.locator("a[href*='/login/?next=/']")
        self.SIGNUP_BTN = self.page.locator("a[href*='/signup/?next=/']")
        self.INTRO_TOUR_CLOSE = self.page.locator("#intro-tour-modal_close")
        self.EVENTS_LINK = self.page.locator("a[href*='event']").nth(1)
        self.VACANCY_LINK = self.page.locator("a[href*='vacancy']").nth(1)

        # ===== USER MENU DROPDOWN =====
        self.USER_MENU_DROPDOWN_OPEN = self.page.locator("#user-menu-dropdown-click")
        self.USER_MENU_DROPDOWN = self.page.locator("#user-menu-dropdown")

    def open_page_from_menu(self, page_name: str):
        with self.page.expect_response(f"**/{page_name}/") as response:
                self.page.keyboard.press("Escape")
                self.EVENTS_LINK.click()
                try:
                    self.EVENTS_LINK.click()
                except Exception:
                    pass

        # expect_response срабатывает по заголовкам ответа — дожидаемся самой навигации
        self.page.wait_for_url(f"**/{page_name}/")
        return response
        

    def navigate(self):
        """Переход на главную. :return: ответ страницы — статус проверяется в тесте"""
        self.page.set_default_timeout(90000)

        with self.page.expect_response(f"{config.app.app_url}/ru") as resp:
            self.page.goto(f"{config.app.app_url}/ru", wait_until="domcontentloaded")

        self.page.set_default_timeout(5000)
        if self.INTRO_TOUR_CLOSE.is_visible():
            self.INTRO_TOUR_CLOSE.click()

        self.page.set_default_timeout(30000)
        return resp.value

    def login_click(self):
        """Клик "Войти". :return: ответ страницы логина — статус и куки проверяются в тесте"""
        self.page.set_default_timeout(90000)

        with self.page.expect_response("**/login/**") as resp:
            self.LOGIN_BTN.click()

        self.page.set_default_timeout(30000)
        return resp.value

    def open_user_profile(self):
        """Переход в профиль через меню юзера. :return: ответ страницы профиля"""
        expect(self.USER_MENU_DROPDOWN_OPEN).to_be_visible()
        self.USER_MENU_DROPDOWN_OPEN.click()

        expect(self.USER_MENU_DROPDOWN).to_be_visible()

        with self.page.expect_response("**/profile/activity/") as response:
            self.USER_MENU_DROPDOWN.locator("a").first.click()

        return response.value
