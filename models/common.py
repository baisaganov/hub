from pydantic import BaseModel, RootModel


class ValidationErrorResponse(RootModel[dict[str, list[str]]]):
    """
    Стандартный ответ DRF при 400: {"поле": ["сообщение", ...], ...}
    """

    def __getitem__(self, field: str) -> list[str]:
        return self.root[field]

    def __contains__(self, field: str) -> bool:
        return field in self.root

    @property
    def fields(self) -> set[str]:
        """Имена полей, по которым пришли ошибки"""
        return set(self.root)


class DetailResponse(BaseModel):
    """Стандартный ответ DRF при 401/403/404: {"detail": "сообщение"}"""

    detail: str


class PermissionDeniedResponse(BaseModel):
    """Кастомный ответ auth-сервиса при 403: {"error": "PermissionDenied"}"""

    error: str