import allure
import pytest

from config import config


@allure.suite("Events")
@allure.label("level", "UI")
@pytest.mark.ui
@pytest.mark.events
class TestEventsCreate:
    @allure.title("Сохранение ивента с одной сферой")
    @pytest.mark.regression
    def test_event_send(self, events_page, events_create_page, api_login):

        with allure.step("Переход на страницу мероприятий (авторизация через API)"):
            events_page.navigate()

        with allure.step("Переход к форме создания"):
            events_page.create_event_click()

        with allure.step("Заполнение формы"):
            events_create_page.fill_form(scope_count=1)

        with allure.step("Отправка заявки"):
            events_create_page.action_buttons("submit-create-event")
