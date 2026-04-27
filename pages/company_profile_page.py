from playwright.sync_api import expect

from pages.base import BasePage


class CompanyProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self._COMPANY_NAME_INPUT = self._page.locator("input[type=text].text-input")
        self._COMPANY_ADD_BTN = self._page.locator("button[x-show=addCompanyBtn]")

        self._ADD_NEW_COMPANY_MODAL = self._page.locator("div[x-show=showAddCompanyModal].relative")
        self._WITHOUT_ECP_BTN = self._ADD_NEW_COMPANY_MODAL.locator("a")

    # =========================== NEW COMPANY FORM =======================================
        self._COMPANY_INFO_FORM = self._page.locator("main form")
        self._COMPANY_INFO_NAME = self._COMPANY_INFO_FORM.get_by_placeholder('Fill in company name')
        self._COMPANY_INFO_LEGAL_NAME = self._COMPANY_INFO_FORM.get_by_placeholder('Fill in legal company name')
        self._COMPANY_INFO_BUTTON = self._COMPANY_INFO_FORM.locator('button')

    def input_company_name(self, name):
        """Ввод наименования компании"""
        expect(self._COMPANY_NAME_INPUT).to_be_visible()
        expect(self._COMPANY_NAME_INPUT).to_be_editable()

        self._COMPANY_NAME_INPUT.fill(name)

    def add_company_btn_clk(self):
        """Клик по кнопке Добавить компанию"""
        expect(self._COMPANY_ADD_BTN).to_be_visible()
        expect(self._COMPANY_ADD_BTN).to_be_enabled()

        self._COMPANY_ADD_BTN.click()

    def modal_discard_ecp(self):
        expect(self._ADD_NEW_COMPANY_MODAL).to_be_visible()
        expect(self._WITHOUT_ECP_BTN).to_be_visible()
        expect(self._WITHOUT_ECP_BTN).to_be_enabled()

        self._WITHOUT_ECP_BTN.click()

    def fill_company_info(self, company_name):
        expect(self._COMPANY_INFO_FORM).to_be_visible()
        expect(self._COMPANY_INFO_NAME).to_be_editable()
        expect(self._COMPANY_INFO_LEGAL_NAME).to_be_editable()
        expect(self._COMPANY_INFO_BUTTON).to_be_enabled()

        self._COMPANY_INFO_NAME.fill(company_name)
        self._COMPANY_INFO_LEGAL_NAME.fill(company_name)

        with self._page.expect_response('**/account/api/company_api/') as response:
            self._COMPANY_INFO_BUTTON.click()

        assert response.value.status == 200, (f'CompanyProfilePage: Компания не была создана {response.value.status} \n'
                                              f'{response.value.json()}')