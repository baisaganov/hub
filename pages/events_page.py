import random

from playwright.sync_api import Page, expect

from playwright.sync_api import expect
from pages.base import BasePage
import random
from config import config


class EventsPage(BasePage):
    def __init__(self, page):
        self.page: Page = page

        self.EVENT_CARD = page.locator("div.event-card")
        self.PARTICIPATE_BTN = page.locator("#participate-button")
        self.MODAL_EVENT = page.locator(
            "#ParticipationRequestModal #event-modal__container"
        )
        self.CREATE_EVENT_BUTTON = page.locator('a[href^="/account/event/create/"]')

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

    def navigate(self):
        self.page.set_default_timeout(90000)

        with self.page.expect_response(f"**/event/") as resp:
            self.page.goto(
                f"{config.app.app_url}/ru/event/", wait_until="domcontentloaded"
            )

        assert resp.value.status in [
            200,
            301,
        ], f"EventPage: Страница не доступна {resp.value.status}"

        self.page.set_default_timeout(30000)

    def open_event_card(self, card_number: int = None):
        if card_number is None:
            x = self.EVENT_CARD.all()
            card_number = random.randint(0, len(x) - 1)

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

    def create_event_click(self):
        expect(self.CREATE_EVENT_BUTTON).to_be_visible()

        with self.page.expect_response("**/account/event/create/") as response:
            self.CREATE_EVENT_BUTTON.click()

        assert (
            response.value.status == 200
        ), f"EventCreatePage: Страница создания не открылась. Статус: {response.value.status}"
