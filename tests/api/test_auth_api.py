import pytest
import allure
from faker import Faker
from config import config

pytestmark = [pytest.mark.api]


@allure.suite("Authorization")
@allure.label("owner", "aliwka")
class TestAuthAPI:
    @allure.title("Valid authorization")
    @pytest.mark.asyncio
    async def test_valid_authorization(self, auth_client):
        response = await auth_client.login(
            email=config.app.test_user_email, password=config.app.test_user_password
        )
        assert response.json()["user"]["email"] == config.app.test_user_email

    @allure.title("Authorization with invalid email")
    @pytest.mark.asyncio
    async def test_authorization_with_invalid_email(self, auth_client):
        fake = Faker()
        response = await auth_client.login(
            fake.email() + "@", fake.password(), expected_status=400
        )
        
        assert (
            response.json()["email"][0] == "Введите правильный адрес электронной почты."
        ), "Ввод почты не правильного формата пропускается системой"

   