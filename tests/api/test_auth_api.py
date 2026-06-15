import pytest
import allure

pytestmark = [pytest.mark.api]

@allure.suite('Authorization')
class TestAuthAPI:
    @allure.title('Valid authorization')
    @pytest.mark.asyncio
    async def test_valid_authorization(self, authorized_http_client):
        # response, cookies = await auth_client.login(email='a.baisaganov@astanahub.com', password='Pass1234!')
        # assert response['user']['email'] == 'auto_test_base_user@hub.kz'


        response = await authorized_http_client.post(
                    's/auth/api/v1/has_permissions/',
                    json_body={
                        "permissions": [
                                        "ai_moderation"
                                    ]
                    },
                    expected_status=200,
                )

        print(response.json())




    # @pytest.mark.asyncio
    # async def test_create_user_success(users_client):
    #     user = await users_client.create_user(
    #         name="Alisher",
    #         email="alisher@example.com",
    #     )

    #     assert user["name"] == "Alisher"
    #     assert user["email"] == "alisher@example.com"
    #     assert user["role"] == "user"


    # @pytest.mark.asyncio
    # async def test_created_user_can_be_fetched(users_client, created_user):
    #     fetched_user = await users_client.get_user(created_user["id"])

    #     assert fetched_user["id"] == created_user["id"]
    #     assert fetched_user["email"] == created_user["email"]


    # @pytest.mark.asyncio
    # async def test_create_user_without_email_returns_400(users_client):
    #     response = await users_client.raw_create_user(
    #         payload={"name": "Broken User"},
    #         expected_status=400,
    #     )

    #     body = response.json()
    #     assert response.status_code == 400
    #     assert "email" in body["errors"]