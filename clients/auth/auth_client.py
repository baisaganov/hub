import httpx

from clients.base.base_client import BaseClient
from models import (
    ActivationResponse,
    AuthCheckResponse,
    AuthUser,
    DetailResponse,
    HasPermissionsResponse,
    LoginResponse,
    OpenApiSchemaResponse,
    PermissionDeniedResponse,
    PermissionsListResponse,
    UpdateNamesRequest,
    ValidationErrorResponse,
)

SCHEMA_URL = "s/auth/api/schema/"
LOGIN_URL = "s/auth/api/v1/auth/email/"
CHECK_URL = "s/auth/api/v1/auth/check/"
EMAIL_OTP_URL = "s/auth/api/v1/auth/email_otp/"
EMAIL_REGISTRATION_URL = "s/auth/api/v1/auth/email_registration/"
EMAIL_RESET_PASSWORD_URL = "s/auth/api/v1/auth/email_reset_password/"
PHONE_LOGIN_URL = "s/auth/api/v1/auth/phone/"
PHONE_REGISTRATION_URL = "s/auth/api/v1/auth/phone_registration/"
PHONE_RESET_PASSWORD_URL = "s/auth/api/v1/auth/phone_reset_password/"
GOOGLE_LOGIN_URL = "s/auth/api/v1/auth/google/"
APPLE_LOGIN_URL = "s/auth/api/v1/auth/apple/"
ACTIVATION_CONFIRM_URL = "s/auth/api/v1/auth/activation_confirm/"
PRIVACY_POLICY_ACCEPT_URL = "s/auth/api/v1/auth/privacy_policy_accept/"
FLOW_SET_NAMES_URL = "s/auth/api/v1/flow/set_names/"
FLOW_SET_PASSWORD_URL = "s/auth/api/v1/flow/set_password/"
FLOW_SET_PHOTO_URL = "s/auth/api/v1/flow/set_photo/"
FLOW_SET_COMPLETED_URL = "s/auth/api/v1/flow/set_completed/"
PERMISSIONS_URL = "s/auth/api/v1/permissions/"
PERMISSION_CHECK_URL = "s/auth/api/v1/permissions/check/{permission}/"
HAS_PERMISSIONS_URL = "s/auth/api/v1/has_permissions/"
PROFILE_INFO_URL = "s/auth/api/v1/profile/info/"
PROFILE_INFO_BY_ID_URL = "s/auth/api/v1/profile/info_by_id/"
PROFILE_UPDATE_URL = "s/auth/api/v1/profile/update_profile/"
CHANGE_EMAIL_URL = "s/auth/api/v1/profile/change_email/"
CHANGE_PASSWORD_URL = "s/auth/api/v1/profile/change_password/"
CHANGE_PHONE_URL = "s/auth/api/v1/profile/change_phone/"
DELETE_ACCOUNT_URL = "s/auth/api/v1/profile/delete_account/"
EXTERNAL_USER_INFO_URL = "s/auth/api/v1/external/user/info/"


