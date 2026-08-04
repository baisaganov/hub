import allure
import pytest

from playwright.sync_api import expect
from config import config


@allure.suite("HUB ID")
@allure.label("level", "UI")
@pytest.mark.hubid
@pytest.mark.ui
@allure.label("owner", "aliwka")
class TestHubID:
    ENV = config.app.env

    @allure.title("Успешная регистрация с валидными кредами email")
    @pytest.mark.critical
    @pytest.mark.skip
    def test_email_registration_from_auth(
        self, auth_page, main_page, registration_user_creds
    ):

        with allure.step(title="Переход на главную страницу"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step('Клик по кнопке "Войти"'):
            login_resp = main_page.login_click()
            assert login_resp.status in (200, 302), (
                f"Страница логина не доступна: {login_resp.status}"
            )
            cookies = login_resp.request.header_value("cookie")
            assert cookies is None or "csrftoken" not in cookies, (
                "Юзер уже авторизован"
            )

        with allure.step("Клик по кнопке 'Перейти в HubID', если есть"):
            auth_page.welcome_hubid()

        with allure.step("Ввод email которого нет в базе"):
            auth_page.input_email_or_phone(registration_user_creds["email"])
            check_resp = auth_page.click_auth_email_continue_btn()
            assert check_resp.status == 200, "Ошибка при клике продолжить"
            assert check_resp.json()["user_exists"] is False, (
                "Юзер с такой почтой уже существует"
            )

        with allure.step("Клик по переходу к регистрации"):
            auth_page.click_registration_span()

        with allure.step("Политика конфиденциальности"):
            privacy_resp = auth_page.accept_privacy_policy()
            assert privacy_resp.status == 200, (
                f"Политика конф-ти вернула {privacy_resp.status}"
            )
            expect(auth_page.PRIVACY_READ).to_be_hidden()

        with allure.step("Проверяем что email подтянулся верный"):
            assert (
                auth_page.get_email_input_text() == registration_user_creds["email"]
            ), "Подтянулась неверная почта"

        with allure.step("Нажимает на кнопку продолжить"):
            reg_resp = auth_page.click_reg_continue_btn(is_auth_step=False)
            assert reg_resp.status == 200, "Ошибка при клике продолжить"

        with allure.step("Ввод кода активации"):
            otp_resp = auth_page.input_registration_code()
            assert otp_resp.status == 200, (
                f"Ошибка активации почты при регистрации: {otp_resp.status}"
            )

        with allure.step("Создание пароля для учетки"):
            password_resp = auth_page.set_password(registration_user_creds["password"])
            assert password_resp.status == 200, (
                f"Ошибка при создании пароля: {password_resp.status}"
            )

        with allure.step("Заполнение информации о юзере"):
            names_resp, redirect_resp = auth_page.fill_user_info(
                registration_user_creds["name"], registration_user_creds["surname"]
            )
            assert names_resp.status == 200, (
                f"ФИО не назначено [Код {names_resp.status}]"
            )
            assert redirect_resp.status == 200, "Редирект не успешный"

        if self.ENV == "qa":
            with allure.step("Прикрепление фото профиля"):
                photo_resps = auth_page.upload_profile_photo()
                assert photo_resps["attach"].status in (200, 201), (
                    "Фото профиля не прикреплено"
                )
                assert photo_resps["file"].status in (200, 201), (
                    "Фото профиля не загружено"
                )
                assert photo_resps["update"].status in (200, 201), "Профиль не обновлен"
                assert photo_resps["set"].status in (200, 201), "Фото не установлено"

            with allure.step("Выбор роли ()"):
                expect(auth_page.ROLES_LIST).to_have_count(4)
                auth_page.select_role()

        with allure.step("Сохраняем контекст для последующего использования"):
            auth_page.save_context(self.ENV)

    @allure.title("Успешная регистрация с валидными кредами phone")
    @pytest.mark.critical
    @pytest.mark.flaky(reruns=1, reruns_delay=15)
    @pytest.mark.skip
    def test_phone_registration_from_auth(
        self, auth_page, main_page, registration_user_creds
    ):

        with allure.step("Переход на главную страницу"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step('Клик по кнопке "Войти"'):
            login_resp = main_page.login_click()
            assert login_resp.status in (200, 302), (
                f"Страница логина не доступна: {login_resp.status}"
            )
            cookies = login_resp.request.header_value("cookie")
            assert cookies is None or "csrftoken" not in cookies, (
                "Юзер уже авторизован"
            )

        with allure.step("Клик по кнопке 'Перейти в HubID', если есть"):
            auth_page.welcome_hubid()

        with allure.step("Ввод phone которого нет в базе"):
            auth_page.input_email_or_phone(registration_user_creds["phone"])
            check_resp = auth_page.click_auth_email_continue_btn()
            assert check_resp.status == 200, "Ошибка при клике продолжить"
            assert check_resp.json()["user_exists"] is False, (
                "Юзер с таким телефоном уже существует"
            )

        with allure.step("Клик по переходу к регистрации"):
            auth_page.click_registration_span()

        with allure.step("Политика конфиденциальности"):
            privacy_resp = auth_page.accept_privacy_policy()
            assert privacy_resp.status == 200, (
                f"Политика конф-ти вернула {privacy_resp.status}"
            )
            expect(auth_page.PRIVACY_READ).to_be_hidden()

        with allure.step("Проверяем что телефон подтянулся верный"):
            assert (
                auth_page.get_email_input_text() == registration_user_creds["phone"]
            ), "Подтянулся неверный телефон"

        with allure.step("Нажимает на кнопку продолжить"):
            reg_resp = auth_page.click_reg_continue_btn(is_auth_step=False)
            assert reg_resp.status == 200, "Ошибка при клике продолжить"

        with allure.step("Ввод кода активации"):
            otp_resp = auth_page.input_registration_code()
            assert otp_resp.status == 200, (
                f"Ошибка активации почты при регистрации: {otp_resp.status}"
            )

        with allure.step("Создание пароля для учетки"):
            password_resp = auth_page.set_password(registration_user_creds["password"])
            assert password_resp.status == 200, (
                f"Ошибка при создании пароля: {password_resp.status}"
            )

        with allure.step("Заполнение информации о юзере"):
            names_resp, redirect_resp = auth_page.fill_user_info(
                registration_user_creds["name"], registration_user_creds["surname"]
            )
            assert names_resp.status == 200, (
                f"ФИО не назначено [Код {names_resp.status}]"
            )
            assert redirect_resp.status == 200, "Редирект не успешный"

    @allure.title("Авторизация с помощью email")
    @pytest.mark.critical
    @allure.id("2")
    @allure.label("owner", "aliwka")
    def test_email_auth(self, base_user_creds, auth_page):

        with allure.step("Переход к HubID"):
            login_page_resp = auth_page.navigate()
            assert login_page_resp.status == 200, (
                f"Страница логина не доступна: {login_page_resp.status}"
            )

        with allure.step("Ввод почты"):
            auth_page.input_email_or_phone(base_user_creds["email"])

        with allure.step("Клик по кнопке продолжить (почта)"):
            check_resp = auth_page.click_auth_email_continue_btn()
            assert check_resp.status == 200, "Ошибка при клике продолжить"
            assert check_resp.json()["user_exists"] is True, (
                "Ошибка при авторизации, юзер отсутствует"
            )

        with allure.step("Ввод пароля"):
            auth_page.input_password(password=base_user_creds["password"])

        with allure.step("Клик по кнопке продолжить (пароль)"):
            auth_resp = auth_page.click_auth_password_continue_btn()
            assert auth_resp.status == 200, (
                "AuthPage: Ошибка при авторизации (этап пароль)"
            )

        with allure.step("Ожидание завершения загрузки страницы и сохранение куки"):
            auth_page.page.wait_for_url(
                "**/account/v2/main/", wait_until="domcontentloaded"
            )
            auth_page.page.keyboard.press("Escape")
            auth_page.save_context()

    def phone_auth(self, base_user_creds):
        pass
