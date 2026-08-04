import pytest
import allure

from testdata.factories import fake_contact_request, empty_contact_request

pytestmark = [pytest.mark.api]


@allure.suite("UserSettings")
@allure.label("owner", "aliwka")
class TestUserSettings:
    @allure.title("UserSettings contact")
    @pytest.mark.asyncio
    async def test_user_setting_valid(self, user_client):
        with allure.step("Сохранение валидных контактов"):
            # клиент сам упадёт с ApiError, если статус не 200
            await user_client.save_contact(fake_contact_request())

    @allure.title("UserSettings empty contact returns 400")
    @pytest.mark.asyncio
    async def test_user_settings_none(self, user_client):
        with allure.step("Сохранение пустых контактов"):
            errors = await user_client.save_contact_expect_error(
                empty_contact_request(), expected_status=400
            )

        with allure.step("Проверка ошибок валидации"):
            assert errors["website"][0] == 'Это поле не может быть пустым.'
            assert "linkedin_url" in errors
            assert "facebook_url" in errors
            assert "portfolio_url" in errors
