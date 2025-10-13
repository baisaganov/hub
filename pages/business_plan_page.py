from base.base_page import BasePage
from config.links import Links


class BusinessPlanPage(BasePage):
    link = Links.BP

    def __init__(self, page):
        super().__init__(page)
        self.company_select = self.page.locator('select.company')

    def get_company_list(self):
        print(self.company_select)

    def select_company(self):
        print(self.company_select.get_attribute('value'))
        self.logging.info(self.company_select.get_attribute('value'))
        self.page.pause()


    def navigate(self):
        self.page.goto(self.link)



