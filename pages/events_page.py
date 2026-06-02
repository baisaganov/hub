import random
from operator import truediv
from xml.sax.xmlreader import Locator

from playwright.sync_api import Page, expect

from pages.base import BasePage


class EventsPage(BasePage):
    def __init__(self, page):
        self.page = page

        self.EVENT_CARD = page.locator("div.event-card")
        self.PARTICIPATE_BTN = page.locator("#participate-button")
        self.MODAL_EVENT = page.locator(
            "#ParticipationRequestModal #event-modal__container"
        )

        # Все локаторы формы — внутри модалки!
        self.FULL_NAME = self.MODAL_EVENT.locator("input[name=full_name]")
        self.EMAIL = self.MODAL_EVENT.locator("input[name=email]")
        self.ROLE = self.MODAL_EVENT.locator("select[name=role]")
        self.AGREEMENT_CHECKBOX = self.MODAL_EVENT.locator("input[name='agreement']")
        self.submit_button = self.MODAL_EVENT.locator("button[type=submit]")

        # Добавление в избранное
        self.FAVORITE_BTN = page.locator("div.favoriteEvent")
        self.FAVORITE_ACTIVE = page.locator("div.favoriteEvent span.liked-icon")
        self.FAVORITE_INACTIVE = page.locator("div.favoriteEvent span.unliked-icon")

    def open_event_card(self, card_number: int = None):
        if card_number is None:
            x = self.EVENT_CARD.all()
            card_number = random.randint(0, len(x) - 1)
            print(x)
            print(card_number)
        self.EVENT_CARD.nth(card_number).click()

    def click_participate_btn(self):
        self.PARTICIPATE_BTN.click()
        expect(self.MODAL_EVENT).to_be_visible()

    def checkbox_click(self):
        self.AGREEMENT_CHECKBOX.check(force=True)

    def get_result(self):
        email = self.EMAIL.input_value()
        name = self.FULL_NAME.input_value()
        role = self.ROLE.input_value()
        agreement = self.AGREEMENT_CHECKBOX.is_checked()

        print(email)
        print(name)
        print(role)
        print(agreement)

        return email, name, role, agreement

    def submit_button(self):
        self.submit_button.click(force=True)

    def submit_form(self):
        self.submit_button.click(force=True)

    def get_cards_count(self) -> int:
        return self.EVENT_CARD.count()

    def is_current_event_favorite(self) -> bool:
        return self.FAVORITE_ACTIVE.is_visible()

    def add_to_favorite(self):
        self.FAVORITE_BTN.click()
        expect(self.FAVORITE_ACTIVE).to_be_visible()

    def remove_from_favorite(self):
        self.FAVORITE_BTN.click()
        expect(self.FAVORITE_INACTIVE).to_be_visible()

    def is_favorite_active(self) -> bool:
        return self.FAVORITE_ACTIVE.is_visible()