class AuthClient(BaseClient):
    # --- логин ---

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

    async def login_phone_expect_error(
        self, phone: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Логин по невалидному телефону. Ошибка приходит в поле `value`."""
        response = await self.post(
            PHONE_LOGIN_URL,
            json_body={"phone": phone},
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())

    async def login_google_expect_error(
        self, access_token: str, expected_status: int = 500
    ) -> ValidationErrorResponse:
        """Логин через Google с невалидным токеном"""
        await self.post(
            GOOGLE_LOGIN_URL,
            json_body={"access_token": access_token},
            expected_status=expected_status,
        )

        

    async def login_apple_expect_error(
        self, id_token: str, expected_status: int = 500
    ) -> ValidationErrorResponse:
        """Логин через Apple с невалидным токеном"""
        await self.post(
            APPLE_LOGIN_URL,
            json_body={"id_token": id_token},
            expected_status=expected_status,
        )


    # --- проверка и регистрация ---

    async def check(self, value: str) -> AuthCheckResponse:
        """Проверка email/телефона: метод входа и существование юзера"""
        response = await self.post(
            CHECK_URL, json_body={"value": value}, expected_status=200
        )

        return AuthCheckResponse.model_validate(response.json())

    async def request_email_otp(self, email: str) -> ActivationResponse:
        """Запрос OTP-кода на зарегистрированный email"""
        response = await self.post(
            EMAIL_OTP_URL, json_body={"email": email}, expected_status=200
        )

        return ActivationResponse.model_validate(response.json())

    async def request_email_otp_expect_error(
        self, email: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Запрос OTP на невалидный/незарегистрированный email"""
        response = await self.post(
            EMAIL_OTP_URL, json_body={"email": email}, expected_status=expected_status
        )

        return ValidationErrorResponse.model_validate(response.json())

    async def register_email(self, email: str) -> ActivationResponse:
        """Старт регистрации по email — создаёт активацию"""
        response = await self.post(
            EMAIL_REGISTRATION_URL,
            json_body={"email": email, "privacy_policy_confirmed": True},
            expected_status=200,
        )

        return ActivationResponse.model_validate(response.json())

    async def register_email_expect_error(
        self, email: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Регистрация по занятому/невалидному email"""
        response = await self.post(
            EMAIL_REGISTRATION_URL,
            json_body={"email": email, "privacy_policy_confirmed": True},
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())

    async def register_phone_expect_error(
        self, phone: str, expected_status: int = 500
    ) -> ValidationErrorResponse:
        """Регистрация по невалидному телефону"""
        await self.post(
            PHONE_REGISTRATION_URL,
            json_body={"phone": phone},
            expected_status=expected_status,
        )

    # --- сброс пароля ---

    async def reset_password_email(self, email: str) -> ActivationResponse:
        """Запрос сброса пароля на зарегистрированный email"""
        response = await self.post(
            EMAIL_RESET_PASSWORD_URL, json_body={"email": email}, expected_status=200
        )

        return ActivationResponse.model_validate(response.json())

    async def reset_password_email_expect_error(
        self, email: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Сброс пароля на невалидный/незарегистрированный email"""
        response = await self.post(
            EMAIL_RESET_PASSWORD_URL,
            json_body={"email": email},
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())

    async def reset_password_phone_expect_error(
        self, phone: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Сброс пароля по неизвестному телефону"""
        response = await self.post(
            PHONE_RESET_PASSWORD_URL,
            json_body={"phone": phone},
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())

    # --- активация ---

    async def confirm_activation_expect_error(
        self, activation: str, code: str, expected_status: int = 404
    ) -> DetailResponse:
        """Подтверждение несуществующей активации"""
        response = await self.post(
            ACTIVATION_CONFIRM_URL,
            json_body={"activation": activation, "code": code},
            expected_status=expected_status,
        )

        return DetailResponse.model_validate(response.json())

    # --- схема ---

    async def get_openapi_schema(self) -> OpenApiSchemaResponse:
        """OpenAPI-схема сервиса в JSON"""
        response = await self.get(
            SCHEMA_URL, params={"format": "json"}, expected_status=200
        )

        return OpenApiSchemaResponse.model_validate(response.json())

    # --- профиль ---

    async def get_profile_info(self) -> AuthUser:
        """Профиль текущего юзера"""
        response = await self.get(PROFILE_INFO_URL, expected_status=200)

        return AuthUser.model_validate(response.json())

    async def get_profile_info_expect_error(
        self, expected_status: int = 401
    ) -> DetailResponse:
        """Профиль без авторизации"""
        response = await self.get(PROFILE_INFO_URL, expected_status=expected_status)

        return DetailResponse.model_validate(response.json())

    async def get_profile_info_by_id_expect_error(
        self, user_id: int, expected_status: int = 403
    ) -> PermissionDeniedResponse:
        """info_by_id без служебных прав"""
        response = await self.get(
            PROFILE_INFO_BY_ID_URL,
            params={"id": user_id},
            expected_status=expected_status,
        )

        return PermissionDeniedResponse.model_validate(response.json())

    async def update_profile(self, names: UpdateNamesRequest) -> httpx.Response:
        """Обновление имени/фамилии. Успешный ответ — пустое тело, модели нет."""
        return await self.post(
            PROFILE_UPDATE_URL, json_body=names.model_dump(), expected_status=200
        )

    async def change_email_expect_error(
        self, email: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Смена email на невалидный"""
        response = await self.post(
            CHANGE_EMAIL_URL, json_body={"email": email}, expected_status=expected_status
        )

        return ValidationErrorResponse.model_validate(response.json())

    async def change_password_expect_error(
        self, old_password: str, password: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Смена пароля с неверным старым паролем"""
        response = await self.post(
            CHANGE_PASSWORD_URL,
            json_body={"old_password": old_password, "password": password},
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())

    async def change_phone(self, phone: str) -> ActivationResponse:
        """Смена телефона — создаёт активацию, телефон меняется после подтверждения кодом"""
        response = await self.post(
            CHANGE_PHONE_URL, json_body={"phone": phone}, expected_status=200
        )

        return ActivationResponse.model_validate(response.json())

    async def delete_account_expect_error(
        self, expected_status: int = 401
    ) -> DetailResponse:
        """Удаление аккаунта без авторизации"""
        response = await self.post(
            DELETE_ACCOUNT_URL, expected_status=expected_status
        )

        return DetailResponse.model_validate(response.json())

    async def accept_privacy_policy_expect_error(
        self, accepted: bool = True, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Повторное принятие политики конфиденциальности"""
        response = await self.post(
            PRIVACY_POLICY_ACCEPT_URL,
            json_body={"accepted": accepted},
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())

    # --- онбординг-флоу ---

    async def flow_set_names(self, names: UpdateNamesRequest) -> httpx.Response:
        """Шаг флоу: имя и фамилия. Успешный ответ — пустое тело."""
        return await self.post(
            FLOW_SET_NAMES_URL, json_body=names.model_dump(), expected_status=200
        )

    async def flow_set_password_expect_error(
        self, password: str, expected_status: int = 400
    ) -> ValidationErrorResponse:
        """Шаг флоу: невалидный пароль"""
        response = await self.post(
            FLOW_SET_PASSWORD_URL,
            json_body={"password": password},
            expected_status=expected_status,
        )

        return ValidationErrorResponse.model_validate(response.json())

    async def flow_skip_photo(self) -> httpx.Response:
        """Шаг флоу: пропуск фото. Успешный ответ — пустое тело."""
        return await self.post(
            FLOW_SET_PHOTO_URL, json_body={"skip": True}, expected_status=200
        )

    async def flow_set_completed(self) -> httpx.Response:
        """Шаг флоу: завершение онбординга. Успешный ответ — пустое тело."""
        return await self.post(FLOW_SET_COMPLETED_URL, expected_status=200)

    # --- права ---

    async def get_permissions(self) -> PermissionsListResponse:
        """Список прав текущего юзера"""
        response = await self.get(PERMISSIONS_URL, expected_status=200)

        return PermissionsListResponse.model_validate(response.json())

    async def check_permission_expect_error(
        self, permission: str, expected_status: int = 403
    ) -> DetailResponse:
        """Проверка права, которого нет у юзера"""
        response = await self.get(
            PERMISSION_CHECK_URL.format(permission=permission),
            expected_status=expected_status,
        )

        return DetailResponse.model_validate(response.json())

    async def has_permissions(self, permissions: list[str]) -> HasPermissionsResponse:
        """Проверка набора прав"""
        response = await self.post(
            HAS_PERMISSIONS_URL,
            json_body={"permissions": permissions},
            expected_status=200,
        )

        return HasPermissionsResponse.model_validate(response.json())

    # --- external ---

    async def get_external_user_info_expect_error(
        self, expected_status: int = 401
    ) -> DetailResponse:
        """external/user/info без Bearer-токена (куки не принимаются)"""
        response = await self.get(
            EXTERNAL_USER_INFO_URL, expected_status=expected_status
        )

        return DetailResponse.model_validate(response.json())
