from clients.base.base_client import BaseClient


class UserClient(BaseClient):
    # async def login(self, email: str, password: str, expected_status = 200) -> str:
    #     response = await self.post(
    #         "s/auth/api/v1/auth/email/",
    #         json_body={
    #             "email": email,
    #             "password": password,
    #         },
    #         expected_status=expected_status,
    #     )
        
    #     return response.json()

    async def save_contact(self, phone, email, url='', expected_status=200):
        response = await self.post(
            "account/api/user/update_profile/",
            json_body=
                {
                    "contact_phone": phone,
                    "contact_email": email,
                    "website": url,
                    "linkedin_url": url,
                    "facebook_url": url,
                    "portfolio_url": url,
                    "visibility_settings": {
                        "contact_phone": "private",
                        "contact_email": "private",
                        "website": "private",
                        "linkedin_url": "private",
                        "facebook_url": "private",
                        "portfolio_url": "private"
                    }
                }
            , 
               expected_status=expected_status,
            
        )
        return response.json()
