from clients.base.base_client import BaseClient
from models import EventsListResponse


class EventsClient(BaseClient):
    async def get_events_list(self, is_active: bool | None = None) -> EventsListResponse:
        """
        Список мероприятий
        :param is_active: фильтр по активности
        :return: валидированный ответ — контракт проверяется моделью
        """
        response = await self.get(
            f"/api/event/?page_size=1000&is_active={is_active}", expected_status=200
        )

        return EventsListResponse.model_validate(response.json())
