from playwright.sync_api import Page

from pages.base import BasePage
from config import config
from pathlib import Path


# Авторизация и Регистрация на портале Astanahub
class AuthPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # ============================ Авторизация ============================

        self.WELCOME = page.get_by_text("Перейти в HubID")

        #  Логин
        self.LOGIN_STEP = page.locator("div[x-show=\"step === 'login'\"]")
        self.LOGIN = self.LOGIN_STEP.locator("input[name=value]")
        self.EMAIL_AUTH_BTN = self.LOGIN_STEP.locator("button[type=submit]")
        self.JOIN_SPAN = self.LOGIN_STEP.locator("span.underline")

        #  Пароль
        self.PASSWORD_STEP = page.locator("div[x-show=\"step === 'password'\"]")
        self.PASSWORD = self.PASSWORD_STEP.locator("input[name=password]")
        self.PASSWORD_AUTH_BTN = self.PASSWORD_STEP.locator("button[type=submit]")

        # ============================ Политика конфиденциальности ============================
        self.PRIVACY_POLICY_STEP = page.locator(
            "div[x-show=\"step === 'privacy_policy'\"]"
        )
        self.PRIVACY_CHECKBOX = self.PRIVACY_POLICY_STEP.locator("input[type=checkbox]")
        self.PRIVACY_CONTINUE_BTN = self.PRIVACY_POLICY_STEP.locator("button")
        self.PRIVACY_READ = self.PRIVACY_POLICY_STEP.locator(
            "div[x-show=showPrivacyRead]"
        )
        self.PRIVACY_SCROLL = self.PRIVACY_POLICY_STEP.locator("div.overflow-auto")

        # ============================ Регистрация ============================
        self.SIGNUP_STEP = page.locator("div[x-show=\"step === 'signup'\"]")
        self.SIGNUP_EMAIL_INPUT = self.SIGNUP_STEP.locator("input")
        self.SIGNUP_SUBMIT = self.SIGNUP_STEP.locator("button[type=submit]")

        self.OTP_STEP = page.locator("form[data_tag=submitOTP]:visible")
        self.OTP_CODE_INPUT = self.OTP_STEP.locator("input[name=code]")
        self.OTP_SUBMIT = self.OTP_STEP.locator("button[type=submit]")

        self.SIGNUP_PASSWORD_STEP = page.locator("form[data_tag=set_password]")
        self.SIGNUP_PASSWORD_INPUT = self.SIGNUP_PASSWORD_STEP.locator("input")
        self.SIGNUP_PASSWORD_SUBMIT = self.SIGNUP_PASSWORD_STEP.locator(
            "button[type=submit]"
        )

        self.SIGNUP_USER_INFO_STEP = page.locator("form[data_tag=set_names]")
        self.SIGNUP_USER_INFO_NAME = self.SIGNUP_USER_INFO_STEP.locator(
            "input[name=first_name]"
        )
        self.SIGNUP_USER_INFO_SURNAME = self.SIGNUP_USER_INFO_STEP.locator(
            "input[name=last_name]"
        )
        self.SIGNUP_USER_INFO_SUBMIT = self.SIGNUP_USER_INFO_STEP.locator(
            "button[type=submit]"
        )

        # ============================ Фото профиля ============================

        self.PROFILE_PHOTO_STEP = page.locator("form[data_tag=set_photo]")
        self.PROFILE_PHOTO_ATTACH = self.PROFILE_PHOTO_STEP.locator("input[type=file]")
        self.PROFILE_PHOTO_BTN = self.PROFILE_PHOTO_STEP.locator("button[type=submit]")
        self.PROFILE_PHOTO_FILE = Path("testdata/files/profile_photo.png")

        # ============================ Роль пользователя ============================
        self.ROLE_STEP = page.locator("form[data_tag=set_community_role]")
        self.ROLES_LIST = self.ROLE_STEP.locator("label")
        self.ROLE_BTN = self.ROLE_STEP.locator("button[type=submit]")

    # ============================ Сингл таск функции ============================
    def navigate(self):
        """Переход на страницу логина. :return: ответ страницы — статус проверяется в тесте"""
        self.page.set_default_timeout(100000)
        with self.page.expect_response("**/ru/s/auth/login/") as resp:
            self.page.goto(f"{config.app.app_url}/ru/s/auth/login/", wait_until="load")

        self.page.set_default_timeout(30000)
        return resp.value

    def welcome_hubid(self):
        self.page.wait_for_load_state("networkidle")
        if self.WELCOME.is_visible():
            self.WELCOME.click()

    def click_auth_password_continue_btn(self):
        """
        Клик на продолжить при вводе пароля Авторизация
        :return: ответ auth/email — статус проверяется в тесте
        """
        with self.page.expect_response(
            "**/s/auth/api/v1/auth/email/"
        ) as response_info:
            self.PASSWORD_AUTH_BTN.click()

        return response_info.value

    def input_email_or_phone(self, value):
        """
        Ввод почты или телефона при авторизации
        :param value: Email or Phone
        :return:
        """
        input_field = self.LOGIN
        if not input_field:
            self.page.reload()
        input_field.fill(value)

    def click_auth_email_continue_btn(self):
        """
        Клик по кнопке продолжить при вводе почты
        :return: ответ auth/check — статус и user_exists проверяются в тесте
        """
        with self.page.expect_response(
            "**/s/auth/api/v1/auth/check/"
        ) as response_info:
            self.EMAIL_AUTH_BTN.click()

        return response_info.value

    def click_reg_continue_btn(self, is_auth_step: bool = True):
        """
        Клик продолжить на шаге почты
        :param is_auth_step: True — кнопка шага авторизации, False — шага регистрации
        :return: ответ auth/check — статус проверяется в тесте
        """
        with self.page.expect_response("**/s/auth/api/v1/auth/check/") as resp:
            if is_auth_step:
                self.EMAIL_AUTH_BTN.click()
            else:
                self.SIGNUP_SUBMIT.click()

        return resp.value

    def input_password(self, password):
        """
        Ввод пароля при авторизации
        :param password: Пароль
        """
        input_field = self.PASSWORD
        input_field.fill(password)

    def click_registration_span(self):
        """
        Нажатие на кнопку "Присоединиться к Astanahub..."
        """
        self.JOIN_SPAN.click()

    def toggle_privacy_checkbox(self, always_checked: bool = True):
        """
        Отмечает чекбокс в политике конфиденциальности
        :param always_checked: если True то чек бокс всегда отмечен, если False отмечает/снимает отметку
        """
        if not self.PRIVACY_CHECKBOX.is_checked() and always_checked:
            self.PRIVACY_CHECKBOX.check()

        if not always_checked:
            self.PRIVACY_CHECKBOX.check()

    def scroll_privacy_policy(self):
        """Скролл текста политики конфиденциальности до конца"""
        self.PRIVACY_SCROLL.evaluate("el => el.scrollTop = el.scrollHeight")

    def accept_privacy_policy(self):
        """
        Чекбокс + скролл соглашения + клик продолжить
        :return: ответ privacy_policy_accept — статус проверяется в тесте
        """
        self.toggle_privacy_checkbox()
        self.scroll_privacy_policy()

        with self.page.expect_response(
            "**/s/auth/api/v1/auth/privacy_policy_accept/"
        ) as resp:
            self.PRIVACY_CONTINUE_BTN.click()

        return resp.value

    def privacy_continue_without_scroll(self):
        """
        Клик продолжить без скролла соглашения —
        появление уведомления PRIVACY_READ проверяется в тесте
        """
        self.toggle_privacy_checkbox()
        self.PRIVACY_CONTINUE_BTN.click()

    def get_email_input_text(self) -> str:
        """
        :return: текст, подтянувшийся в инпут почты на шаге регистрации — сверяется в тесте
        """
        self.page.set_default_timeout(90000)

        result = self.get_input_value("form[data_tag=start_registration] input")

        self.page.set_default_timeout(30000)
        return result

    def input_registration_code(self, code="111111"):
        """
        Ввод кода с почты при регистрации
        :param code:
        """
        self.OTP_CODE_INPUT.fill(code)

        with self.page.expect_response(
            "**/s/auth/api/v1/auth/activation_confirm/"
        ) as response:
            self.OTP_SUBMIT.click()

        return response.value

    def set_password(self, password):
        """
        Создание пароля при регистрации
        :param password: Пароль учетки
        """
        for i in self.SIGNUP_PASSWORD_INPUT.all():
            i.fill(password)

        with self.page.expect_response(
            "**/s/auth/api/v1/flow/set_password/"
        ) as response:
            self.SIGNUP_PASSWORD_SUBMIT.click()

        return response.value

    def fill_user_info(self, name, surname):
        """
        Ввод имени и фамилии при регистрации
        :param name: Имя юзера
        :param surname: Фамилия юзера
        """
        self.SIGNUP_USER_INFO_NAME.fill(name)
        self.SIGNUP_USER_INFO_SURNAME.fill(surname)
        with (
            self.page.expect_response("**/s/auth/api/v1/flow/set_names/") as response,
            (
                self.page.expect_navigation(url="**/account/v2/main/**")
                if config.app.subdomain == "dev"
                else self.page.expect_navigation(url="**/account/v2/onboarding/**")
            ) as resp,
        ):
            self.SIGNUP_USER_INFO_SUBMIT.click()

        return response.value, resp.value

    def upload_profile_photo(self) -> dict:
        """
        Прикрепление и загрузка фото профиля при регистрации
        :return: словарь ответов по шагам — статусы проверяются в тесте
        """
        with self.page.expect_response(
            f"blob:https://{config.app.subdomain}.astanahub.com/**"
        ) as attach_resp:
            self.PROFILE_PHOTO_ATTACH.set_input_files(self.PROFILE_PHOTO_FILE)

        with (
            self.page.expect_response("**/account/api/media_file/") as file_resp,
            self.page.expect_response(
                "**/account/api/user/update_profile/"
            ) as update_resp,
            self.page.expect_response(
                "**/account/api/v2/onboarding/set_photo/"
            ) as set_resp,
        ):
            self.PROFILE_PHOTO_BTN.click()

        return {
            "attach": attach_resp.value,
            "file": file_resp.value,
            "update": update_resp.value,
            "set": set_resp.value,
        }

    def select_role(self):
        """Выбор первой роли — количество ролей проверяется в тесте по ROLES_LIST"""
        self.ROLES_LIST.first.click()
        self.ROLE_BTN.click()

    #   ====================================== Обобщенные функции ======================================

    def email_auth(self, email, password):
        """
        Авторизация через почту (хелпер: полный флоу без проверок)
        :param email: Почта
        :param password: Пароль
        :return: ответ auth/email — статус проверяется в тесте
        """
        self.navigate()

        self.input_email_or_phone(email)

        self.click_auth_email_continue_btn()

        self.input_password(password=password)

        response = self.click_auth_password_continue_btn()

        self.page.wait_for_url("**/account/v2/main/", wait_until="networkidle")

        self.page.keyboard.press("Escape")

        return response
