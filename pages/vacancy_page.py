from playwright.sync_api import expect
from pages.base import BasePage


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


           