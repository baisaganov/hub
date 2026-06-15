from clients.base.base_client import BaseClient


class AuthClient(BaseClient):
    async def login(self, email: str, password: str, expected_status = 200) -> str:
        response = await self.post(
            "s/auth/api/v1/auth/email/",
            json_body={
                "email": email,
                "password": password,
            },
            expected_status=expected_status,
        )
        
        return response.json()
