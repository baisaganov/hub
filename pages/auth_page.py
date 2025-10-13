import random

import playwright._impl._errors

from playwright.sync_api import Page
import logging

from commons.types import ServiceType, AdminFuncTypes, AdminAccountChangeType
from config.links import Links
from services.admin_api import AdminAPI
from base.base_page import BasePage
# from services.egov.sign_service import SignXml TODO: SignXml fix


# Авторизация и Регистрация на портале Astanahub
class AuthPage(BasePage):
    log = logging.getLogger(__name__)  # Подхватываем логгер

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.username_field = page.locator("div[x-show=\"step === 'login'\"] input[type='text']")
        self.password_field = page.locator("div[x-show=\"step === 'password'\"] input[name=password]")

        self.username_signup_field = page.locator("//html/body/div[2]/div[10]/div[1]/form/div/input")
        self.otp_code_field = page.locator("div[x-show=\"step === 'confirm_email_register'\"] "
                                           "form[data_tag='submitOTP'] input")
        self.new_password_field_1 = page.locator('form[data_tag="set_password"] input[name="new_password"]')
        self.new_password_field_2 = page.locator('form[data_tag="set_password"] input[name="confirm_password"]')
        self.continue_reg_password_btn = page.locator('form[data_tag=set_password] button[type=submit]')
        self.name_field = page.locator("input[name='first_name']")
        self.surname_field = page.locator("input[name='last_name']")
        self.profile_photo_skip = page.locator('div[x-show="step === \'set_photo\'"] button[type=submit]')



        self.auth_email_continue_btn = page.locator("div[x-show=\"step === 'login'\"] button[type='submit']")
        self.auth_password_continue_btn = page.locator("div[x-show=\"step === 'password'\"] button[type='submit']")
        self.continue_btn_signup = page.locator("form[data_tag='start_registration'] > button")
        self.join_btn = page.locator("div[x-show=\"step === 'login'\"] span.underline")
        self.send_code_btn = page.locator("div[x-show=\"step === 'confirm_email_register'\"] button")
        self.resend_code_btn = page.locator("div[x-show=\"step === 'confirm_email_register'\"] "
                                            "form > div > div > span.cursor-pointer")
        self.continue_user_info_btn = page.locator("form[data_tag=set_names] button[type=submit]")
        self.role_select_btn = page.locator('//html/body/div[2]/div[9]/div/div/div[1]')
        self.role_not_select_btn = page.locator('//html/body/div[2]/div[9]/div/div/div[2]')
        self.ecp_auth_btn = page.locator("div[x-show=\"step === 'login'\"] button").nth(1)

        # Photo Form
        self.set_photo_submit_btn = page.locator('form[data_tag="set_photo"] button[type="submit"]')
        self.set_photo = page.locator('label.photo')

        # Select Community Role
        self.comunity_form = page.locator('form[data_tag=set_community_role]')
        self.tag_list = self.comunity_form.locator('label')
        self.tag_continue_btn = self.comunity_form.locator('button[type=submit]')

        # Reg success
        self.success_form = page.locator("div[x-show=\"step === 'success'\"]")
        self.success_btn = self.success_form.locator('div.btn')

    def navigate(self):
        with self.page.expect_response(Links.LOGIN_PAGE) as resp:
            self.page.goto(Links.LOGIN_PAGE)

        assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                         msg="AuthPage: Страница не доступна")

    def input_email_or_phone(self, value):
        """
        Ввод почты или телефона при авторизации
        :param value: Email
        :return:
        """
        input_field = self.username_field
        input_field.click()
        input_field.fill(value)
        self.log.debug(f"LoginModal: Filled {value}")

    def input_password(self, password):
        """
        Ввод пароля при авторизации
        :param password:
        :return:
        """
        input_field = self.password_field
        input_field.click()
        input_field.fill(password)
        self.log.debug(f"LoginModal: Filled {password}")

    def click_auth_email_continue_btn(self):
        """
        Клик по кнопке продолжить при вводе почты Авторизация
        :return:
        """
        try:
            with self.page.expect_response(f"{Links.HOST}/s/auth/api/v1/auth/check/") as response_info:
                self.auth_email_continue_btn.click()
                self.log.debug(f"Клик по кнопке продолжить при вводе почты Авторизация")
            assert response_info.value.status == 200, (
                self.error_info(msg=f"LoginModal: Continue btn clicked error", status=response_info.value.status))
            return response_info
        except Exception as e:
            assert 1 == 0, self.error_info(msg='Continue btn error exception', status=400, exception=e)

    def click_auth_password_continue_btn(self):
        """
        Клик на продолжить при вводе пароля Авторизация
        :return:
        """
        try:
            with self.page.expect_response(f"{Links.HOST}/s/auth/api/v1/auth/email/") as response_info:
                self.auth_password_continue_btn.click()
            self.log.debug(f"LoginModal: Continue btn 2 clicked")

            assert response_info.value.status == 200, (
                self.error_info(msg=f"LoginModal: Continue btn 2 clicked error", status=response_info.value.status))

        except Exception as e:
            assert 1 == 0, self.error_info(msg='Continue btn 2 error exception', status=400, exception=e)

    def click_reg_join_btn(self):
        """
        Нажатие на кнопку "Присоединиться к Astanahub..."
        :return:
        """
        try:
            self.join_btn.click()
        except Exception as e:
            assert 1 == 0, self.error_info(msg=f"Нажатие на кнопку \"Присоединиться к Astanahub...\"",
                                           exception=e,
                                           status=400)

    def check_inputed_email(self):
        """
        Проверка введенной почты при регистарции
        :return:
        """
        try:
            # if self.continue_btn_signup.is_enabled()
            with self.page.expect_response(
                    f'{Links.HOST}/s/auth/api/v1/auth/email_registration/') as response:
                self.continue_btn_signup.click()

            assert response.value.status == 200, self.error_info(msg=f"Ошибка проверки почты, токен не получен",
                                                                 status=response.value.status)
            return response
        except Exception as e:
            assert 1 == 0, self.error_info(msg='Ошибка при нажатии Продолжить при регистрации (проверка почты)',
                                           status=400,
                                           exception=e)

    def input_registration_code(self, code):
        """
        Ввод кода с почты при регистрации
        :param code:
        :return:
        """
        try:
            self.otp_code_field.fill(code)

            with self.page.expect_response(
                    f'{Links.HOST}/s/auth/api/v1/auth/activation_confirm/') as response:
                self.send_code_btn.click()
                self.log.debug('Registration: Input code send')

            assert response.value.status == 200, 'Ошибка при отправке кода регистарции'

        except Exception as e:
            self.error_info(status=400, msg='Registration: Input code error', exception=e)

    def create_password(self, password):
        """
        Создание пароля при регистрации
        :param password:
        :return:
        """
        try:

            self.new_password_field_1.fill(password)
            self.new_password_field_2.fill(password)
            with self.page.expect_response(f'{Links.HOST}/s/auth/api/v1/flow/set_password/') as response:
                self.continue_reg_password_btn.click()
                self.log.debug(f'Registration: Password created')

            assert response.value.status == 200, self.error_info(status=response.value.status,
                                                                 msg='AuthPage: Пароль не создан')
        except Exception as e:
            self.error_info(status=400, msg='Registration: Create password error', exception=e)

    def input_user_info(self, name, surname):
        """
        Ввод имени и фамилии при регистрации
        :param name:
        :param surname:
        :return:
        """
        try:
            self.name_field.fill(name)
            self.surname_field.fill(surname)
            with self.page.expect_response(f"{Links.HOST}/s/auth/api/v1/flow/set_names/") as response:
                self.continue_user_info_btn.click()
                self.log.debug(f'Registration: Set name completed')

            assert response.value.status == 200, self.error_info(msg="AuthPage: ФИО не назначено",
                                                                 status=response.value.status)

            self.continue_user_info_btn.click()
        except Exception as e:
            self.error_info(status=400, msg='Registration: Set names error', exception=e)

    def choose_role(self, is_role_select=False):
        """

        :param is_role_select:
        :return:
        """
        try:
            with self.page.expect_response(f"{Links.HOST}/s/auth/api/v1/flow/set_completed/") as response:
                if is_role_select is True:
                    self.role_select_btn.click()
                else:
                    self.role_not_select_btn.click()

            assert response.value.status == 200, self.error_info(status=response.value.status,
                                                                 msg="Registration: Role choosed")

        except Exception as e:
            self.error_info(status=400,
                            msg=f"Registration: Select role error(is_role_select={is_role_select}",
                            exception=e)
        finally:
            self.page.goto(f"{Links.HOST}/ru/")
            user_id = self.page.locator('a.gamification-header').last.get_attribute('href').split('/')[-2]
            self.log.debug(user_id)
            admin = AdminAPI()
            admin.delete_user_by_id(user_id=user_id, service='auth')
            try:
                admin.delete_user_by_id(user_id=user_id, service='techhub')
            except:
                pass

    def auth_using_egov(self, iin, user_id):
        """
        Реализация авторизации с помощью ЭЦП
        :param iin: ИИН
        :param user_id: id юзера у которого меняем
        :return:
        """
        admin = AdminAPI()
        data = {'iin': iin}

        reserved_user_id = admin.get_user_id_by_(data.get('iin'))

        if reserved_user_id is None or reserved_user_id != user_id:
            admin.change_user(change_mode=AdminAccountChangeType.IIN,
                              data=data,
                              user_id=user_id,
                              functinonality=AdminFuncTypes.CHANGE)

        with self.page.expect_response(f'{Links.HOST}/s/auth/api/v1/auth/signature_xml/') as response:
            self.ecp_auth_btn.click()

        assert response.value.status == 200, self.error_info(msg=f'ЭЦП Авторизация: Клик по кнопке ЭЦП',
                                                             status=response.value.status)

        try:
            with self.page.expect_response(f'{Links.HOST}/s/auth/api/v1/auth/signature/') as response:
                # SignXml().sign_xml() TODO: SignXml fix
                pass

            assert response.value.status == 200, self.error_info(msg='ЭЦП Авторизация: Авторизация не удалась',
                                                                 status=response.value.status)
        except playwright._impl._errors.TimeoutError as e:
            assert None is not None, self.error_info(msg='ЭЦП Авторизация: Окно не найдено или неверные координаты',
                                                     status=400,
                                                     exception=e)

    def email_auth(self, email, password):
        with self.page.expect_response(f'{Links.HOST}/ru/s/auth/login/') as response:
            self.page.goto(f'{Links.HOST}/ru/s/auth/login/')

        assert response.value.status == 200, self.error_info(status=response.value.status,
                                                             msg='Auth: Ошибка при авторизации, страница не открылась')

        self.input_email_or_phone(value=email)
        response = self.click_auth_email_continue_btn()

        assert response is not None, self.error_info(msg='Auth: Пустой ответ при заполнении почты')
        assert response.value.status == 200, self.error_info(msg='Ошибка при авторизации через почту, этап ввод почты',
                                                             status=response.value.status)
        assert response.value.json()['user_exists'] is True, self.error_info(status=response.value.status,
                                                                             msg="Ошибка при авторизации, Юзер "
                                                                                 "отсутвует")
        self.input_password(password=password)
        self.click_auth_password_continue_btn()

    def set_photo_form(self):

        with self.page.expect_response() as response:
            pass

    def complete_registration(self):
        with self.page.expect_response(f'{Links.HOST}/account/v2/main/') as response:
            self.success_btn.click()

        assert response.value.status == 200, self.error_info(msg='Ошибка при завершении регистрации',
                                                             status=response.value.status)

    def skip_profile_photo(self):
        with self.page.expect_response(f'https://{Links.HOST}/s/auth/api/v1/flow/set_photo/') as response:
            self.profile_photo_skip.click()

        assert response.value.status == 200, self.error_info(msg='Ошибка пропуска шага',
                                                             status=response.value.status)

    def select_tag(self):
        tag_count = self.tag_list.count()
        # Select random tag
        self.tag_list.nth(random.randint(0, tag_count)).click()

        with (self.page.expect_response(f'https://{Links.HOST}/s/auth/api/v1/flow/set_community_role/') as set_response,
              self.page.expect_response(f'https://{Links.HOST}/account/api/user/update_profile/') as profile_response):
            self.tag_continue_btn.click()

        assert set_response.value.status == 200, self.error_info(msg='Тэг не установился',
                                                                 status=set_response.value.status)

        assert profile_response.value.status == 200, self.error_info(msg='Профиль не обновился',
                                                                     status=profile_response.value.status)
