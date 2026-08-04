import pytest
import allure

from config import config
from testdata.factories import fake_invalid_email, fake_password

pytestmark = [pytest.mark.api]


@allure.suite("Authorization")
@allure.label("owner", "aliwka")
class TestAuthAPI:
    @allure.title("Valid authorization")
    @pytest.mark.asyncio
    async def test_valid_authorization(self, auth_client):
        with allure.step("Логин с валидными кредами"):
            login = await auth_client.login(
                email=config.app.test_user_email,
                password=config.app.test_user_password,
            )

        with allure.step("Проверка данных юзера в ответе"):
            assert login.user.email == config.app.test_user_email
            assert login.user.email_verified is True
            assert login.user.blocked is False

    @allure.title("Authorization with invalid email")
    @pytest.mark.asyncio
    async def test_authorization_with_invalid_email(self, auth_client):
        with allure.step("Логин с невалидным email"):
            errors = await auth_client.login_expect_error(
                email=fake_invalid_email(),
                password=fake_password(),
                expected_status=400,
            )

        with allure.step("Проверка ошибки валидации по полю email"):
            assert "email" in errors, f"Ожидалась ошибка по email, пришло: {errors.fields}"
            assert errors["email"], "Список ошибок по email пуст"
