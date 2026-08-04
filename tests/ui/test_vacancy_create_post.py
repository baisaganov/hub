import allure
import pytest
from playwright.sync_api import expect
from config import config


from pages.vacancy.vacancy_page import VacancyPage

mutates_data = pytest.mark.skipif(
    config.is_production(), reason="Мутирует данные — только dev/qa"
)


@allure.suite("Vacancy")
@allure.label("level", "UI")
@pytest.mark.vacancy
@pytest.mark.ui
@allure.label("owner", "aizada")
class TestVacancy:
    @allure.title("Создание вакансии")
    @pytest.mark.critical
    @mutates_data
    def test_vacancy_create(
        self,
        main_page,
        vacancy_page: VacancyPage,
        base_user_creds,
        vacancy_create_post_page,
        api_login,
    ):
        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (
                200,
                301,
            ), f"Главная страница не доступна: {main_resp.status}"

        with allure.step("Вакансии"):
            vacancy_resp = vacancy_page.open_vacancy_from_menu()
            assert (
                vacancy_resp.status == 200
            ), f"Страница вакансий не открылась: {vacancy_resp.status}"

        with allure.step("Вакансии клик"):
            vacancy_create_post_page.dropdown_click_publish()
            create_page_resp = vacancy_create_post_page.dropdown_vacancy_item_click()
            assert (
                create_page_resp.status == 200
            ), f"Страница создания вакансии не открылась: {create_page_resp.status}"

        with allure.step("Заполнить поля"):
            vacancy_create_post_page.fill_vacancy(
                email=base_user_creds["email"],
                name="Тестовая вакансия",
                text="Тестовый текст",
                number="100",
            )

        with allure.step("Checkbox"):
            vacancy_create_post_page.click_checkbox()

        with allure.step("Publish"):
            vacancy_create_post_page.publish()

        with allure.step("Translate"):
            translate_resp = vacancy_create_post_page.translate()
            assert (
                translate_resp.status == 200
            ), f"Перевод не выполнился: {translate_resp.status}"

    @allure.title("Добавление вакансии в избранное")
    @pytest.mark.medium
    def test_add_vacancy_to_favorite(self, main_page, vacancy_page, api_login):
        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (
                200,
                301,
            ), f"Главная страница не доступна: {main_resp.status}"

        with allure.step("Переход к Вакансиям"):
            vacancy_resp = vacancy_page.open_vacancy_from_menu()
            assert (
                vacancy_resp.status == 200
            ), f"Страница вакансий не открылась: {vacancy_resp.status}"

        with allure.step("Добавление вакансии в избранное"):
            cards_count = vacancy_page.get_cards_count()
            if cards_count == 0:
                pytest.skip("Нет доступных вакансий")

            for i in range(cards_count):
                if vacancy_page.is_vacancy_liked(i):
                    continue

                favorite_btn = vacancy_page.add_vacancy_to_favorites(i)
                expect(favorite_btn.locator("path")).to_have_attribute(
                    "fill", "#CC2243"
                )
                break
            else:
                pytest.skip("Все вакансии уже в избранном")
