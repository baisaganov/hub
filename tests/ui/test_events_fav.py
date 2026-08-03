import allure
import pytest

from playwright.sync_api import expect


@allure.suite("Events")
@allure.label("owner", "aliwka")
@allure.title("Добавление мероприятия в избранное")
@allure.label("level", "UI")
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.events
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


@allure.suite("Events")
@allure.label("owner", "aliwka")
@allure.title("Удаление мероприятия из избранного")
@pytest.mark.critical
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


@allure.suite("Events")
@allure.label("owner", "aliwka")
@allure.title("Проверка всех карточек мероприятий")
@pytest.mark.critical
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
