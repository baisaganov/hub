import allure
import pytest

from playwright.sync_api import expect


@allure.suite("Vacancy")
@allure.label("level", "UI")
@pytest.mark.vacancy
@pytest.mark.ui
@allure.label("owner", "aliwka")
class TestVacancy:

    @allure.title("Добавление вакансии в избранное")
    @pytest.mark.critical
    def test_add_vacancy_to_favorite(self, main_page, vacancy_page, api_login):
        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step("Переход к Вакансиям"):
            vacancy_resp = vacancy_page.open_vacancy_from_menu()
            assert vacancy_resp.status == 200, (
                f"Страница вакансий не открылась: {vacancy_resp.status}"
            )

        with allure.step("Добавление вакансии в избранное"):
            cards_count = vacancy_page.get_cards_count()
            if cards_count == 0:
                pytest.skip("Нет доступных вакансий")

            for i in range(cards_count):
                if vacancy_page.is_vacancy_liked(i):
                    continue

                favorite_btn = vacancy_page.add_vacancy_to_favorites(i)
                expect(favorite_btn.locator("path")).to_have_attribute("fill", "#CC2243")
                break
            else:
                pytest.skip("Все вакансии уже в избранном")
            
            
            




            

            