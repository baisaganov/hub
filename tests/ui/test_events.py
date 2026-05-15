import allure
import pytest
from config import config
from playwright.sync_api import Page




@allure.suite('Events')
@pytest.mark.events
class TestEvents:


    @allure.title('Events')
    @pytest.mark.critical
    @pytest.mark.parametrize('env', ['qa'])
    def test_participate_event(self, main_page, events_page, env):
        config.app.subdomain = env
        config.app.update_app_url()

        with allure.step('Подгружаем куки'):
            main_page.navigate()
            main_page.load_context(env)
            main_page.page.reload()
            main_page.page.keyboard.press('Escape')

        with allure.step('Переход к Мероприятиям'):

            with main_page.page.expect_response('**/event/') as response:
                main_page.page.keyboard.press('Escape')
                main_page.EVENTS_LINK.click()
                try:
                    main_page.EVENTS_LINK.click()
                except:
                    pass

            assert response.value.status == 200, 'Event Page does not open'

        with allure.step('Открытие Мероприятия'):
            events_page.open_event_card(0)

        with allure.step('Клик на "Участвовать"'):
            events_page.click_participate_btn()
            main_page.page.pause()

        with allure.step('Заполнение формы'):
            pass

        with allure.step('Отправка'):
            pass