import allure
import pytest

from pages.auth_page import AuthPage


@allure.suite("Events")
@pytest.mark.events
class TestEvents:

    @allure.title("Events")
    @pytest.mark.critical
    def test_participate_event(
        self,
        main_page,
        events_page,
        auth_page: AuthPage,
        base_user_creds,
    ):
        with allure.step("Авторизация"):
            auth_page.email_auth(
                base_user_creds["email"],
                password=base_user_creds["password"],
            )
            main_page.page.keyboard.press("Escape")

        with allure.step("Переход к Мероприятиям"):
            with main_page.page.expect_response("**/event/") as response:
                main_page.page.keyboard.press("Escape")
                main_page.EVENTS_LINK.click()

                try:
                    main_page.EVENTS_LINK.click()
                except Exception:
                    pass

            assert response.value.status == 200, "Event Page does not open"

        with allure.step("Открытие Мероприятия"):
            events_page.open_event_card(0)

        with allure.step('Клик на "Участвовать"'):
            events_page.click_participate_btn()

        with allure.step("Заполнение формы"):
            selected_role = events_page.choose_random_role_event()
            events_page.checkbox_click()

            print(f"Выбрана роль: {selected_role}")

        with allure.step("Отправка"):
            events_page.submit_participation_form()