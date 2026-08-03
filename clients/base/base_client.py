import json
from typing import Any

import allure
import httpx

from utils.logger import Logger

logger = Logger().get_logger(__name__)


class ApiError(Exception):
    def __init__(
        self, message: str, status_code: int | None = None, response_body: Any = None
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        extras = []
        if self.status_code is not None:
            extras.append(f"status_code={self.status_code}")
        if self.response_body is not None:
            extras.append(f"response_body={self.response_body}")
        suffix = f" ({'; '.join(extras)})" if extras else ""
        return f"{super().__str__()}{suffix}"


class BaseClient:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _request(
        self,
        method: str,
        url: str,
        *,
        expected_status: int | tuple[int, ...] | list[int] | None = None,
        params: dict | None = None,
        json_body: dict | list | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> httpx.Response:
        with allure.step(f"{method} {url}"):
            if params:
                allure.attach(
                    json.dumps(params, ensure_ascii=False, indent=2),
                    name="query_params",
                    attachment_type=allure.attachment_type.JSON,
                )

            if json_body:
                allure.attach(
                    json.dumps(json_body, ensure_ascii=False, indent=2),
                    name="request_body",
                    attachment_type=allure.attachment_type.JSON,
                )

            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=json_body,
                data=data,
                headers=headers,
            )

            allure.attach(
                str(response.status_code),
                name="status_code",
                attachment_type=allure.attachment_type.TEXT,
            )

            allure.attach(
                self._safe_response_text(response),
                name="response_body",
                attachment_type=(
                    allure.attachment_type.JSON
                    if "application/json" in response.headers.get("content-type", "")
                    else allure.attachment_type.TEXT
                ),
            )

            if expected_status is not None:
                expected = (
                    {expected_status}
                    if isinstance(expected_status, int)
                    else set(expected_status)
                )
                if response.status_code not in expected:
                    error_message = f"{method} {url} returned {response.status_code}, expected {expected}."
                    response_body = self._safe_json(response)
                    logger.error(error_message)
                    logger.error("Response body: %s", response_body)
                    raise ApiError(
                        message=error_message,
                        status_code=response.status_code,
                        response_body=response_body,
                    )

            return response

    async def get(self, url: str, *, expected_status=None, params=None, headers=None):
        return await self._request(
            "GET", url, expected_status=expected_status, params=params, headers=headers
        )

    async def post(
        self, url: str, *, expected_status=None, json_body=None, data=None, headers=None
    ):
        return await self._request(
            "POST",
            url,
            expected_status=expected_status,
            json_body=json_body,
            data=data,
            headers=headers,
        )

    async def patch(
        self, url: str, *, expected_status=None, json_body=None, headers=None
    ):
        return await self._request(
            "PATCH",
            url,
            expected_status=expected_status,
            json_body=json_body,
            headers=headers,
        )

    async def delete(self, url: str, *, expected_status=None, headers=None):
        return await self._request(
            "DELETE", url, expected_status=expected_status, headers=headers
        )

    @staticmethod
    def _safe_json(response: httpx.Response):
        try:
            return response.json()
        except Exception:
            return response.text

    @staticmethod
    def _safe_response_text(response: httpx.Response):
        try:
            return json.dumps(response.json(), ensure_ascii=False, indent=2)
        except Exception:
            return response.text
