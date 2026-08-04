import httpx

from clients.base.base_client import BaseClient
from models import UpdateContactRequest, ValidationErrorResponse

UPDATE_PROFILE_URL = "account/api/user/update_profile/"


class UserClient(BaseClient):
    async def save_contact(self, contacts: UpdateContactRequest) -> httpx.Response:
        """
        Сохранение контактов профиля. Успешный ответ приходит с пустым телом,
        поэтому модели ответа нет — клиент падёт с ApiError, если статус не 200.
        """
        return await self.post(
            UPDATE_PROFILE_URL,
            json_body=contacts.model_dump(),
            expected_status=200,
        )

    async def save_contact_expect_error(
        self, contacts: UpdateContactRequest, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Сохранение невалидных контактов. :return: ошибки по полям"""
        response = await self.post(
            UPDATE_PROFILE_URL,
            json_body=contacts.model_dump(),
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())
