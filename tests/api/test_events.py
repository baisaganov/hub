import allure
import pytest

@allure.suite('Events')
@allure.label("owner", "aliwka")
class TestEvents:


    
    @allure.title(test_title="Test Events List active")
    @pytest.mark.asyncio
    async def test_events_list_active_true(self, events_client):
        with allure.step('Получение списка активных ивентов'):
            response = await events_client.get_events_list(is_active=True)

        with allure.step('Проверка что пришли только активные'):
            await events_client.check_event_(is_active=True, json_list=response.json())

