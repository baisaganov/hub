import allure
import pytest


@allure.suite("Events")
@allure.label("level", "UI")
@pytest.mark.events
@pytest.mark.ui
class TestEvents:

    @allure.title("Events")
    @pytest.mark.critical
    def test_participate_event(self, main_page, events_page, api_login):
        with allure.step("Авторизация через API и открытие главной"):
            main_page.navigate()

        with allure.step("Переход к Мероприятиям"):
            response = main_page.open_page_from_menu('event')
            assert response.value.status == 200, "Event Page does not open"

        with allure.step("Открытие Мероприятия"):
            if events_page.get_cards_count() == 0:
                pytest.skip("Нет доступных мероприятий")
            events_page.open_event_card()

        with allure.step('Клик на "Участвовать"'):
            events_page.click_participate_btn()

        with allure.step("Заполнение формы"):
            events_page.checkbox_click()
            events_page.get_result()



        with allure.step("Отправка"):
            events_page.submit_form()
