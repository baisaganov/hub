import allure
import pytest
from config import config
from playwright.sync_api import Page

from pages.auth_page import AuthPage

@allure.suite("Vacancy")
@allure.label("level", "UI")
@pytest.mark.vacancy
@pytest.mark.ui
class TestVacancy:

    @allure.title("Добавление вакансии в избранное")
    @pytest.mark.critical
    def test_add_vacancy_to_favorite(
       self, auth_page: AuthPage, main_page, vacancy_page, base_user_creds
    ):
        with allure.step("Авторизация"):
            auth_page.email_auth(
                base_user_creds["email"], password=base_user_creds["password"]
            )
            main_page.page.keyboard.press("Escape")
        with allure.step("Переход к Вакансиям"):
             with main_page.page.expect_response("**/vacancy/") as response:
                main_page.page.keyboard.press("Escape")
                main_page.VACANCY_LINK.click()
                try:
                    main_page.VACANCY_LINK.click()
                except:
                    pass

        assert response.value.status == 200, "Event Page does not open"
        with allure.step("Добавление вакансии в избранное"):
            vacancy_page.add_vacancy_to_favorites()
            
            
            




            

            