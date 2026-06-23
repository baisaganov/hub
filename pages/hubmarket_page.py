from playwright.sync_api import expect

from config import config
from pages.base import BasePage
import random

# from tests.conftest import hubmarket_page


class HubmarketPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        # self.HUBMARKET_MENU = page.locator('a[href="/ru/hub-market/"] span.w-5.h-5').nth(1)
        # self.CARD = self.CARD = page.locator('a[href*="/ru/hub-market/c/listing/"]').nth(1)
        # категория
        self.CATEGORIES_BUTTON = page.locator('#hubmarket_tour')
        self.CATEGORY_ITEMS = page.locator('a.hubmarket-category-item')
        self.CARD = page.locator('a[href*="/hub-market/c/listing/"]')
        self.BUY = page.locator('button:has(span:text("Купить"))')

        # Заполнение модалки
        self.NAME = page.locator('input[x-model="$store.checkout.formData.first_name"]')
        self.LASTNAME = page.locator('input[x-model="$store.checkout.formData.last_name"]')
        self.EMAIL = page.locator('input[x-model="$store.checkout.formData.email"]')
        self.PHONE = page.locator('input[x-model="$store.checkout.formData.phone"]')
        #подтверждение заказа
        self.CONFIRM_THE_ORDER = page.locator('aside button[type="button"].btn--primary')
        # заказ подтвержден
        self.ORDER_CONFIRMED = page.locator('h1.text-text-strong')

    def go_to_hubmarket_menu(self):
        url = f"{config.app.app_url}/hub-market/"
        response = self.page.goto(url)
        assert response.status == 200, f"Expected 200, got {response.status}"

    def select_random_category(self):
        self.CATEGORIES_BUTTON.click()

        count = self.CATEGORY_ITEMS.count()
        random_index = random.randint(1, count - 1)

        self.CATEGORY_ITEMS.nth(random_index).click()

    def open_random_card(self):
        count = self.CARD.count()
        random_index = random.randint(0, count - 1)
        self.CARD.nth(random_index).click()

    def go_to_buy(self):
        self.BUY.click()

    def verify_contact_fields_filled(self, name, lastname, email, phone):
        if self.NAME.input_value() == "" and self.NAME.is_enabled():
            self.NAME.fill(name)
        if self.LASTNAME.input_value() == "" and self.NAME.is_enabled():
            self.LASTNAME.fill(lastname)
        if self.EMAIL.input_value() == "" and self.NAME.is_enabled():
            self.EMAIL.fill(email)
        if self.PHONE.input_value() == "" and self.NAME.is_enabled():
            self.PHONE.fill(phone)


        expect(self.NAME).not_to_be_empty()
        expect(self.LASTNAME).not_to_be_empty()
        expect(self.EMAIL).not_to_be_empty()
        expect(self.PHONE).not_to_be_empty()

    def click_confirm(self, expected_status=200):
        with self.page.expect_response('**s/marketplace/api/order/create_v2/') as response_info:
            self.CONFIRM_THE_ORDER.click()
        response = response_info.value
        assert response.status == expected_status, f"Expected {expected_status}, got {response.status}"


    def order_confirmed(self):
        expect(self.ORDER_CONFIRMED).to_be_visible()

