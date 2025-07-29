import configparser
import pytest
import allure

from commons.types import AdminFuncTypes, AdminAccountChangeType
from pages.account_page import AccountPage
from services.admin_api import AdminAPI
from pages.auth_page import AuthPage


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
    def test_connect_ecp_to_account(self, page, admin, auth_page, account_page, email, password):
        with allure.step('Очищаем у юзера ИИН в базе'):
            user_id = admin.get_user_id_by_(email)
            admin.change_user(change_mode=AdminAccountChangeType.IIN,
                              data={'iin': '990315351258'},
                              user_id=user_id,
                              functinonality=AdminFuncTypes.CLEAR)

        with allure.step('Авторизация с помощью почты'):
            auth_page.email_auth(email, password)

        with allure.step('Привязка ИИН'):
            account_page.connect_ecp()
