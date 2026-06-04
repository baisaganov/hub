import random

from playwright.sync_api import expect, Page, Locator
from pages.base import BasePage
import random
import json


class VacancyCreatePostPage(BasePage):
    def __init__(self,page):
        self.page: Page = page
        self.DROPDOWN_PUBLISH = page.locator('div[x-data="dropdown()"] div[aria-controls="dropdown-panel-4"]')
        self.DROPDOWN_VACANCY_ITEM = page.locator("#dropdown-panel-6 > a[href*='/account/vacancy/']")

        # ============ forma vacancy
        self.FORM = self.page.locator("div[x-show='!loader']")
        self.SELECT_COMPANY = self.FORM.locator('select[x-model="form.company"]')
        self.EMAIL_VACANCY = self.FORM.locator('input[type="email"]')
        self.NAME_VACANCY = self.FORM.locator('input[x-model="form.title[lang]"]')
        self.SELECT_DIRECTION = self.FORM.locator('select[x-model="form.direction"]')
        self.MAIN_REQUIR = self.FORM.locator('#editorRU div.ce-paragraph')
        self.WHAT_W_DO = self.FORM.locator('#responsibilitiesEditorRU div.ce-paragraph'  )
        self.WHAT_W_OFFER = self.FORM.locator('#benefitsEditorRU div.ce-paragraph')
        self.EDUCATION_LVL = self.FORM.locator('select[x-model="form.education"]')
        self.WORK_EXPERIENCE = self.FORM.locator('select[x-model="form.experience"]')
        self.SALARY_FROM = self.FORM.locator('input[placeholder="from"]')
        self.SALARY_TO = self.FORM.locator('input[placeholder="to"]')
        self.JOB_TYPE = self.FORM.locator('button.btn-medium')
        self.JOB_TYPE_LIST = self.page.locator('div[x-show="open"]:visible li')
        self.TYPE_EMPLOYMENT = self.FORM.locator('select[x-model="form.vacancy_type"]')
        self.CITY = self.FORM.locator('select[x-model="form.region"]')

        self.PUBLICATION_POLICY_CHECKBOX: Locator = self.page.locator('input#publication_policy_accepted')
        self.AGREEMENT_CHECKBOX = self.page.locator('input[x-model="form.agreement"]')

        self.PUBLISH_BUTTON = self.page.locator(selector="button.btn.btn--primary.w-full")

        self.TRANSLATION_MODAL = self.page.locator('div[x-show="showTranslationModal"]')
        self.TRANSLATE_BUTTON = self.TRANSLATION_MODAL.locator('button.btn--primary')

    def dropdown_click_publish(self):
        expect(self.DROPDOWN_PUBLISH).to_be_visible()
        self.DROPDOWN_PUBLISH.click()
        
    def dropdown_vacancy_item_click(self):
        expect(self.DROPDOWN_VACANCY_ITEM).to_be_visible()

        with self.page.expect_response('**/account/vacancy/create/') as response:
            self.DROPDOWN_VACANCY_ITEM.click()

        assert response.value.status == 200, "не удалось открыть страницу"

    def fill_vacancy(self, email, name, text, number):
        x=self.SELECT_COMPANY.locator("option").nth(1).get_attribute("value")
        self.SELECT_COMPANY.select_option(value=x)

        self.EMAIL_VACANCY.fill(email)
        self.NAME_VACANCY.fill(value=name)

        options = self.SELECT_DIRECTION.locator("option")
        count = options.count()
        random_index = random.randint(1, count - 1)
        random_value = options.nth(random_index).get_attribute("value")
        self.SELECT_DIRECTION.select_option(value=random_value)

        self.MAIN_REQUIR.fill(text)
        self.WHAT_W_DO.fill(text)
        self.WHAT_W_OFFER.fill(text)

        options = self.EDUCATION_LVL.locator("option")
        count = options.count()
        random_index = random.randint(1, count - 1)
        random_value = options.nth(random_index).get_attribute("value")
        self.EDUCATION_LVL.select_option(value=random_value)

        options = self.WORK_EXPERIENCE.locator("option")
        count = options.count()
        random_index = random.randint(1, count - 1)
        random_value = options.nth(random_index).get_attribute("value")
        self.WORK_EXPERIENCE.select_option(value=random_value)

        self.JOB_TYPE.click()

        expect(self.JOB_TYPE_LIST.nth(0)).to_be_visible()

        self.JOB_TYPE_LIST.nth(0).click()
        self.JOB_TYPE_LIST.nth(1).click()

        self.FORM.click(position={"x": 10, "y": 10})

        options = self.TYPE_EMPLOYMENT.locator("option")
        count = options.count()
        random_index = random.randint(1, count - 1)
        random_value = options.nth(random_index).get_attribute("value")
        self.TYPE_EMPLOYMENT.select_option(value=random_value)

        options = self.CITY.locator("option")
        count = options.count()
        random_index = random.randint(1, count - 1)
        random_value = options.nth(random_index).get_attribute("value")
        self.CITY.select_option(value=random_value)

    def click_checkbox(self):
        self.PUBLICATION_POLICY_CHECKBOX.check()
        self.AGREEMENT_CHECKBOX.check()
    
    def publish(self):
        expect(self.PUBLISH_BUTTON).to_be_visible()

        self.PUBLISH_BUTTON.click()


    def translate(self):

        with self.page.expect_response("**/translate/") as translation:
            self.TRANSLATE_BUTTON.click()

        response = translation.value
        assert response.status == 200, "Не перевелось, переделывай"
            

        





         

        




                                     







    