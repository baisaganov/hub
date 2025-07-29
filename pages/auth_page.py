import logging

import playwright._impl._errors

from playwright.sync_api import Page
import logging as log


from commons.types import ServiceType, AdminFuncTypes, AdminAccountChangeType
from services.admin_api import AdminAPI
from pages.base_page import BasePage
from services.egov.sign_service import SignXml


# Авторизация и Регистрация на портале Astanahub
class AuthPage(BasePage):
    log = logging.getLogger(__name__)  # Подхватываем логгер

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.username_field = page.locator("//html/body/div[2]/div[1]/div[1]/form/div/input")
        self.password_field = page.locator("input[name=password]")
        self.username_signup_field = page.locator("//html/body/div[2]/div[10]/div[1]/form/div/input")
        self.otp_code_field = page.locator("//html/body/div[2]/div[4]/div/form/div/input")
        self.new_password_field_1 = page.locator('//html/body/div[2]/div[3]/div/form/div/input[1]')
        self.new_password_field_2 = page.locator('//html/body/div[2]/div[3]/div/form/div/input[2]')
        self.name_field = page.locator("//html/body/div[2]/div[8]/div/form/div[1]/input")
        self.surname_field = page.locator("//html/body/div[2]/div[8]/div/form/div[2]/input")

        self.continue_button = page.locator("//html/body/div[2]/div[1]/div[1]/form/button")
        self.continue_button_2 = page.locator("//html/body/div[2]/div[2]/div/form/button")
        self.continue_btn_signup = page.locator("//html/body/div[2]/div[10]/div[1]/form/button")
        self.join_btn = page.locator("//html/body/div[2]/div[1]/div[1]/div[1]/div/div/p[2]/span")
        self.send_code_btn = page.locator("//html/body/div[2]/div[4]/div/form/button")
        self.resend_code_btn = page.locator("//html/body/div[2]/div[4]/div/form/div/div/span[2]")
        self.continue_reg_password_btn = page.locator("//html/body/div[2]/div[3]/div/form/button")
        self.continue_user_info_btn = page.locator("//html/body/div[2]/div[8]/div/form/button")
        self.role_select_btn = page.locator('//html/body/div[2]/div[9]/div/div/div[1]')
        self.role_not_select_btn = page.locator('//html/body/div[2]/div[9]/div/div/div[2]')
        self.ecp_auth_btn = page.locator('//html/body/div[2]/div[1]/div[1]/div[3]/button')

    def input_email_or_phone(self, value):
        """
        Ввод почты или телефона при авторизации
        :param value:
        :return:
        """
        try:
            input_field = self.username_field
            input_field.click()
            input_field.fill(value)
            log.info(f"LoginModal: Filled {value}")
        except Exception as e:
            return self.error_response(error_text=f"Ошибка при вводе почты {e}",
                                       service=ServiceType.HUBID,
                                       status=400)

    def input_password(self, password):
        """
        Ввод пароля при авторизации
        :param password:
        :return:
        """
        try:
            input_field = self.password_field
            input_field.click()
            input_field.fill(password)
            log.info(f"LoginModal: Filled {password}")
            return {'response': 200, 'msg': 'Пароль введен'}
        except Exception as e:
            return self.error_response(error_text=f"Input password error {e}",
                                       service=ServiceType.HUBID,
                                       status=400)

    def click_auth_continue_btn(self):
        """
        Клик на продолжить при вводе почты Авторизация
        :return:
        """
        try:
            with self.page.expect_response("https://dev.astanahub.com/s/auth/api/v1/auth/check/") as response_info:
                self.continue_button.click()
            log.info(f"LoginModal: Continue btn clicked")
            return response_info
        except Exception as e:
            return self.error_response(error_text=f"Continue btn error {e}",
                                       service=ServiceType.HUBID,
                                       status=400)

    def click_auth_continue_btn_2(self):
        """
        Клик на продолжить при вводе пароля Авторизация
        :return:
        """
        try:
            with self.page.expect_response("https://dev.astanahub.com/s/auth/api/v1/auth/email/") as response_info:
                self.continue_button_2.click()
            log.info(f"LoginModal: Continue btn 2 clicked")
            return response_info
        except Exception as e:
            return self.error_response(error_text=f"Continue btn 2 error {e}",
                                       service=ServiceType.HUBID,
                                       status=400)

    def click_reg_join_btn(self):
        """
        Нажатие на кнопку "Приесоединиться к Astanahub..."
        :return:
        """
        try:
            self.join_btn.click()
        except Exception as e:
            return self.error_response(error_text=f"Join span click error {e}",
                                       service=ServiceType.HUBID,
                                       status=400)

    def check_inputed_email(self):
        """
        Проверка введенно почты при регистарции
        :return:
        """
        try:
            # if self.continue_btn_signup.is_enabled()
            with self.page.expect_response(
                    'https://dev.astanahub.com/s/auth/api/v1/auth/email_registration/') as response:
                self.continue_btn_signup.click()
            if response.value.status == 200:
                return response
            else:
                self.__take_screenshot("Ошибка ответа при нажатии Продолжить при регистрации (проверка почты)")
                raise
        except Exception as e:
            log.error(f"Registration: Check_inputed_email error {e}")
            self.__take_screenshot("Ошибка при нажатии Продолжить при регистрации (проверка почты)")
            raise e

    def input_registration_code(self, code, status_code):
        """
        Ввод кода с почты при регистрации
        :param code:
        :param status_code:
        :return:
        """
        try:
            self.otp_code_field.fill(code)

            with self.page.expect_response(
                    'https://dev.astanahub.com/s/auth/api/v1/auth/activation_confirm/') as response:
                self.send_code_btn.click()
            if response.value.status == status_code:  # Ок 200 Неверный код 400
                log.info(f'Registration: Code accept')
            else:
                raise
            return response
        except Exception as e:
            log.error(f"Registration: Input code error {e}")
            self.__take_screenshot("Registration: Input code error")

            raise

    def create_password(self, password):
        """
        Создание пароля при регистрации
        :param password:
        :return:
        """
        try:

            self.new_password_field_1.fill(password)
            self.new_password_field_2.fill(password)
            with self.page.expect_response('https://dev.astanahub.com/s/auth/api/v1/flow/set_password/') as response:
                self.continue_reg_password_btn.click()
            if response.value.status != 200:
                raise
            log.info(f'Registration: Password created')
            return response
        except Exception as e:
            log.error(f"Registration: Create password error {e}")
            raise e

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
            with self.page.expect_response("https://dev.astanahub.com/s/auth/api/v1/flow/set_names/") as response:
                self.continue_user_info_btn.click()
            log.info(f'Registration: Set name completed')
            return response
        except Exception as e:
            self.__take_screenshot("Ошибка при отправке ФИО")
            log.error(f"Registration: Set names error: {e}")
            raise e

    def choose_role(self, is_role_select=False):
        """

        :param is_role_select:
        :return:
        """
        try:
            with self.page.expect_response("https://dev.astanahub.com/s/auth/api/v1/flow/set_completed/") as response:
                if is_role_select is True:
                    self.role_select_btn.click()
                else:
                    self.role_not_select_btn.click()
            if response.value.status == 200:
                log.info(f'Registration: Role choosed')
                return response
            raise
        except Exception as e:
            self.__take_screenshot(f"Registration: Select role error(is_role_select={is_role_select}")
            log.error(f"Registration: Select role error(is_role_select={is_role_select}: {e}")
            raise e
        finally:
            self.page.goto("https://dev.astanahub.com/ru/")
            user_id = self.page.locator('a.gamification-header').last.get_attribute('href').split('/')[-2]
            logging.info(user_id)
            admin = AdminAPI()
            admin.delete_user_by_id(user_id=user_id, service='auth')
            admin.delete_user_by_id(user_id=user_id, service='techhub')

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

        with self.page.expect_response('https://dev.astanahub.com/s/auth/api/v1/auth/signature_xml/') as response:
            self.ecp_auth_btn.click()

        if response.value.status not in [200]:
            log.error(f'ЭЦП Авторизация: Не удалось получить timestamp {response.value.status}')
            return response

        try:
            with self.page.expect_response('https://dev.astanahub.com/s/auth/api/v1/auth/signature/') as response:
                SignXml().sign_xml()
        except playwright._impl._errors.TimeoutError:
            log.error('ЭЦП Авторизация: Окно не найдено или неверные координаты')
            return None

        if response.value.status == 200:
            log.info(f'ЭЦП Авторизация: Успешно авторизованы')
        else:
            log.error(f'ЭЦП Авторизация: Не удалась авторизация. Status: {response.value.status}')

        return response

    def email_auth(self, email, password):
        with self.page.expect_response('https://dev.astanahub.com/ru/s/auth/login/') as response:
            self.page.goto('https://dev.astanahub.com/ru/s/auth/login/')
        if response.value.status != 200:
            return self.error_response(error_text='Ошибка при авторизации, страница не открылась',
                                       status=response.value.status,
                                       service=ServiceType.HUBID)

        self.input_email_or_phone(value=email)
        response = self.click_auth_continue_btn()

        if response is None:
            return self.error_response(error_text='Пустой ответ при заполнении почты',
                                       status=None,
                                       service=ServiceType.HUBID)
        elif response.value.status != 200:
            return self.error_response(error_text='Ошибка при авторизации через почту, этап ввод почты',
                                       status=response.value.status,
                                       service=ServiceType.HUBID)
        elif response.value.json()['user_exists'] is False:
            return self.error_response(error_text='Ошибка при авторизации, Юзер отсутвует',
                                       status=response.value.status,
                                       service=ServiceType.HUBID)

        response = self.input_password(password=password)
        if response['response'] != 200:
            return self.error_response(error_text='Ошибка при вводе пароля',
                                       status=response.value.status,
                                       service=ServiceType.HUBID)
        response = self.click_auth_continue_btn_2()

        if response is None:
            return self.error_response(error_text='Пустой ответ при заполнении пароля',
                                       status=None,
                                       service=ServiceType.HUBID)
        elif response.value.status != 200:
            return self.error_response(error_text='Ошибка при входе с валидными данными',
                                       status=response.value.status,
                                       service=ServiceType.HUBID)

        return {"response": 200, 'msg': 'Успешно авторизован'}
