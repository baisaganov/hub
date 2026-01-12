from playwright.sync_api import Page

from pages.base import BasePage


# Авторизация и Регистрация на портале Astanahub
class AuthPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # ============================ Авторизация ============================
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
        self.PRIVACY_POLICY_STEP = page.locator("div[x-show=\"step === 'privacy_policy'\"]")
        self.PRIVACY_CHECKBOX = self.PRIVACY_POLICY_STEP.locator("input[type=checkbox]")
        self.PRIVACY_CONTINUE_BTN = self.PRIVACY_POLICY_STEP.locator("button")
        self.PRIVACY_READ = self.PRIVACY_POLICY_STEP.locator("div[x-show=showPrivacyRead]")
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
        self.SIGNUP_PASSWORD_SUBMIT = self.SIGNUP_PASSWORD_STEP.locator("button[type=submit]")

        self.SIGNUP_USER_INFO_STEP = page.locator("form[data_tag=set_names]")
        self.SIGNUP_USER_INFO_NAME = self.SIGNUP_USER_INFO_STEP.locator("input[name=first_name]")
        self.SIGNUP_USER_INFO_SURNAME = self.SIGNUP_USER_INFO_STEP.locator("input[name=last_name]")
        self.SIGNUP_USER_INFO_SUBMIT = self.SIGNUP_USER_INFO_STEP.locator("button[type=submit]")

        # ============================ К исправлению ============================

        # self.continue_reg_password_btn = page.locator('form[data_tag=set_password] button[type=submit]')
        # self.name_field = page.locator("input[name='first_name']")
        # self.surname_field = page.locator("input[name='last_name']")
        # self.profile_photo_skip = page.locator('div[x-show="step === \'set_photo\'"] button[type=submit]')
        #
        # # self.auth_password_continue_btn = page.locator("div[x-show=\"step === 'password'\"] button[type='submit']")
        # self.continue_btn_signup = page.locator("form[data_tag='start_registration'] > button")
        # self.send_code_btn = page.locator("div[x-show=\"step === 'confirm_email_register'\"] button")
        # self.resend_code_btn = page.locator("div[x-show=\"step === 'confirm_email_register'\"] "
        #                                     "form > div > div > span.cursor-pointer")
        # self.continue_user_info_btn = page.locator("form[data_tag=set_names] button[type=submit]")
        # self.role_select_btn = page.locator('//html/body/div[2]/div[9]/div/div/div[1]')
        # self.role_not_select_btn = page.locator('//html/body/div[2]/div[9]/div/div/div[2]')
        # self.ecp_auth_btn = page.locator("div[x-show=\"step === 'login'\"] button").nth(1)
        #
        # # Photo Form
        # self.set_photo_submit_btn = page.locator('form[data_tag="set_photo"] button[type="submit"]')
        # self.set_photo = page.locator('label.photo')
        #
        # # Select Community Role
        # self.comunity_form = page.locator('form[data_tag=set_community_role]')
        # self.tag_list = self.comunity_form.locator('label')
        # self.tag_continue_btn = self.comunity_form.locator('button[type=submit]')
        #
        # # Reg success
        # self.success_form = page.locator("div[x-show=\"step === 'success'\"]")
        # self.success_btn = self.success_form.locator('div.btn')

    # ============================ Сингл таск функции ============================
    def navigate(self):
        with self.page.expect_response(f'**/ru/s/auth/login/') as resp:
            self.page.goto(f'{self.config.app.app_url}/ru/s/auth/login/')

        assert resp.value.status == 200, f'AuthPage: Страница не доступна {resp.value.status}'

    def click_auth_password_continue_btn(self):
        """
        Клик на продолжить при вводе пароля Авторизация
        :return:
        """
        with self.page.expect_response(f'**/s/auth/api/v1/auth/email/') as response_info:
            self.PASSWORD_AUTH_BTN.click()

        assert response_info.value.status == 200, f"AuthPage: Continue btn 2 clicked error"

    def input_email_or_phone(self, value):
        """
        Ввод почты или телефона при авторизации
        :param value: Email or Phone
        :return:
        """
        input_field = self.LOGIN
        input_field.fill(value)

    def click_auth_email_continue_btn(self, is_auth: bool = True):
        """
        Клик по кнопке продолжить при вводе почты в шаге Авторизация
        :param is_auth: Bool: default True = шаг авторизация; False = шаг регистрация
        """
        with self.page.expect_response(f'**/s/auth/api/v1/auth/check/') as response_info:
            self.EMAIL_AUTH_BTN.click()

        assert response_info is not None, "AuthPage: Пустой ответ при заполнении почты"
        assert response_info.value.status == 200, "AuthPage: Ошибка при клике продолжить"

        if is_auth:
            assert response_info.value.json()['user_exists'] is True, ("AuthPage: Ошибка при авторизации, "
                                                                       "Юзер отсутвует")
        else:
            assert response_info.value.json()['user_exists'] is False, ("AuthPage: Ошибка при авторизации, "
                                                                        "Юзер существует")

    def click_reg_continue_btn(self, is_auth_step: bool = True):
        with self.page.expect_response(f'**/s/auth/api/v1/auth/check/') as resp:
            if is_auth_step:
                self.EMAIL_AUTH_BTN.click()
            else:
                self.SIGNUP_SUBMIT.click()

        assert resp is not None, "AuthPage: Пустой ответ при заполнении почты"
        assert resp.value.status == 200, "AuthPage: Ошибка при клике продолжить"

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
        try:
            self.JOIN_SPAN.click()
        except Exception as e:
            assert 1 == 0, f"AuthPage: Ошибка при нажатии на кнопку \"Присоединиться к Astanahub...\" \n {e}"

    def toggle_privacy_checkbox(self, always_checked: bool = True):
        """
        Отмечает чекбокс в политике конфиденциальности
        :param always_checked: если True то чек бокс всегда отмечен, если False отмечает/снимает отметку
        """
        if not self.PRIVACY_CHECKBOX.is_checked() and always_checked:
            self.PRIVACY_CHECKBOX.check()

        if not always_checked:
            self.PRIVACY_CHECKBOX.check()

    def privacy_continue_btn_click(self, need_scroll: bool = True):
        """
        Метод отмечает чекбокс если не отмечен, делает скролл соглашения если необоходимо и нажимает на продолжить
        Проверки на та что, если скролл не делается, выходит ли уведомление, если скролл сделан не выходит ли или
        скрывается ли уведомление, а также при нажатии на продолжить, успешно ли выполняется запрос

        :param need_scroll: если True то нужен скролл соглашения, в противном случаем клик по кнопке продолжить
        :return:
        """

        self.toggle_privacy_checkbox()

        if need_scroll:
            self.PRIVACY_SCROLL.evaluate('el => el.scrollTop = el.scrollHeight')
            assert self.PRIVACY_READ.is_hidden(), ('AuthPage: Вышло уведомление, что необходимо прочесть политику '
                                                   'конфиденциальности')
            with self.page.expect_response(f'**/s/auth/api/v1/auth/privacy_policy_accept/') as resp:
                self.PRIVACY_CONTINUE_BTN.click()

            assert resp.value.status == 200, f'AuthPage: Политика конф-ти вернула {resp.value.status}'

        else:
            self.PRIVACY_CONTINUE_BTN.click()
            assert self.PRIVACY_READ.is_visible(), (f'AuthPage: Не вышло уведомление, о необходимости прочесть '
                                                    f'политику конфиденциальности')

    def check_email_input_text(self, text):
        """
        Проверка что в инпуте введен верный текст
        :param text: Ожидаемый текст
        """
        self.page.set_default_timeout(90000)

        result = self.check_input_text_correct('form[data_tag=start_registration] input', text)
        assert result == text, 'AuthPage: Подтянулась неверная почта'

        self.page.set_default_timeout(30000)

    def input_registration_code(self, code='111111'):
        """
        Ввод кода с почты при регистрации
        :param code:
        """
        self.OTP_CODE_INPUT.fill(code)

        with self.page.expect_response(
                f'**/s/auth/api/v1/auth/activation_confirm/') as response:
            self.OTP_SUBMIT.click()

        assert response.value.status == 200, (f'AuthPage: Ошибка активации почты '
                                              f'при регистарции {response.value.status}')

    def set_password(self, password):
        """
        Создание пароля при регистрации
        :param password: Пароль учетки
        """
        for i in self.SIGNUP_PASSWORD_INPUT.all():
            i.fill(password)

        with self.page.expect_response(f'**/s/auth/api/v1/flow/set_password/') as response:
            self.SIGNUP_PASSWORD_SUBMIT.click()

        assert response.value.status == 200, ('AuthPage: Ошибка при создании пароля '
                                              f'{response.value.status} {response.value.json()}')

    def fill_user_info(self, name, surname):
        """
        Ввод имени и фамилии при регистрации
        :param name: Имя юзера
        :param surname: Фамилия юзера
        """
        self.SIGNUP_USER_INFO_NAME.fill(name)
        self.SIGNUP_USER_INFO_SURNAME.fill(surname)
        with (self.page.expect_response(f"**/s/auth/api/v1/flow/set_names/") as response,
              self.page.expect_navigation(url=f"**/account/v2/main/**") as redirect):
            self.SIGNUP_USER_INFO_SUBMIT.click()

        assert response.value.status == 200, f"AuthPage: ФИО не назначено [Код {response.value.status}]"
        assert redirect.value.status == 200, f"AuthPage: Редирект не успешеый"
        assert redirect.value.request.header_value('cookie').find('csrftoken') != -1, ("AuthPage: Регистраци не успешна"
                                                                                       ", куки не пришли")

    #   ====================================== Обобщенные функции ======================================

    def email_auth(self, email, password):
        """
        Авторизация с через почту
        :param email: Почта
        :param password: Пароль
        :return:
        """
        self.navigate()

        self.input_email_or_phone(email)

        self.click_auth_email_continue_btn()

        self.input_password(password=password)

        with self.page.expect_response(f'**/s/auth/api/v1/auth/email/') as response:
            self.click_auth_password_continue_btn()

        assert response.value.status == 200, 'AuthPage: Ошибка при авторизации (этап пароль)'

        self.page.wait_for_url(f"**/account/v2/main/")

        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("load")
        self.page.wait_for_load_state("networkidle")

        self.page.keyboard.press('Escape')
