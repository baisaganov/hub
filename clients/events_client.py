from clients.base.base_client import BaseClient
import pytest


class EventsClient(BaseClient):
    async def get_events_list(self, is_active=None):
        """Отоборажение только активных мероприятий"""
        response = await self.get(
            f"/api/event/?page_size=1000&is_active={is_active}", expected_status=200
        )

        print(response.json())

        return response

    @staticmethod
    async def check_event_(is_active, json_list):
        if json_list["count"] == 0:
            pytest.skip(f'Нет {"активных" if is_active else "не активных"} мероприятий')

        results_list = json_list['results']
        for i in results_list:
            assert i['available'] == is_active, f'Мероприятие {i['available']} ожидалось {is_active}'