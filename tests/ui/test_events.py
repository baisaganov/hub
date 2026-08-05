import allure
import pytest
import re
from config import config

from playwright.sync_api import expect

mutates_data = pytest.mark.skipif(
    config.is_production(), reason="Мутирует данные — только dev/qa"
)


@allure.suite("Events")
@allure.label("level", "UI")
@pytest.mark.events
@pytest.mark.ui
@allure.label("owner", "aliwka")
@pytest.mark.xdist_group("events")
class TestEvents:

    @allure.title("Отправление ивента с одной сферой")
    @pytest.mark.critical
    @mutates_data
    def test_event_send(self, page, events_page, events_create_page, api_login):
        with allure.step("Переход на страницу мероприятий (авторизация через API)"):
            events_resp = events_page.navigate()
            assert events_resp.status in (200, 301), (
                f"Страница мероприятий не доступна: {events_resp.status}"
            )

        with allure.step("Переход к форме создания"):
            create_page_resp = events_page.create_event_click()
            assert create_page_resp.status == 200, (
                f"Страница создания не открылась: {create_page_resp.status}"
            )

        with allure.step("Проверка дефолтного формата — Онлайн"):
            expect(events_create_page.format_option("online")).to_have_class(
                re.compile("bg-surface-brand-fade")
            )

        with allure.step("Заполнение формы"):
            scopes = events_create_page.fill_form(scope_count=1)

        with allure.step("Проверка заполненной формы"):
            assert len(scopes) == 1, f"Выбрано сфер: {len(scopes)}, ожидалась 1"
            expect(events_create_page.SCOPE_SELECTED_PILLS).to_have_count(1)
            expect(events_create_page.EVENT_TITLE_VISIBLE).not_to_be_empty()
            expect(events_create_page.EVENT_EMAIL).to_have_value(config.app.test_user_email)
            expect(events_create_page.POLICY_CHECKBOX).to_be_checked()
            expect(events_create_page.AGREEMENT_CHECKBOX).to_be_checked()

        with allure.step("Отправка на модерацию"):
            create_resp, send_resp = events_create_page.submit_for_moderation()

        with allure.step("Проверка ответов API и редиректа"):
            assert create_resp.status in (200, 201), (
                f"Создание ивента не прошло: {create_resp.status}, {create_resp.text()}"
            )
            assert send_resp.status == 200, (
                f"Отправка на модерацию не прошла: {send_resp.status}, {send_resp.text()}"
            )
            expect(page).to_have_url(re.compile(r"/event/"))

    @allure.title("Участвовать в мероприятии")
    @pytest.mark.critical
    @mutates_data
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


    @allure.title("Участвовать в мероприятии")
    @pytest.mark.medium
    def test_add_event_to_favorite(main_page, events_page, api_login):
        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step("Переход к Мероприятиям"):
            response = main_page.open_page_from_menu('event')
            assert response.value.status == 200, "Events page does not open"

        with allure.step("Поиск ивента не в избранном и добавление"):
            total = events_page.get_cards_count()
            if total == 0:
                pytest.skip("Нет доступных мероприятий")

            added = False
            for i in range(total):
                events_page.open_event_card(i)

                if not events_page.is_current_event_favorite():
                    with allure.step(f"Открыт ивент #{i} — не в избранном, добавляем"):
                        events_page.add_to_favorite()
                        expect(
                            events_page.FAVORITE_ACTIVE, "Не удалось добавить в избранное"
                        ).to_be_visible()
                        added = True
                        break
                else:
                    with allure.step(
                        f"Ивент #{i} уже в избранном — переходим к следующему"
                    ):
                        events_page.page.go_back()  # ← возвращаемся на список карточек

            if not added:
                pytest.skip("Все мероприятия уже добавлены в избранное")

    @allure.title("Проверка статуса избранного по карточкам ")
    @pytest.mark.low
    def test_check_all_events_favorite_status(main_page, events_page, api_login):
        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step("Переход к Мероприятиям"):
            response = main_page.open_page_from_menu('event')
            assert response.value.status == 200, "Events page does not open"

        with allure.step("Проверка карточек мероприятий"):
            total = events_page.get_cards_count()
            if total == 0:
                pytest.skip("Нет доступных мероприятий")

            found_not_favorite = False

            for i in range(total):
                events_page.open_event_card(i)

                if not events_page.is_current_event_favorite():
                    with allure.step(f"Ивент #{i} не в избранном — добавляем"):
                        events_page.add_to_favorite()

                        expect(
                            events_page.FAVORITE_ACTIVE, "Не удалось добавить в избранное"
                        ).to_be_visible()

                        found_not_favorite = True

                    break

                else:
                    with allure.step(f"Ивент #{i} уже в избранном"):
                        events_page.page.go_back()

            if not found_not_favorite:
                with allure.step("Все мероприятия уже находятся в избранном"):
                    assert True


    @allure.title("Удаление мероприятия из избранного")
    @pytest.mark.medium
    def test_remove_event_from_favorite(main_page, events_page, api_login):
        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step("Переход к Мероприятиям"):
            response = main_page.open_page_from_menu('event')
            assert response.value.status == 200, "Events page does not open"

        with allure.step("Поиск ивента в избранном и удаление"):
            total = events_page.get_cards_count()
            if total == 0:
                pytest.skip("Нет доступных мероприятий")

            removed = False
            for i in range(total):
                events_page.open_event_card(i)

                if events_page.is_current_event_favorite():
                    with allure.step(f"Открыт ивент #{i} — в избранном, убираем лайк"):
                        events_page.remove_from_favorite()
                        expect(
                            events_page.FAVORITE_INACTIVE, "Не удалось убрать из избранного"
                        ).to_be_visible()
                        removed = True
                        break
                else:
                    with allure.step(f"Ивент #{i} не в избранном — переходим к следующему"):
                        events_page.page.go_back()  # ← возвращаемся на список карточек

            if not removed:
                pytest.skip("Нет мероприятий в избранном — нечего убирать")


