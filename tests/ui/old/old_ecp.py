from playwright.sync_api import Page

import allure
import pytest

class TestECP:
    @allure.title("Подача заявки ")
    def test_accreditation_renewal_fl(self, page: Page, auth_page, ecp_page):
        with allure.step("Авторизация"):
            auth_page.navigate()
            auth_page.input_email_or_phone(value="a.baisaganov@astanahub.com")
            auth_page.click_auth_email_continue_btn()
            auth_page.input_password(password="Pass1234!")
            auth_page.click_auth_password_continue_btn()


        with allure.step("Переход к заявке"):
            # page.pause()
            ecp_page.click_sign()
            # page.pause()
