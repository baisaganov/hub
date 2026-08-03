import allure
import pytest

from playwright.sync_api import expect


@allure.suite("Hub Market")
@allure.label("level", "UI")
@pytest.mark.ui
@pytest.mark.hubmarket
@allure.label("owner", "aliwka")
class TestHubMarket:

    @allure.title("Добавление популярного листинга в избранное")
    @pytest.mark.regression
    def test_add_popular_listing_to_favorite(
        self,
        main_page,
        hubmarket_page,
        api_login,
    ):
        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step("Переход на страницу Hub Market"):
            hubmarket_page.open_hub_market_from_menu()

        with allure.step("Добавление первого доступного популярного листинга в избранное"):
            cards_count = hubmarket_page.get_cards_count()
            if cards_count == 0:
                pytest.skip("Карточки не найдены")

            for i in range(cards_count):
                if hubmarket_page.is_card_liked(i):
                    continue

                like_resp = hubmarket_page.like_card(i)
                assert like_resp.status == 200, (
                    f"Лайк не поставился: {like_resp.status}"
                )
                expect(hubmarket_page.liked_icon(i)).to_be_visible()
                break
            else:
                pytest.skip("Все карточки уже добавлены в избранное")
