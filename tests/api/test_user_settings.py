import pytest
import allure

pytestmark = [pytest.mark.api]


@allure.suite("UserSettings")
@allure.label("owner", "aliwka")
class TestUserSettings:
    @allure.title(test_title="UserSettings contact")
    @pytest.mark.asyncio
    async def test_user_setting_valid(self, user_client):
        await user_client.save_contact(
            phone="778", email="aa@a.com", url=''
        )

    
    @allure.title("UserSettings empty contact returns 400")
    @pytest.mark.asyncio
    async def test_user_settings_none(self,user_client):
        response=  await user_client.save_contact(
            phone=None, email=None, url=None, expected_status=400
        )
        assert response["website"][0] == 'Это поле не может быть пустым.'
        
