from pydantic import BaseModel

VISIBILITY_PRIVATE = "private"


class VisibilitySettings(BaseModel):
    contact_phone: str = VISIBILITY_PRIVATE
    contact_email: str = VISIBILITY_PRIVATE
    website: str = VISIBILITY_PRIVATE
    linkedin_url: str = VISIBILITY_PRIVATE
    facebook_url: str = VISIBILITY_PRIVATE
    portfolio_url: str = VISIBILITY_PRIVATE


class UpdateContactRequest(BaseModel):
    """Тело запроса account/api/user/update_profile/"""

    contact_phone: str | None
    contact_email: str | None
    website: str | None
    linkedin_url: str | None
    facebook_url: str | None
    portfolio_url: str | None
    visibility_settings: VisibilitySettings = VisibilitySettings()
