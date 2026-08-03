import re

import allure
import pytest
from playwright.sync_api import expect

from config import config


@allure.suite("Events")
@allure.label("level", "UI")
@pytest.mark.ui
@pytest.mark.events
@allure.label("owner", "aliwka")
class TestEventsCreate:
    @allure.title("Сохранение ивента с одной сферой")
    @pytest.mark.regression
    def test_event_send(self, page, events_page, events_create_page, api_login):

        with allure.step("Переход на страницу мероприятий (авторизация через API)"):
            events_resp = events_page.navigate()
            assert events_resp.status in (200, 301), (
                f"Страница мероприятий не доступна: {events_resp.status}"
            )

        with allure.step("Переход к форме создания"):
            create_page_resp = events_page.create_event_click()
            assert create_page_resp.status == 200, (
                f"Страница создания не открылась: {create_page_resp.status}"
            )

        with allure.step("Проверка дефолтного формата — Онлайн"):
            expect(events_create_page.format_option("online")).to_have_class(
                re.compile("bg-surface-brand-fade")
            )

        with allure.step("Заполнение формы"):
            scopes = events_create_page.fill_form(scope_count=1)

        with allure.step("Проверка заполненной формы"):
            assert len(scopes) == 1, f"Выбрано сфер: {len(scopes)}, ожидалась 1"
            expect(events_create_page.SCOPE_SELECTED_PILLS).to_have_count(1)
            expect(events_create_page.EVENT_TITLE_VISIBLE).not_to_be_empty()
            expect(events_create_page.EVENT_EMAIL).to_have_value(config.app.test_user_email)
            expect(events_create_page.POLICY_CHECKBOX).to_be_checked()
            expect(events_create_page.AGREEMENT_CHECKBOX).to_be_checked()

        with allure.step("Отправка на модерацию"):
            create_resp, send_resp = events_create_page.submit_for_moderation()

        with allure.step("Проверка ответов API и редиректа"):
            assert create_resp.status in (200, 201), (
                f"Создание ивента не прошло: {create_resp.status}, {create_resp.text()}"
            )
            assert send_resp.status == 200, (
                f"Отправка на модерацию не прошла: {send_resp.status}, {send_resp.text()}"
            )
            expect(page).to_have_url(re.compile(r"/event/"))
