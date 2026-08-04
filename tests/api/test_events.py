import allure
import pytest

pytestmark = [pytest.mark.api]


@allure.suite('Events')
@allure.label("owner", "aliwka")
class TestEvents:

    @allure.title("Test Events List active")
    @pytest.mark.asyncio
    async def test_events_list_active_true(self, events_client):
        with allure.step('Получение списка активных ивентов'):
            events = await events_client.get_events_list(is_active=True)

        if events.count == 0:
            pytest.skip('Нет активных мероприятий')

        with allure.step('Проверка что пришли только активные'):
            for event in events.results:
                assert event.available is True, (
                    f'Мероприятие {event.id} ({event.slug}): available={event.available}, '
                    f'ожидалось True'
                )
