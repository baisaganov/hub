import allure
import page
import pytest
from playwright.sync_api import Page
from pages.auth_page import AuthPage



@allure.suite("Hubmarket")
class TestHubmarket:
    @allure.title("Покупка в Хабмаркете")
    def test_hubmarket_buy(self, page, auth_page: AuthPage, base_user_creds, hubmarket_page):
        with allure.step("Авторизация"):
            auth_page.email_auth(base_user_creds['email'], password=base_user_creds['password'])
            page.keyboard.press("Escape")

        with allure.step("Переход в Хабмаркет"):
            hubmarket_page.go_to_hubmarket_menu()

        with allure.step("Выбор случайной категории"):
            hubmarket_page.select_random_category()
        with allure.step("Открыть случайную карточку товара"):
            hubmarket_page.open_random_card()

        # with allure.step("Открыть карточку"):
        #     hubmarket_page.open_hubmarket_card()

        with allure.step("Кнопка купить"):
            hubmarket_page.go_to_buy()

        # with allure.step("Заполните данные"):
        #     hubmarket_page.write_your_data(
        #         name="Madina",
        #         lastname="Zeinolla",
        #         phone="+77712717305"
        #     )

        with allure.step("Проверка, что контактные данные заполнены автоматически"):
            hubmarket_page.verify_contact_fields_filled(
                name='Madina',
                lastname='Zeinolla',
                email='madina@test.com',
                phone='+77001234567'
            )

        with allure.step("Подтвердите заказ"):
            hubmarket_page.click_confirm()

        with allure.step("Успешный заказ"):
            hubmarket_page.order_confirmed()

        page.pause()
