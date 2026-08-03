import allure
import pytest

from pages.vacancy.vacancy_page import VacancyPage

@allure.suite("Vacancy")
@allure.label("level", "UI")
@pytest.mark.vacancy
@pytest.mark.ui
class TestVacancy:
    @allure.title("Vacancy")
    @pytest.mark.critical

    def test_vacancy_create_post_page(
        self,
        main_page,
        vacancy_page: VacancyPage,
        base_user_creds,
        vacancy_create_post_page,
        api_login,
    ):
         with allure.step("Авторизация через API и открытие главной"):
            main_page.navigate()

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

             