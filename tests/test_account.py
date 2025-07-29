import configparser
import pytest
import allure

from commons.types import AdminFuncTypes, AdminAccountChangeType
from pages.account.account import AccountPage
from services.admin_api import AdminAPI
from pages.hub_Id.auth import AuthPage


@allure.suite("Account")
class TestAccount:
    config = configparser.ConfigParser()
    config.read('CONFIG')

    @allure.title("Привязка ИИН")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "email, password",
        [
            ('a.baisaganov@astanahub.com', 'Pass1234!')
        ],
        ids=["Успешное Добавление ИИН",]
    )
    def test_connect_ecp_to_account(self, page, email, password):
        admin = AdminAPI()
        user_id = admin.get_user_id_by_(email)
        resp = admin.change_user(change_mode=AdminAccountChangeType.IIN,
                                 data={'iin': '990315351258'},
                                 user_id=user_id,
                                 functinonality=AdminFuncTypes.CLEAR)

        assert resp['response'] == 200, resp['msg']

        with allure.step('Авторизация с помощью почты'):
            auth = AuthPage(page)
            resp = auth.email_auth(email, password)

            assert resp['response'] == 200, resp['msg']

        with allure.step('Привязка ИИН'):
            account = AccountPage(page)
            resp = account.connect_ecp(user_id=user_id)

            assert resp['response'] == 200, resp['msg']

    @allure.title("Позитивный сценарий тэг НИИ")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "email, password",
        [
            ('a.baisaganov@astanahub.com', 'Pass1234!')
        ],
        ids=["Успешное Добавление НИИ", ]
    )
    def test_tag_nii(self, page, email, password):
        admin = AdminAPI()
        user_id = admin.get_user_id_by_(email)
        resp = admin.change_user(change_mode=AdminAccountChangeType.IIN,
                                 data={'iin': '990315351258'},
                                 user_id=user_id,
                                 functinonality=AdminFuncTypes.CHANGE)

        assert resp['response'] == 200, resp['msg']

        with allure.step('Авторизация с помощью почты'):
            auth = AuthPage(page)
            resp = auth.email_auth(email, password)

            assert resp['response'] == 200, resp['msg']

