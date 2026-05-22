import random

from playwright.sync_api import expect
from pages.base import BasePage


class EventsPage(BasePage):
    def __init__(self, page):
        self.page = page

        self.EVENT_CARD = page.locator("div.event-card")

        self.PARTICIPATE_BTN = page.locator("#participate-button")

        self.MODAL_EVENT = page.locator(
            "#ParticipationRequestModal #event-modal__container"
        )

        self.FULL_NAME = page.locator(
            "#ParticipationRequestModal input[name='full_name']"
        )

        self.EMAIL = page.locator(
            "#ParticipationRequestModal input[name='email']"
        )

        self.CHOOSE_ROLE_EVENT = page.locator(
            "#ParticipationRequestModal select[name='role']"
        )

        self.AGREEMENT_CHECKBOX = page.locator(
            "#ParticipationRequestModal input[name='agreement']"
        )

        self.AGREEMENT_CHECKBOX_LABEL = page.locator(
            "#ParticipationRequestModal #event-label-checkbox-2 label"
        )

        self.SUBMIT_PARTICIPATE_BTN = page.locator(
            "#ParticipationRequestModal button[type='submit']"
        )

    def open_event_card(self, card_number: int):
        expect(self.EVENT_CARD.nth(card_number)).to_be_visible()
        self.EVENT_CARD.nth(card_number).click()

    def click_participate_btn(self):
        expect(self.PARTICIPATE_BTN).to_be_visible()
        expect(self.PARTICIPATE_BTN).to_be_enabled()

        self.PARTICIPATE_BTN.click()

        expect(self.MODAL_EVENT).to_be_visible()

    def choose_random_role_event(self):
        expect(self.CHOOSE_ROLE_EVENT).to_be_visible()

        options = self.CHOOSE_ROLE_EVENT.locator("option")
        roles = []

        for i in range(options.count()):
            option = options.nth(i)
            value = option.get_attribute("value")
            text = option.inner_text().strip()

            if value and text != "Выберите":
                roles.append(value)

        if not roles:
            raise Exception("Список ролей пустой")

        random_role = random.choice(roles)

        self.CHOOSE_ROLE_EVENT.select_option(value=random_role)
        expect(self.CHOOSE_ROLE_EVENT).to_have_value(random_role)

        return random_role

    def checkbox_click(self):
        expect(self.AGREEMENT_CHECKBOX).to_be_attached()

        self.AGREEMENT_CHECKBOX_LABEL.scroll_into_view_if_needed()
        self.AGREEMENT_CHECKBOX_LABEL.click()

        if not self.AGREEMENT_CHECKBOX.is_checked():
            self.AGREEMENT_CHECKBOX.set_checked(True, force=True)

        expect(self.AGREEMENT_CHECKBOX).to_be_checked()

    def submit_participation_form(self):
        expect(self.SUBMIT_PARTICIPATE_BTN).to_be_visible()
        expect(self.SUBMIT_PARTICIPATE_BTN).to_be_enabled()

        self.SUBMIT_PARTICIPATE_BTN.scroll_into_view_if_needed()
        self.SUBMIT_PARTICIPATE_BTN.click()

    def get_result(self):
        name = self.FULL_NAME.input_value()
        email = self.EMAIL.input_value()

        print(f"ФИО: {name}")
        print(f"Email: {email}")

        return {
            "name": name,
            "email": email,
        }