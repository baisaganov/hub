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
    def test_event_send(
        self, auth_page, events_page, events_create_page, base_user_creds
    ):

        with allure.step("Авторизация на портале"):
            auth_page.email_auth(base_user_creds["email"], base_user_creds["password"])

        with allure.step("Переход на страницу мероприятий"):
            events_page.navigate()

        with allure.step("Переход к форме создания"):
            events_page.create_event_click()

        with allure.step("Заполнение формы"):
            events_create_page.fill_form(scope_count=1)

        with allure.step("Отправка заявки"):
            events_create_page.action_buttons("submit-create-event")
