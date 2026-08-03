from pages.base import BasePage
from playwright.sync_api import expect


class UserProfilePage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self._NTRO_DIALOG = self.page.locator('div.tg-dialog')
        self._INTRO_DIALOG_FINISH = self._NTRO_DIALOG.locator('button')

        self._CREATE_COMPANY_BTN = self.page.locator("div:not([class]) > a.btn > img")

    def close_intro(self):

        if self._NTRO_DIALOG.is_visible():
            self._INTRO_DIALOG_FINISH.click()

    def create_company(self):
        """
        Поиск и клик на странице профайла кнопки Добавить компанию
        :return: ответ страницы создания компании — статус проверяется в тесте
        """
        expect(self._CREATE_COMPANY_BTN).to_be_visible()

        with self.page.expect_response('**/account/v2/company/profile/create/') as response:
            self._CREATE_COMPANY_BTN.click()

        return response.value



