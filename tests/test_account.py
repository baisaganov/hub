import configparser
import pytest
import allure
from os import getenv
from dotenv import load_dotenv, find_dotenv

from commons.types import AdminFuncTypes, AdminAccountChangeType


@allure.suite("Account")
class TestAccount:
    config = configparser.ConfigParser()
    config.read('CONFIG')
    load_dotenv(find_dotenv())
    USERNAME = getenv("AUTH_LOGIN")
    PASSWORD = getenv("AUTH_PASSWORD")

    @allure.title("Привязка ИИН")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "email, password",
        [
            (USERNAME, PASSWORD)
        ],
        ids=["Успешное Добавление ИИН",]
    )
    @pytest.mark.skip('ЭЦП')
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
