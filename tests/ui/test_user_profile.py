import pytest
from playwright.sync_api import Page
from config import config
import allure


@allure.suite('User Profile')
@pytest.mark.order(2)
class TestUserProfile:

    @allure.title('Добавление компании')
    @pytest.mark.regression
    @pytest.mark.parametrize('env', ['qa', 'dev'])
    def test_create_company(self, env, auth_page, main_page, user_profile_page, company_profile_page,
                            registration_user_creds, base_user_creds):
        config.app.subdomain = env
        config.app.update_app_url()

        company_name = registration_user_creds.get('company_name')

        if auth_page.is_context_exists(env=env):
            with allure.step('Переход на главную старницу'):
                main_page.navigate()

            with allure.step('Загрузка юзера'):
                auth_page.load_context(env)
        else:
            with allure.step('Авторизация на портале c Базового пользователя'):
                auth_page.email_auth(base_user_creds['email'], base_user_creds['password'])

        with allure.step('Переход к профилю'):
            main_page.open_user_profile()

        with allure.step('Закрытие интро окна'):
            user_profile_page.close_intro()

        with allure.step('Переход к форме добавления компании'):
            user_profile_page.create_company()

        with allure.step('Ввод наименования компании'):
            company_profile_page.input_company_name(company_name)
            company_profile_page.add_company_btn_clk()
            company_profile_page.modal_discard_ecp()

        with allure.step('Заполнение информации о компании и создание'):
            company_profile_page.fill_company_info(company_name)
