import allure
import pytest
from pages.auth_page import AuthPage
from pages.community_page import CommunityPage


@allure.suite("Post")
@pytest.mark.events
class TestPost:

    @allure.title("Создание поста")
    @pytest.mark.critical
    def test_create_post(self, page, auth_page: AuthPage, base_user_creds):
        with allure.step("Авторизация"):
            auth_page.email_auth(base_user_creds['email'], password=base_user_creds['password'])
            page.keyboard.press("Escape")

        with allure.step("Создание поста"):
            post = CommunityPage(page)
            post.go_to_community()
            post.go_to_create_post()
            page.wait_for_load_state("networkidle")  # ждём загрузки страницы
            post.title("Мой тестовый заголовок")
            page.wait_for_timeout(500)
            post.select_category("GameDev")
            page.wait_for_timeout(500)
            post.fill_youtube_link("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            page.wait_for_timeout(500)
            post.fill_text("Это текст тестового поста")
            page.wait_for_timeout(500)
            post.publish()