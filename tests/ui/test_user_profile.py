import pytest
import allure


@allure.suite("User Profile")
@allure.label("level", "UI")
@pytest.mark.ui
@allure.label("owner", "aliwka")
class TestUserProfile:

    @allure.title("Добавление компании")
    @pytest.mark.regression
    def test_create_company(
        self,
        main_page,
        user_profile_page,
        company_profile_page,
        registration_user_creds,
        api_login,
    ):
        company_name = registration_user_creds.get("company_name")

        with allure.step("Авторизация через API и открытие главной"):
            main_resp = main_page.navigate()
            assert main_resp.status in (200, 301), (
                f"Главная страница не доступна: {main_resp.status}"
            )

        with allure.step("Переход к профилю"):
            profile_resp = main_page.open_user_profile()
            assert profile_resp.status == 200, (
                f"Страница профиля не открылась: {profile_resp.status}"
            )

        with allure.step("Закрытие интро окна"):
            user_profile_page.close_intro()

        with allure.step("Переход к форме добавления компании"):
            create_page_resp = user_profile_page.create_company()
            assert create_page_resp.status == 200, (
                f"Форма добавления компании не открылась: {create_page_resp.status}"
            )

        with allure.step("Ввод наименования компании"):
            company_profile_page.input_company_name(company_name)
            company_profile_page.add_company_btn_clk()
            company_profile_page.modal_discard_ecp()

        with allure.step("Заполнение информации о компании и создание"):
            company_resp = company_profile_page.fill_company_info(company_name)
            assert company_resp.status == 200, (
                f"Компания не была создана: {company_resp.status}, {company_resp.text()}"
            )
