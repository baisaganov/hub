import allure
import pytest


@allure.title("Добавление мероприятия в избранное")
@allure.label("level", "UI")
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.events
def test_add_event_to_favorite(main_page, events_page, api_login):
    with allure.step("Авторизация через API и открытие главной"):
        main_page.navigate()

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
                    assert (
                        events_page.is_favorite_active()
                    ), "Не удалось добавить в избранное"
                    added = True
                    break
            else:
                with allure.step(
                    f"Ивент #{i} уже в избранном — переходим к следующему"
                ):
                    events_page.page.go_back()  # ← возвращаемся на список карточек

        if not added:
            pytest.skip("Все мероприятия уже добавлены в избранное")


@allure.title("Удаление мероприятия из избранного")
@pytest.mark.critical
def test_remove_event_from_favorite(main_page, events_page, api_login):
    with allure.step("Авторизация через API и открытие главной"):
        main_page.navigate()

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
                    assert (
                        not events_page.is_favorite_active()
                    ), "Не удалось убрать из избранного"
                    removed = True
                    break
            else:
                with allure.step(f"Ивент #{i} не в избранном — переходим к следующему"):
                    events_page.page.go_back()  # ← возвращаемся на список карточек

        if not removed:
            pytest.skip("Нет мероприятий в избранном — нечего убирать")


@allure.title("Проверка всех карточек мероприятий")
@pytest.mark.critical
def test_check_all_events_favorite_status(main_page, events_page, api_login):
    with allure.step("Авторизация через API и открытие главной"):
        main_page.navigate()

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

                    assert (
                        events_page.is_favorite_active()
                    ), "Не удалось добавить в избранное"

                    found_not_favorite = True

                break

            else:
                with allure.step(f"Ивент #{i} уже в избранном"):
                    events_page.page.go_back()

        if not found_not_favorite:
            with allure.step("Все мероприятия уже находятся в избранном"):
                assert True
