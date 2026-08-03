from playwright.sync_api import expect
from pages.base import BasePage


from playwright.sync_api._generated import Locator



class VacancyPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.VACANCY_LINK = page.locator("#main-top").get_by_role(
            "link",
            name="Вакансии",
            exact=True,
        )

        self.VACANCY_CARD_LIST: Locator = self.page.locator("div.card-item")

    def open_vacancy_from_menu(self):
        """Переход к вакансиям через меню. :return: ответ страницы — статус проверяется в тесте"""
        expect(self.VACANCY_LINK).to_be_visible()

        with self.page.expect_response("**/ru/vacancy/") as response:
            self.VACANCY_LINK.click()
        # expect_response срабатывает по заголовкам ответа — дожидаемся самой навигации
        self.page.wait_for_url("**/vacancy/")

        return response.value

    def get_cards_count(self) -> int:
        # count() не умеет авто-ждать — сначала дожидаемся отрисовки карточек
        expect(self.VACANCY_CARD_LIST.first).to_be_visible()
        return self.VACANCY_CARD_LIST.count()

    def favorite_icon(self, card_number: int) -> Locator:
        """Иконка лайка в карточке (для проверок в тесте: fill=#CC2243 — в избранном)"""
        return self.VACANCY_CARD_LIST.nth(card_number).locator("svg path")

    def is_vacancy_liked(self, card_number: int) -> bool:
        return self.favorite_icon(card_number).get_attribute("fill") == "#CC2243"

    def add_vacancy_to_favorites(self, card_number: int) -> Locator:
        """
        Клик по лайку в карточке вакансии
        :return: локатор кнопки лайка — состояние (заливка иконки) проверяется в тесте
        """
        favorite_btn: Locator = self.VACANCY_CARD_LIST.nth(card_number).locator("svg")
        favorite_btn.click()

        return favorite_btn
