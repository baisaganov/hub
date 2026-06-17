import pytest
import allure
from config import config

pytestmark = [pytest.mark.api]


@allure.suite("UserSettings")
class TestUserSettings:
    @allure.title("UserSettings contact")
    @pytest.mark.asyncio
    async def test_user_setting_valid(self, user_client):
        await user_client.save_contact(
            phone="778", email="aa@a.com", url=''
        )
    async def test_user_settings_none(self,user_client):
        response=  await user_client.save_contact(
            phone=None, email=None, url=None, expected_status=400
        )
        assert response["website"][0] == 'Это поле не может быть пустым.'
        
