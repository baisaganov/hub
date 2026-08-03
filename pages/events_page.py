import random

from playwright.sync_api import expect, Locator

from pages.base import BasePage
from config import config


class EventsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.EVENT_CARD = page.locator("div.event-card")
        self.PARTICIPATE_BTN:Locator = page.locator("#participate-button")
        self.PARTICIPATE_SUBMITED = page.locator('div.event-participant-submitted')
        self.MODAL_EVENT = page.locator(
            "#ParticipationRequestModal #event-modal__container"
        )
        self.CREATE_EVENT_BUTTON = page.locator('a[href^="/account/event/create/"]')

        # Все локаторы формы — внутри модалки!
        self.FULL_NAME = self.MODAL_EVENT.locator("input[name=full_name]")
        self.EMAIL: Locator = self.MODAL_EVENT.locator("input[name=email]")
        self.ROLE: Locator = self.MODAL_EVENT.locator("select[name=role]")
        self.AGREEMENT_CHECKBOX = self.MODAL_EVENT.locator("input[name='agreement']")
        self.SUBMIT_BUTTON = self.MODAL_EVENT.locator("button[type=submit]")

        # Добавление в избранное
        self.FAVORITE_BTN = page.locator("div.favoriteEvent")
        self.FAVORITE_ACTIVE = page.locator("div.favoriteEvent span.liked-icon")
        self.FAVORITE_INACTIVE = page.locator("div.favoriteEvent span.unliked-icon")

    def navigate(self):
        """Переход на страницу мероприятий. :return: ответ страницы — статус проверяется в тесте"""
        self.page.set_default_timeout(90000)

        with self.page.expect_response("**/event/") as resp:
            self.page.goto(
                f"{config.app.app_url}/ru/event/", wait_until="domcontentloaded"
            )

        self.page.set_default_timeout(30000)
        return resp.value

    def open_event_card(self, card_number: int = None):
        if card_number is None:
            x = self.EVENT_CARD.all()
            card_number = random.randint(0, len(x) - 1)

        self.EVENT_CARD.nth(card_number).click()

    def click_participate_btn(self) -> bool:
        """
        Клик по кнопке Участвовать.
        :return: False — кнопки нет (например, заявка уже подана), решение о skip принимает тест
        """
        if not self.PARTICIPATE_BTN.is_visible():
            return False

        expect(self.PARTICIPATE_BTN).to_be_enabled()
        self.PARTICIPATE_BTN.click()
        return True

    SUBMITTED_TEXT = {
        'ru': 'Заявка на участие подана',
        'kk': 'Қатысуға өтінім берілді',
        'en': 'Application for participation has been submitted'
    }

    def get_expected_submitted_text(self) -> str:
        """Ожидаемый текст "заявка подана" для текущего языка страницы"""
        return self.SUBMITTED_TEXT[self.get_current_lang(self.page.url)]

    def choose_random_role_event(self):
        expect(self.ROLE).to_be_visible()

        options = self.ROLE.locator("option")
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

        self.ROLE.select_option(value=random_role)

        return random_role

    def checkbox_click(self):
        self.AGREEMENT_CHECKBOX.check(force=True)

    def submit_form(self):
        self.SUBMIT_BUTTON.click(force=True)

    def get_cards_count(self) -> int:
        try:
            self.EVENT_CARD.first.wait_for(state="visible", timeout=5000)
        except Exception:
            pass 
        return self.EVENT_CARD.count()

    def is_current_event_favorite(self) -> bool:
        return self.FAVORITE_ACTIVE.is_visible()

    def add_to_favorite(self):
        """Клик по лайку — результат проверяется в тесте по FAVORITE_ACTIVE"""
        self.FAVORITE_BTN.click()

    def remove_from_favorite(self):
        """Клик по лайку — результат проверяется в тесте по FAVORITE_INACTIVE"""
        self.FAVORITE_BTN.click()

    def is_favorite_active(self) -> bool:
        return self.FAVORITE_ACTIVE.is_visible()

    def create_event_click(self):
        """Клик "Создать мероприятие". :return: ответ страницы создания — статус проверяется в тесте"""
        expect(self.CREATE_EVENT_BUTTON).to_be_visible()

        with self.page.expect_response("**/account/event/create/") as response:
            self.CREATE_EVENT_BUTTON.click()

        return response.value
