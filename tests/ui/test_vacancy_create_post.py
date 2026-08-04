import allure
import pytest

from pages.vacancy.vacancy_page import VacancyPage

@allure.suite("Vacancy")
@allure.label("level", "UI")
@pytest.mark.vacancy
@pytest.mark.ui
@allure.label("owner", "aliwka")
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
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

         with allure.step("Вакансии"):
             vacancy_resp = vacancy_page.open_vacancy_from_menu()
             assert vacancy_resp.status == 200, (
                 f"Страница вакансий не открылась: {vacancy_resp.status}"
             )

         with allure.step("Вакансии клик"):
             vacancy_create_post_page.dropdown_click_publish()
             create_page_resp = vacancy_create_post_page.dropdown_vacancy_item_click()
             assert create_page_resp.status == 200, (
                 f"Страница создания вакансии не открылась: {create_page_resp.status}"
             )

         with allure.step("Заполнить поля"):
             vacancy_create_post_page.fill_vacancy(email=base_user_creds["email"], name="Тестовая вакансия", text="Тестовый текст", number="100")

         with allure.step("Checkbox"):
             vacancy_create_post_page.click_checkbox()

         with allure.step("Publish"):
             vacancy_create_post_page.publish()

         with allure.step("Translate"):
             translate_resp = vacancy_create_post_page.translate()
             assert translate_resp.status == 200, (
                 f"Перевод не выполнился: {translate_resp.status}"
             )

             