import allure
import pytest

from playwright.sync_api import Page
from config import config


@allure.suite("Events")
class TestEvents:
    @allure.title("Сохранение ивента с одной сферой")
    @allure.description("Тест проверяет, что ивент с одной сферой корректно сохраняется")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('env, scope_count', [('qa', 1), ('qa', 3)])
    def test_event_send(self, page: Page, auth_page, event_page, test_user, env, scope_count):
        config.app.subdomain = env
        config.app.update_app_url()

        with allure.step('Авторизация на портале'):
            auth_page.email_auth(test_user['email'], test_user['password'])

        with allure.step('Переход на страницу мероприятий'):
            event_page.navigate()

        with allure.step('Переход к форме создания'):
            event_page.open_create_form()

        with allure.step('Заполнение формы'):
            event_page.fill_form(test_user['company_id'], scope_count=scope_count)

        with allure.step('Отправка заявки'):
            event_page.action_buttons('submit-create-event')

