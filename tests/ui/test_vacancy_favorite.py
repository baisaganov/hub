import allure
import pytest


@allure.suite("Vacancy")
@allure.label("level", "UI")
@pytest.mark.vacancy
@pytest.mark.ui
class TestVacancy:

    @allure.title("Добавление вакансии в избранное")
    @pytest.mark.critical
    def test_add_vacancy_to_favorite(self, main_page, vacancy_page, api_login):
        with allure.step("Авторизация через API и открытие главной"):
            main_page.navigate()

        with allure.step("Переход к Вакансиям"):
            vacancy_page.open_vacancy_from_menu()
        with allure.step("Добавление вакансии в избранное"):
            vacancy_page.add_vacancy_to_favorites()
            
            
            




            

            