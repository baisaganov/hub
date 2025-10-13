import random
from os import getenv
from dotenv import load_dotenv, find_dotenv
from config.links import Links

import allure
import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError



@allure.suite("Astanahub - Авторизация")
@allure.sub_suite("Smoke тесты")
class TestAuth:
    load_dotenv(find_dotenv())
    USERNAME = getenv("AUTH_LOGIN")
    PASSWORD = getenv("AUTH_PASSWORD")

    @allure.title("Проверка авторизации с валидными данными")
    @allure.description("Тест проверяет, что пользователь может войти с правильными учетными данными.")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize(
        "email, password",
        [
            (USERNAME, PASSWORD)  # Валидный
        ],
        ids=["✅ Валидный логин"]
    )
    def test_email_login_valid(self, page, auth_page, email, password):
        with allure.step("Переход на страницу авторизации"):
            try:
                response = page.goto(Links.LOGIN_PAGE)
                assert response.status == 200, f"Ошибка, url не действительный: {response.status}"
            except PlaywrightTimeoutError as e:
                assert False, f"Не удалось загрузить страницу: {e}"

        with allure.step("Ввод почты"):
            auth_page.input_email_or_phone(value=email)

        with allure.step("Клик по кнопке продолжить"):
            response = auth_page.click_auth_email_continue_btn()

        assert response is not None, "Ошибка при входе, пустой ответ"
        assert response.value.status == 200, f"Ошибка, неверный статус код: {response.value.status}"
        assert response.value.json()['user_exists'] is True, "Юзер отсутвует"

        with allure.step("Ввод пароля"):
            auth_page.input_password(password=password)

        with allure.step("Клик по кнопке продолжить"):
            auth_page.click_auth_password_continue_btn()

    @allure.title("Проверка авторизации с несуществующей почтой")
    @allure.description("Тест проверяет, что если нет почты в базе, она предложит пройти регистрацию")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "email, password, expected_status",
        [
            ("123alisher123@alisher.alisher", "Adfsaf4213!", 200),
            (f"wrong@example{random.randint(1, 1000)}.com", "wrongpass", 200),

        ],
        ids=["✅ Невалидный логин", "✅ Невалидный логин 2"]
    )
    def test_invite_for_reg(self, page, auth_page, email, password, expected_status):
        with allure.step("Переход на страницу авторизации"):
            try:
                response = page.goto(Links.LOGIN_PAGE)
                assert response.status == 200, f"Ошибка, url не действительный: {response.status}"
            except PlaywrightTimeoutError as e:
                assert False, f"Не удалось загрузить страницу: {e}"

        with allure.step("Ввод несуществующей почты"):
            auth_page.input_email_or_phone(email)
            response = auth_page.click_auth_email_continue_btn()

            assert response.value.status == expected_status, f"Ошибка проверки статуса {response.value.status}"
            assert response.value.json()['user_exists'] is not True, "Почта существует, хоть и не должна"

    @allure.title("Авторизация с помощью ЭЦП")
    @allure.description("Проверяем дает ли система авторизоваться с помощью ЭЦП")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "iin, user_id",
        [
            ("990315351258", 59919)

        ],
        ids=["✅ Валидный логин"]
    )
    @pytest.mark.skip("Проверка ЭЦП отключена")
    def test_ecp_auth(self, page, auth_page, iin, user_id):
        with allure.step("Переход на страницу авторизации"):
            page.goto(Links.LOGIN_PAGE)


        with allure.step("Авторизация ЭЦП"):
            auth_page.auth_using_egov(iin, user_id)

