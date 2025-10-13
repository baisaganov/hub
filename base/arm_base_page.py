import time

from base import Page

from base.base_page import BasePage
from config.links import Links


class ArmBasePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.email_field = page.locator('input[name=email]')
        self.password_field = page.locator('input[name=password]')
        self.rnd_checkbox = page.locator('input[name=RnD_policy]')
        self.login_btn = page.locator('button.btn')

    def auth_arm(self, login, password):
        try:
            self.page.goto(Links.ARM_LOGIN)
            self.email_field.fill(login)
            self.password_field.fill(password)
            self.rnd_checkbox.click()

            with self.page.expect_response('https://dev.astanahub.com/arm/login/') as response:
                self.login_btn.click()
                self.logging.info('Auth ARM: Login btn clicked')

            assert response.value.status == 200, self.error_info(status=response.value.status,
                                                                 msg="ARM: Login success")

        except Exception as e:
            assert 1 == 0, self.error_info(msg="ARM: Login error", exception=e)

    def logout_arm(self):
        self.page.evaluate('window.localStorage.clear()')
        self.page.evaluate('window.sessionStorage.clear()')
        self.page.context.clear_cookies()

    def nav(self, url):
        self.page.goto(url)

    def get_button_list(self):
        """
        Возвращает все доступные кнопки действия
        :return: Список доступных кнопок на странице
        """
        time.sleep(4)
        try:
            text_list = self.page.locator('div.request-footer.card-footer').all_inner_texts()[0].split('\n')
            self.logging.info(f'ARM: Доступные кнопки {text_list}')
            return text_list
        except TimeoutError as e:
            1 == 0, self.error_info(msg=f'ARM: Кнопки не получены', exception=e)

    def get_users_list(self):
        time.sleep(5)
        text_list = self.page.locator('ul.user-list').all_text_contents()
        self.logging.info(f'ARM: Доступные пользователи {text_list}')
        return text_list

    def click_on_button(self, button_text, tag="button"):
        if tag == 'span':
            self.page.locator(f'//span[contains(text(), "{button_text}")]').click()
        elif tag == 'button_class':
            self.page.locator(f'{button_text}').click()
        else:
            self.page.get_by_role(role=tag, name=button_text).click()
