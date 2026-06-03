import allure
import pytest

from pages.auth_page import AuthPage
from pages.vacancy_page import VacancyPage

@allure.suite("Vacancy")
@pytest.mark.vacancy
class TestVacancy:
    @allure.title("Vacancy")
    @pytest.mark.critical

    def test_vacancy_create_post_page(
        self,
        main_page,
        vacancy_page: VacancyPage,
        auth_page: AuthPage,
        base_user_creds,
        vacancy_create_post_page
    ):
         with allure.step("Авторизация"):
            auth_page.email_auth(
                base_user_creds["email"],
                password=base_user_creds["password"],
            )
            main_page.page.keyboard.press("Escape")      
    
         with allure.step("Вакансии"):
             vacancy_page.open_vacancy_from_menu()

         with allure.step("Вакансии клик"):
             vacancy_create_post_page.dropdown_click_publish()
             vacancy_create_post_page.dropdown_vacancy_item_click()

         with allure.step("Заполнить поля"):
             vacancy_create_post_page.fill_vacancy(email=base_user_creds["email"], name="Тестовая вакансия", text="Тестовый текст", number="100")

         with allure.step("Checkbox"):
             vacancy_create_post_page.click_checkbox()
        
         with allure.step("Publish"):
             vacancy_create_post_page.publish()

         with allure.step("Translate"):
             vacancy_create_post_page.translate()

             