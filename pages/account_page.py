from playwright.sync_api import Page

from commons.types import ServiceType
from base.base_page import BasePage

from config.links import Links
# from services.egov.sign_service import SignXml


class AccountPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.connect_ecp_btn = self.page.locator('div.card-verification > button.btn')

    def connect_ecp(self):
        """
        Привязка ЭЦП к аккаунту
        :return:
        """
        # admin = AdminPage()
        # data = {'iin': '990315351258'}
        # admin.change_user('iin', data=data, user_id=user_id, functinonality=AdminFuncTypes.CLEAR)
        url = Links.ACCOUNT_SETTING

        with self.page.expect_response('https://dev.astanahub.com/account/settings/') as resp:
            self.logging.info(f'AccountPage: Переход на страницу настркойки аккаунта')
            self.page.goto(url)

        assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                         msg='AccountPage: Ошибка при переходе в настройки')

        with self.page.expect_response('https://dev.astanahub.com/account/api/login/signature/xml/') as resp:
            self.logging.info(f'AccountPage: Начали процедуру привязки')
            self.connect_ecp_btn.click()

        assert resp.value.status == 200, self.error_info(msg='AccountPage: Ошибка при вызове подписи',
                                                         status=resp.value.status)

        with self.page.expect_response('https://dev.astanahub.com/account/api/user/verify/') as resp:
            SignXml().sign_xml()

        assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                         msg=f'AccountPage: Ошибка при подписании {resp.value.json()}')
