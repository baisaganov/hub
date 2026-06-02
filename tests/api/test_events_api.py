import json

import allure
import pytest
import requests

from config import config


@pytest.mark.api
@allure.suite("Events")
@allure.tag("api")
class TestEventsAPI:
    @staticmethod
    def assert_event_item_structure(event_item: dict) -> None:
        assert isinstance(event_item, dict), "Event item must be an object"
        assert isinstance(event_item.get("id"), int), "Event id must be an integer"

        assert isinstance(
            event_item.get("title"), dict
        ), "Event title must be an object"
        assert "ru" in event_item["title"], "Event title must contain 'ru' field"
        assert isinstance(
            event_item["title"].get("ru"), str
        ), "Event title.ru must be a string"

        assert isinstance(
            event_item.get("author"), dict
        ), "Event author must be an object"
        assert isinstance(
            event_item["author"].get("id"), int
        ), "Author id must be an integer"
        assert isinstance(
            event_item["author"].get("full_name"), str
        ), "Author full_name must be a string"

        assert isinstance(
            event_item.get("status"), str
        ), "Event status must be a string"
        assert isinstance(
            event_item.get("available"), bool
        ), "Event available must be a boolean"

    @allure.title("Проверка доступности списка мероприятий по API")
    def test_get_event_list_status_code(self, api_base_url, api_headers):
        with allure.step("Выполнить GET запрос к /api/event/"):
            response = requests.get(
                f"{api_base_url}/api/event/",
                headers=api_headers,
                timeout=30,
            )

        with allure.step("Проверить код ответа и тип содержимого"):
            assert (
                response.status_code == 200
            ), f"Expected 200 OK, got {response.status_code}"
            assert "application/json" in response.headers.get(
                "Content-Type", ""
            ), "Response content type must be application/json"

        with allure.step("Прикрепить тело ответа для отладки"):
            allure.attach(
                response.text,
                name="event_list_response",
                attachment_type=allure.attachment_type.JSON,
            )

    @allure.title("Проверка структуры ответа списка мероприятий")
    def test_get_event_list_response_schema(self, api_base_url, api_headers):
        with allure.step("Выполнить GET запрос к /api/event/"):
            response = requests.get(
                f"{api_base_url}/api/event/",
                headers=api_headers,
                timeout=30,
            )

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200

        with allure.step("Проверить JSON-структуру"):
            payload = response.json()

            assert isinstance(payload, dict), "Response payload must be an object"
            assert isinstance(payload.get("count"), int), "count must be integer"
            assert "next" in payload, "next field must be present"
            assert "previous" in payload, "previous field must be present"
            assert isinstance(payload.get("results"), list), "results must be a list"

        with allure.step("Проверить хотя бы один элемент результата"):
            results = payload["results"]
            assert results, "results list must not be empty"
            self.assert_event_item_structure(results[0])

    @allure.title("Проверка JSON-валидности ответа")
    def test_get_event_list_valid_json(self, api_base_url, api_headers):
        with allure.step("Выполнить GET запрос и попытаться разобрать JSON"):
            response = requests.get(
                f"{api_base_url}/api/event/",
                headers=api_headers,
                timeout=30,
            )

        with allure.step("Проверить, что тело ответа парсится как JSON"):
            try:
                json.loads(response.text)
            except json.JSONDecodeError as exc:
                pytest.fail(f"Response body is not valid JSON: {exc}")
