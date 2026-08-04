from pydantic import RootModel


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
