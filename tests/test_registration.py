import allure
import pytest

from config.links import Links
from services.admin_api import AdminAPI


@allure.suite("Astanahub - Регистрация")
class TestRegistration:

    @allure.title("Проверка регистрации с валидными данными")
    @allure.description("Тест проверяет, что пользователь может зарегестрироваться с правильными учетными данными.")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize("email, password, status_code",
                             [
                                 ("admin@admin.hub", "Pass1234!", 200)
                             ],
                             ids=["Валидная регистрация"])
    def test_valid_reg_email(self, page, auth_page, email, password, status_code):
        admin = AdminAPI()
        with allure.step("Проверяем есть ли аккаунт, если есть удаляем"):
            account_id = admin.get_user_id_by_(email)
            if account_id is not None:
                admin.delete_user_by_id(user_id=account_id)

        with allure.step("Переход на страницу авторизации"):
            page.goto(Links.LOGIN_PAGE)

        with allure.step("Ввод почты"):
            auth_page.input_email_or_phone(value=email)
            response = auth_page.click_auth_continue_btn()

        assert (response is not None and
                response.value.status == status_code and
                response.value.json()['user_exists'] is False and
                response.value.json()['method'] == "email"), (f'Ошибка при вводе почты '
                                                              f'Status : {response.value.status}'
                                                              f'method: {response.value.json()["method"]},'
                                                              f'Пользователь существует: '
                                                              f'{response.value.json()["user_exists"]}')

        with allure.step("Переход к форме регистрации"):
            auth_page.click_reg_join_btn()

        with allure.step("Проверка почты"):
            activation = auth_page.check_inputed_email()
            assert activation.value.status == status_code, "Ошибка при проверке введенной почты при регистарции"

        with allure.step("Ввод кода"):
            code = admin.get_code(activation.value.json()['activation'])
            assert code is not None, "Код регистрации не получен"
            response = auth_page.input_registration_code(code)

        assert response.value.status == 200, f"Неверный статус запроса: {response.value.status}"

        with allure.step("Ввод пароля с подтверждением"):
            auth_page.create_password(password=password)

        with allure.step("Ввод информации о пользователе (ФИО)"):
            auth_page.input_user_info(name="Auto", surname="Test")

        with allure.step("Выбор роли"):
            auth_page.choose_role(is_role_select=False)
