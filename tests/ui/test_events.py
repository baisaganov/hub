import allure
import pytest

from playwright.sync_api import expect


@allure.suite("Events")
@allure.label("level", "UI")
@pytest.mark.events
@pytest.mark.ui
@allure.label("owner", "aliwka")
class TestEvents:

    @allure.title("Events")
    @pytest.mark.critical
    def test_participate_event(self, main_page, events_page, api_login):
        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step("Переход к Мероприятиям"):
            response = main_page.open_page_from_menu('event')
            assert response.value.status == 200, "Event Page does not open"

        with allure.step("Открытие Мероприятия"):
            if events_page.get_cards_count() == 0:
                pytest.skip("Нет доступных мероприятий")
            events_page.open_event_card()

        with allure.step('Клик на "Участвовать"'):
            if not events_page.click_participate_btn():
                pytest.skip("Кнопка Участвовать недоступна (заявка уже подана)")
            expect(events_page.MODAL_EVENT).to_be_visible()

        with allure.step("Заполнение формы"):
            events_page.checkbox_click()

        with allure.step("Проверка заполненной формы"):
            expect(events_page.EMAIL).not_to_be_empty()
            expect(events_page.FULL_NAME).not_to_be_empty()
            expect(events_page.AGREEMENT_CHECKBOX).to_be_checked()

        with allure.step("Отправка"):
            events_page.submit_form()
