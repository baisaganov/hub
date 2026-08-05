from uuid import UUID

from pydantic import BaseModel


class AuthUser(BaseModel):
    id: int
    username: str
    iin: str | None
    email: str
    email_verified: bool
    phone: str | None
    phone_verified: bool
    first_name: str
    last_name: str
    middle_name: str | None
    full_name: str
    is_staff: bool
    is_superuser: bool
    blocked: bool
    role: str
    avatar_letters: str
    privacy_policy_accepted: bool
    signup_flow_completed: bool
    last_login: str | None


class LoginResponse(BaseModel):
    user: AuthUser
    token: str | None
    redirect_url: str | None


class AuthCheckResponse(BaseModel):
    """Ответ /auth/check/ — определяет метод входа и наличие юзера"""

    value: str
    method: str  # "email" | "phone"
    user_exists: bool


class ActivationResponse(BaseModel):
    """
    Единый контракт запуска активации (OTP/регистрация/сброс пароля/смена телефона):
    uuid активации + задержка до повторной отправки кода.
    """

    activation: UUID
    resend_delay: int


class PermissionsListResponse(BaseModel):
    """Ответ GET /permissions/"""

    result: list


class HasPermissionsResponse(BaseModel):
    """Ответ POST /has_permissions/"""

    valid: bool


class OpenApiSchemaResponse(BaseModel):
    """Минимальный контракт OpenAPI-схемы сервиса"""

    openapi: str
    info: dict
    paths: dict


class UpdateNamesRequest(BaseModel):
    """Тело /flow/set_names/ и /profile/update_profile/"""

    first_name: str
    last_name: str
