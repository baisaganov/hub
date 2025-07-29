from pages.feed_page import FeedPage
from pages.hub_Id.auth import AuthPage
import allure
import pytest


@allure.suite("Astanahub - Авторизация")
@allure.sub_suite("Smoke тесты")
class TestAuth:
    @allure.title("Проверка авторизации с валидными данными")
    @allure.description("Тест проверяет, что пользователь может войти с правильными учетными данными.")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize(
        "email, password, expected_status",
        [
            ("baisaganov99@gmail.com", "Pass1234!", 200)  # Валидный
        ],
        ids=["✅ Валидный логин"]
    )
    def test_email_login_valid(self, page, email, password, expected_status):
        feed = FeedPage(page)

        with allure.step("Переход на главную страницу портала"):
            feed.navigate()

        with allure.step("Клик по кнопке авторизации"):
            feed.click_on_login_page()

        login_page = AuthPage(page)

        with allure.step("Ввод почты"):
            login_page.input_email_or_phone(value=email)

        with allure.step("Клик по кнопке продолжить"):
            response = login_page.click_auth_continue_btn()

        assert response is not None, "Ошибка при входе, пустой ответ"
        assert response.value.status == expected_status, f"Ошибка, неверный статус код: {response.value.status}"
        assert response.value.json()['user_exists'] is True, "Юзер отсутвует"

        with allure.step("Ввод пароля"):
            login_page.input_password(password=password)

        with allure.step("Клик по кнопке продолжить"):
            response = login_page.click_auth_continue_btn_2()

        assert response.value.status == 200, "Ошибка при входе с валидными данными"

    @allure.title("Проверка авторизации с несуществующей почтой")
    @allure.description("Тест проверяет, что если нет почты в базе, она предложит пройти регистрацию")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "email, password, expected_status",
        [
            ("123alisher123@alisher.alisher", "Pass1234!", 200),  # Невалидный
            ("wrong@example.com", "wrongpass", 200),  # Невалидный

        ],
        ids=["✅ Невалидный логин", "✅ Невалидный логин 2"]
    )
    def test_invite_for_reg(self, page, email, password, expected_status):
        feed = FeedPage(page)

        with allure.step("Переход на главную страницу портала"):
            feed.navigate()

        with allure.step("Клик по кнопке авторизации"):
            feed.click_on_login_page()

        login_page = AuthPage(page)

        with allure.step("Ввод несуществующей почты"):
            login_page.input_email_or_phone(email)
            response = login_page.click_auth_continue_btn()

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
    def test_ecp_auth(self, page, iin, user_id):
        feed = FeedPage(page)
        with allure.step("Переход на главную страницу портала"):
            feed.navigate()

        with allure.step("Клик по кнопке авторизации"):
            feed.click_on_login_page()

        login_page = AuthPage(page)

        with allure.step("Авторизация ЭЦП"):
            response = login_page.auth_using_egov(iin, user_id)

        assert response is not None, 'Ошибка при подписании ЭЦП, окно возможно не найдено'
        assert response.value.status == 200, 'Автоизация не удалась'
