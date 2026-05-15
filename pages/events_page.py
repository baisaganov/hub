from playwright.sync_api import expect

from pages.base import BasePage


class EventsPage(BasePage):
    def __init__(self, page):
        self.page = page

        self.EVENT_CARD = page.locator('div.event-card')
        self.PARTICIPATE_BTN = page.locator('#participate-button')
        self.MODAL_EVENT = page.locator('#ParticipationRequestModal #event-modal__container')

    def open_event_card(self, card_number: int):
        self.EVENT_CARD.nth(card_number).click()

    def click_participate_btn(self):
        self.PARTICIPATE_BTN.click()
        expect(self.MODAL_EVENT).to_be_visible()


