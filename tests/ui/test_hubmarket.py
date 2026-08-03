import allure
import pytest


@allure.suite("Hub Market")
@allure.label("level", "UI")
@pytest.mark.ui
@pytest.mark.hubmarket
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
            main_page.navigate()

        with allure.step("Переход на страницу Hub Market"):
            hubmarket_page.open_hub_market_from_menu()

        with allure.step("Добавление первого доступного популярного листинга в избранное"):
            hubmarket_page.add_first_available_favorite()