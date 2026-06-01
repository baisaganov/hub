import allure
import pytest

from pages.auth_page import AuthPage


@allure.suite("Hub Market")
class TestHubMarket:

    @allure.title("Добавление популярного листинга в избранное")
    @pytest.mark.regression
    def test_add_popular_listing_to_favorite(
        self,
        main_page,
        hubmarket_page,
        auth_page: AuthPage,
        base_user_creds,
    ):
        with allure.step("Авторизация"):
            auth_page.email_auth(
                base_user_creds["email"],
                password=base_user_creds["password"],
            )
            main_page.page.keyboard.press("Escape")

        with allure.step("Переход на страницу Hub Market"):
            hubmarket_page.open_hub_market_from_menu()

        with allure.step("Добавление первого доступного популярного листинга в избранное"):
            hubmarket_page.add_first_available_favorite()