import allure

from tests.conftest import events_page


def test_add_event_to_favorite(main_page, events_page, auth_page: AuthPage, events_create_page, base_user_creds):
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
        events_create_page.create_event_click()

    with allure.step("Заполнение формы"):
        events_create_page.fill_required_fields()
