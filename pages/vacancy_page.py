from playwright.sync_api import expect
from pages.base import BasePage
import random

import allure
import playwright._impl._errors

from playwright.sync_api import Page, expect
from playwright.sync_api._generated import Locator

from pages.base import BasePage
import random


class VacancyPage(BasePage):
    def __init__(self, page):
        self.page = page

        self.VACANCY_LINK = page.locator("#main-top").get_by_role(
            "link",
            name="Вакансии",
            exact=True,
        )
    def open_vacancy_from_menu(self):
       expect(self.VACANCY_LINK).to_be_visible()
       
       with self.page.expect_response("**/ru/vacancy/") as response:
                  self.VACANCY_LINK.click()
       assert response.value.status == 200, "Страница не открылась"
        # VACANCY LIST
       self.VACANCY_CARD_LIST: Locator = self.page.locator("div.card-item.gap-3.cursor-pointer.w-full.vacancy-item")

    def add_vacancy_to_favorites(self, card_number: int = None):
        if card_number is None:
            card = self.VACANCY_CARD_LIST.nth(
                random.randint(0, self.VACANCY_CARD_LIST.count() - 1)
            )
        else:
            card = self.VACANCY_CARD_LIST.nth(card_number)

        favorite_btn: Locator = card.locator("svg")
        favorite_btn.click()

        expect(favorite_btn.locator("path")).to_have_attribute("fill", "#CC2243")
