import allure
import pytest

from playwright.sync_api import Page
from config import config
from pages.auth_page import AuthPage
from pages.community_page import CommunityPage


@allure.suite("Post creation")
@pytest.mark.events
class CreatPost:
    @allure.title("Создание поста")
    def test_create_post(self, page, auth_page: AuthPage, base_user_creds, main_page, community_page):
        with allure.step("Авторизация"):
            auth_page.email_auth(base_user_creds['email'], password=base_user_creds['password'])
            page.keyboard.press("Escape")

        with main_page.page.expect_response("**/community/") as response:
            main_page.page.keyboard.press("Escape")
            main_page.COMMUNITY_LINK.click()
            try:
                main_page.COMMUNITY_LINK.click()
            except:
                pass
        assert response.value.status == 200, "Events page does not open"

@allure.title("Создание поста в Комьюнити")
def test_create_community_post(page, auth_page: AuthPage, base_user_creds, community_page: CommunityPage):
    with allure.step("Авторизация"):
        auth_page.email_auth(base_user_creds['email'], password=base_user_creds['password'])

    with allure.step("Переход в Комьюнити"):
        community_page.click_community()

    with allure.step("Нажать создать пост"):
        community_page.click_create_post()

    with allure.step("Заполнить заголовок"):
        community_page.title_fill(title="Тестовый пост")

    with allure.step("Выбрать категорию"):
        community_page.select_random_category()

    with allure.step("Добавить YouTube ссылку"):
        community_page.youtube_fill(youtube="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    with allure.step("Заполнить текст поста"):
        community_page.text_fill(text1="Текст тестового поста")

    with allure.step("Опубликовать пост"):
        community_page.publish()
        page.wait_for_url("**/blog/**", wait_until='domcontentloaded')
        assert "/blog/" in page.url, f"Пост не опубликован, текущий URL: {page.url}"













