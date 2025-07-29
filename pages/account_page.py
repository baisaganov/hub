from playwright.sync_api import Page

from commons.types import ServiceType
from pages.base_page import BasePage
from services.egov.sign_service import SignXml


class AccountPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.connect_ecp_btn = self.page.locator('div.card-verification > button.btn')

    def connect_ecp(self, user_id):
        """
        Привязка ЭЦП к аккаунту
        :param user_id:
        :return:
        """
        # admin = AdminPage()
        # data = {'iin': '990315351258'}
        # admin.change_user('iin', data=data, user_id=user_id, functinonality=AdminFuncTypes.CLEAR)
        url = self.config['account']['settings_url']

        with self.page.expect_response('https://dev.astanahub.com/account/settings/') as resp:
            self.logging.info(f'Account: Переход на страницу настркойки аккаунта')
            self.page.goto(url)

        if resp.value.status != 200:
            return self.error_response(status=resp.value.status,
                                       service=ServiceType.ACCOUNT,
                                       error_text='Ошибка при переходе в настройки')

        with self.page.expect_response('https://dev.astanahub.com/account/api/login/signature/xml/') as resp:
            self.logging.info(f'Account: Начали процедуру привязки')
            self.connect_ecp_btn.click()

        if resp.value.status != 200:
            return self.error_response(status=resp.value.status,
                                       service=ServiceType.ACCOUNT,
                                       error_text='Ошибка при вызове подписи')

        with self.page.expect_response('https://dev.astanahub.com/account/api/user/verify/') as resp:
            SignXml().sign_xml()

        if resp.value.status != 200:
            return self.error_response(status=resp.value.status,
                                       service=ServiceType.ACCOUNT,
                                       error_text=f'Ошибка при подписании {resp.value.json()}')

        return {'response': resp.value.status, 'msg': 'ЭЦП успешно привязался'}

