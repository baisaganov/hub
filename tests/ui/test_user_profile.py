import pytest
from playwright.sync_api import Page
from config import config
import allure


@allure.suite("User Profile")
@allure.label("level", "UI")
@pytest.mark.ui
class TestUserProfile:

    @allure.title("Добавление компании")
    @pytest.mark.regression
    def test_create_company(
        self,
        auth_page,
        main_page,
        user_profile_page,
        company_profile_page,
        registration_user_creds,
        base_user_creds,
    ):
        env = config.app.env
        company_name = registration_user_creds.get("company_name") 

        with allure.step("Авторизация на портале c Базового пользователя"):
            auth_page.email_auth(base_user_creds["email"], base_user_creds["password"])

        with allure.step("Переход к профилю"):
            main_page.open_user_profile()

        with allure.step("Закрытие интро окна"):
            user_profile_page.close_intro()

        with allure.step("Переход к форме добавления компании"):
            user_profile_page.create_company()

        with allure.step("Ввод наименования компании"):
            company_profile_page.input_company_name(company_name)
            company_profile_page.add_company_btn_clk()
            company_profile_page.modal_discard_ecp()

        with allure.step("Заполнение информации о компании и создание"):
            company_profile_page.fill_company_info(company_name)
