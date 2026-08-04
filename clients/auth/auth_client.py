from clients.base.base_client import BaseClient
from models import LoginResponse, ValidationErrorResponse

LOGIN_URL = "s/auth/api/v1/auth/email/"


class AuthClient(BaseClient):
    async def login(self, email: str, password: str) -> LoginResponse:
        """
        Успешный логин. Куки сессии оседают в cookie jar httpx-клиента
        (self.client.cookies).
        :return: валидированный ответ — контракт проверяется моделью
        """
        response = await self.post(
            LOGIN_URL,
            json_body={"email": email, "password": password},
            expected_status=200,
        )

        return LoginResponse.model_validate(response.json())

    async def login_expect_error(
        self, email: str, password: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Логин с невалидными кредами. :return: ошибки по полям"""
        response = await self.post(
            LOGIN_URL,
            json_body={"email": email, "password": password},
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())
