import allure
import pytest

from playwright.sync_api import Page
from config import config


@allure.suite('HUB ID')
@pytest.mark.hubid
@pytest.mark.order(1)
class TestHubID:
    @allure.title('Успешная регистрация с валидными кредами email')
    @pytest.mark.critical
    # @pytest.mark.flaky(reruns=1, reruns_delay=10)
    @pytest.mark.parametrize('env',
                             ['qa', 'dev'])
    @pytest.mark.skip
    def test_email_registration_from_auth(self, auth_page, main_page, registration_user_creds, env):
        config.app.subdomain = env
        config.app.update_app_url()

        with allure.step('Переход на главную страницу'):
            main_page.navigate()

        with allure.step('Клик по кнопке "Войти"'):
            main_page.login_click()

        with allure.step("Клик по кнопке 'Перейти в HubID', если есть"):
            auth_page.welcome_hubid()

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

        if env == 'qa':
            with allure.step('Прикрепление фото профиля'):
                auth_page.upload_profile_photo()

            with allure.step('Выбор роли ()'):
                auth_page.select_role()

        with allure.step('Сохраняем контекст для последующего использования'):
            auth_page.save_context(env)

    @allure.title('Успешная регистрация с валидными кредами phone')
    @pytest.mark.critical
    @pytest.mark.flaky(reruns=1, reruns_delay=15)
    @pytest.mark.parametrize('env', ['dev', 'qa'])
    @pytest.mark.skip
    def test_phone_registration_from_auth(self, auth_page, main_page, registration_user_creds, env):
        config.app.subdomain = env
        config.app.update_app_url()

        with allure.step('Переход на главную страницу'):
            main_page.navigate()

        with allure.step('Клик по кнопке "Войти"'):
            main_page.login_click()

        with allure.step("Клик по кнопке 'Перейти в HubID', если есть"):
            auth_page.welcome_hubid()

        with allure.step('Ввод phone которого нет в базе'):
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

    @allure.title('Авторизация с помощью почты')
    @allure.label("level", "UI")
    @pytest.mark.critical
    @pytest.mark.parametrize('env', ['qa', ])
    def test_email_auth(self, base_user_creds, auth_page, env):
        config.app.subdomain = env
        config.app.update_app_url()

        with allure.step('Переход к HubID'):
            auth_page.navigate()

        with allure.step('Ввод почты'):
            auth_page.input_email_or_phone(base_user_creds['email'])

        with allure.step('Клик по кнопке продолжить (почта)'):
            auth_page.click_auth_email_continue_btn()

        with allure.step('Ввод пароля'):
            auth_page.input_password(password=base_user_creds['password'])

        with allure.step('Клик по кнопке продолжить (пароль)'):
            with auth_page.page.expect_response(f'**/s/auth/api/v1/auth/email/') as response:
                auth_page.click_auth_password_continue_btn()

            assert response.value.status == 200, 'AuthPage: Ошибка при авторизации (этап пароль)'

        with allure.step('Ожидание завершения загрузки страницы и сохранение куки'):
            auth_page.page.wait_for_url(f"**/account/v2/main/", wait_until='domcontentloaded')
            auth_page.page.keyboard.press('Escape')
            auth_page.save_context(env)

    def phone_auth(self, env, base_user_creds):
        pass
