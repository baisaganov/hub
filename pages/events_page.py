from operator import le
from urllib import request
from xml.sax.xmlreader import Locator

from playwright.sync_api import Page, expect
from playwright.sync_api._generated import Locator

from pages.base import BasePage
import random
import json


class EventsPage(BasePage):
    def __init__(self, page):
        self.page: Page = page

        self.EVENT_CARD_LIST: Locator = page.locator("div.event-card")
        self.PARTICIPATE_BTN = page.locator("#participate-button")

        # MODAL
        self.MODAL_EVENT = page.locator(
            "#ParticipationRequestModal #event-modal__container"
        )
        self.AGREEMENT_CHECKBOX = self.MODAL_EVENT.locator("span.event-checkbox-text")
        self.FULL_NAME_INPUT = self.MODAL_EVENT.locator("input[name=full_name]")
        self.EMAIL_INPUT: Locator = self.MODAL_EVENT.locator("input[name=email]")
        self.ROLE_SELECT: Locator = self.MODAL_EVENT.locator("select[name=role]")
        self.SEND_FORM = self.MODAL_EVENT.get_by_role("button")

    def open_event_card(self, card_number: int = None):
        if card_number is None:
            self.EVENT_CARD_LIST.nth(
                random.randint(0, self.EVENT_CARD_LIST.count() - 1)
            ).click()
        else:
            self.EVENT_CARD_LIST.nth(card_number).click()
        self.page.wait_for_url("**/event/**", wait_until="domcontentloaded")

    def click_participate_btn(self):
        self.PARTICIPATE_BTN.click()
        expect(self.MODAL_EVENT).to_be_visible()

    def checkbox_click(self):
        self.AGREEMENT_CHECKBOX.check()

    def get_result(self):
        email = self.EMAIL_INPUT.get_attribute("value")
        name = self.FULL_NAME_INPUT.get_attribute("value")
        options_list = self.ROLE_SELECT.locator("option").all()
        option = random.choice(options_list)

        self.ROLE_SELECT.select_option(value=option.get_attribute("value"))

        assert len(email) != 0, "EventsPage: Почта не заполнена"
        assert len(name) != 0, "EventsPage: ФИО не заполнено"

        assert self.ROLE_SELECT.input_value() == option.get_attribute(
            "value"
        ), "EventsPage: Роль не была выбрана"

    def send_form(self):
        with self.page.expect_request("**/account/api/event/participate/") as request:
            self.SEND_FORM.click()

        event_keys = json.loads(request.value.post_data).keys()

        for key in ["event", "full_name", "email", "role", "agreement"]:
            assert (
                key in event_keys
            ), f"EventPage: Ключ {key} не был найден в body запроса {event_keys}"
