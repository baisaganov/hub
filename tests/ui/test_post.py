import allure
import pytest
from pages.auth_page import AuthPage
from pages.community_page import CommunityPage


@allure.suite("Post")
@pytest.mark.events
class TestPost:

    @allure.title("Создание поста")
    @pytest.mark.critical
    def test_create_post(self, page, auth_page: AuthPage, base_user_creds, create_post):
        with allure.step("Авторизация"):
            auth_page.email_auth(base_user_creds['email'], password=base_user_creds['password'])
            page.keyboard.press("Escape")

        with allure.step("Создание поста"):
            create_post.go_to_community() # TODO: Не переходить на прямую, а из меню
            create_post.go_to_create_post()
            page.wait_for_load_state("networkidle")  # ждём загрузки страницы
            create_post.title("Мой тестовый заголовок")
            create_post.select_category("GameDev")
            create_post.fill_youtube_link("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            create_post.fill_text("Это текст тестового поста")
            create_post.publish()