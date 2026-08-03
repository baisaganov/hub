from playwright.sync_api import expect, Locator

from pages.base import BasePage


class HubMarketPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.POPULAR_TITLE = page.get_by_text("Популярные услуги и товары", exact=True)
        self.POPULAR_BLOCK = self.POPULAR_TITLE.locator("xpath=ancestor::div[1]")
        self.POPULAR_CARDS = self.POPULAR_BLOCK.locator("div.card-item")

    def open_hub_market_from_menu(self):
        hub_market_link = self.page.locator("#main-top").get_by_role(
            "link",
            name="Hub Market",
            exact=True,
        )

        expect(hub_market_link).to_be_visible()
        hub_market_link.click()

        self.page.wait_for_url("**/ru/hub-market/")
        expect(self.POPULAR_TITLE).to_be_visible()

    def get_cards_count(self) -> int:
        return self.POPULAR_CARDS.count()

    def card(self, card_number: int) -> Locator:
        return self.POPULAR_CARDS.nth(card_number)

    def liked_icon(self, card_number: int) -> Locator:
        """Иконка активного лайка в карточке (для проверок в тесте)"""
        favorite = self.card(card_number).locator("[x-data^='listingLikes']").first
        return favorite.locator("svg[x-show='liked']")

    def is_card_liked(self, card_number: int) -> bool:
        return self.liked_icon(card_number).is_visible()

    def like_card(self, card_number: int):
        """
        Клик по лайку в карточке
        :return: ответ product_like — статус проверяется в тесте
        """
        card = self.card(card_number)
        expect(card).to_be_visible()

        favorite = card.locator("[x-data^='listingLikes']").first
        expect(favorite).to_be_visible()

        with self.page.expect_response("**/product_like/**/like/") as response_info:
            favorite.click()

        return response_info.value
