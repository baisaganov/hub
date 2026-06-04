import allure

from tests.conftest import events_page


def test_add_event_to_favorite(main_page, events_page, auth_page: AuthPage, base_user_creds):
    with allure.step("Авторизация"):
        auth_page.email_auth(base_user_creds['email'], password=base_user_creds['password'])
        main_page.page.keyboard.press("Escape")

    with allure.step("Переход к Мероприятиям"):
        with main_page.page.expect_response("**/event/") as response:
            main_page.page.keyboard.press("Escape")
            main_page.EVENTS_LINK.click()
            try:
                main_page.EVENTS_LINK.click()
            except:
                pass
        assert response.value.status == 200, "Events page does not open"
    with allure.step("Проверка наличия кнопки 'Создать мероприятие'"):
        assert events_page.CREATE_EVENT_BUTTON.is_visible(), "Кнопка 'Создать мероприятие' не отображается для авторизованного пользователя"
    with allure.step("Выбор компании"):
        events_page.CREATE_EVENT_BUTTON.click()
        events_page.COMPANY_SELECT.select_option(label="QA Studio LLP")
        assert events_page.COMPANY_SELECT.input_value() != "", "Компания не выбрана"
