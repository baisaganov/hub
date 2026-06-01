from playwright.sync_api import expect
from pages.base import BasePage


class HubMarketPage(BasePage):
    def __init__(self, page):
        self.page = page
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
    def click_favorite_in_card(self, card_number: int):
        card = self.POPULAR_CARDS.nth(card_number)
        expect(card).to_be_visible()

        favorite = card.locator("[x-data^='listingLikes']").first
        expect(favorite).to_be_visible()

        liked_svg = favorite.locator("svg[x-show='liked']")

        if liked_svg.is_visible():
            return False

        favorite.click()
        expect(liked_svg).to_be_visible()

        return True

    def add_first_available_favorite(self):
        cards_count = self.POPULAR_CARDS.count()

        if cards_count == 0:
            raise AssertionError("Карточки не найдены")

        for i in range(cards_count):
            result = self.click_favorite_in_card(i)

            if result is True:
                return

        raise AssertionError("Все карточки уже добавлены в избранное")