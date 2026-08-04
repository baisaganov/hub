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
