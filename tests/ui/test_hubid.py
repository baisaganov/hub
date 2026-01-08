import allure
import pytest

from playwright.sync_api import Page
from config import config


@allure.feature('HUB ID')
class TestHubID:
    @allure.story('User Registration')
    @allure.title('Успешная регистрация с валидными кредами email')
    @allure.description('Тест проверяет что юзер может успешно зарегестрироваться через почту')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke")
    @pytest.mark.flaky(reruns=1, reruns_delay=30)
    @pytest.mark.parametrize('env',
                             ['dev'])
    def test_email_registration_from_auth(self, auth_page, main_page, registration_user_creds, env):
        config.app.subdomain = env
        config.app.update_app_url()

        with allure.step('Переход на главную страницу'):
            main_page.navigate()

        with allure.step('Клик по кнопке "Войти"'):
            main_page.login_click()

        with allure.step('Ввод email которого нет в базе'):
            auth_page.input_email_or_phone(registration_user_creds['email'])
            auth_page.click_auth_email_continue_btn(is_auth=False)

        with allure.step('Клик по переходу к регистрации'):
            auth_page.click_registration_span()

        with allure.step('Политика конфиденциальности'):
            # auth_page.privacy_continue_btn_click(False)  # Ожидаем ошибку
            auth_page.privacy_continue_btn_click(True)  # Ожидаем что уведомление исчезло

        with allure.step('Проверяем что email подтянулся верный'):
            auth_page.check_email_input_text(registration_user_creds['email'])

        with allure.step('Нажимает на кнопку продолжить'):
            auth_page.click_reg_continue_btn(is_auth_step=False)

        with allure.step('Ввод кода активации'):
            auth_page.input_registration_code()

        with allure.step('Создание пароля для учетки'):
            auth_page.set_password(registration_user_creds['password'])

        with allure.step('Заполнение информации о юзере'):
            auth_page.fill_user_info(
                registration_user_creds['name'],
                registration_user_creds['surname']
            )

        with allure.step('Сохраняем куки для последующего использования'):
            auth_page.save_cookies()

    @allure.story('User Registration')
    @allure.title('Успешная регистрация с валидными кредами phone')
    @allure.description('Тест проверяет что юзер может успешно зарегестрироваться через номер телефона')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.tag("smoke")
    # @pytest.mark.flaky(reruns=1, reruns_delay=30)
    @pytest.mark.parametrize('env',
                             ['dev'])
    def test_phone_registration_from_auth(self, auth_page, main_page, registration_user_creds, env):
        config.app.subdomain = env
        config.app.update_app_url()

        with allure.step('Переход на главную страницу'):
            main_page.navigate()

        with allure.step('Клик по кнопке "Войти"'):
            main_page.login_click()

        with allure.step('Ввод email которого нет в базе'):
            auth_page.input_email_or_phone(registration_user_creds['phone'])
            auth_page.click_auth_email_continue_btn(is_auth=False)

        with allure.step('Клик по переходу к регистрации'):
            auth_page.click_registration_span()

        with allure.step('Политика конфиденциальности'):
            # auth_page.privacy_continue_btn_click(False)  # Ожидаем ошибку
            auth_page.privacy_continue_btn_click(True)  # Ожидаем что уведомление исчезло

        with allure.step('Проверяем что телефон подтянулся верный'):
            auth_page.check_email_input_text(registration_user_creds['phone'])

        with allure.step('Нажимает на кнопку продолжить'):
            auth_page.click_reg_continue_btn(is_auth_step=False)

        with allure.step('Ввод кода активации'):
            auth_page.input_registration_code()

        with allure.step('Создание пароля для учетки'):
            auth_page.set_password(registration_user_creds['password'])

        with allure.step('Заполнение информации о юзере'):
            auth_page.fill_user_info(
                registration_user_creds['name'],
                registration_user_creds['surname']
            )

        with allure.step('Сохраняем куки для последующего использования'):
            auth_page.save_cookies()
