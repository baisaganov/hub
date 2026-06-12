from clients.base.base_client import BaseClient


class UsersClient(BaseClient):
    async def create_user(self, name: str, email: str, role: str = "user"):
        payload = {
            "name": name,
            "email": email,
            "role": role,
        }
        response = await self.post(
            "/users",
            json_body=payload,
            expected_status=201,
        )
        return response.json()

    async def get_user(self, user_id: str):
        response = await self.get(
            f"/users/{user_id}",
            expected_status=200,
        )
        return response.json()

    async def list_users(self, page: int = 1, limit: int = 20, role: str | None = None):
        params = {
            "page": page,
            "limit": limit,
        }
        if role:
            params["role"] = role

        response = await self.get(
            "/users",
            params=params,
            expected_status=200,
        )
        return response.json()

    async def update_user_email(self, user_id: str, email: str):
        response = await self.patch(
            f"/users/{user_id}",
            json_body={"email": email},
            expected_status=200,
        )
        return response.json()

    async def delete_user(self, user_id: str):
        response = await self.delete(
            f"/users/{user_id}",
            expected_status=(200, 204),
        )
        return response

    async def create_and_fetch_user(self, name: str, email: str, role: str = "user"):
        created_user = await self.create_user(name=name, email=email, role=role)
        fetched_user = await self.get_user(created_user["id"])
        return fetched_user