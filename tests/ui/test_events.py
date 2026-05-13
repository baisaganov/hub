import allure
import pytest

from playwright.sync_api import Page
from config import config


@allure.suite("Events")
@pytest.mark.order(3)
class TestEvents:
    @allure.title("Сохранение ивента с одной сферой")
    @pytest.mark.regression
    @pytest.mark.parametrize('env, scope_count', [('dev', 1)])  # ('qa', 1), ('qa', 3)
    def test_event_send(self,
                        page: Page,
                        auth_page,
                        event_page,
                        main_page,
                        registration_user_creds,


                        env,
                        scope_count):
        config.app.subdomain = env
        config.app.update_app_url()

        if auth_page.is_context_exists(env=env):
            with allure.step('Переход на главную старницу'):
                main_page.navigate()

            with allure.step('Загрузка юзера'):
                auth_page.load_context(env)
        else:
            with allure.step('Авторизация на портале'):
                auth_page.email_auth(registration_user_creds['email'], registration_user_creds['password'])

        with allure.step('Переход на страницу мероприятий'):
            event_page.navigate()

        with allure.step('Переход к форме создания'):
            event_page.open_create_form()

        with allure.step('Заполнение формы'):
            event_page.fill_form(scope_count=scope_count)

        with allure.step('Отправка заявки'):
            event_page.action_buttons('submit-create-event')
