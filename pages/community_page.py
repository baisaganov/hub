from playwright.sync_api import Page, expect
from pages.base import BasePage
import re


class CommunityPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.COMMUNITY_TAP = page.locator('a[href="/ru/community/"]').first
        self.CREATE_POST = page.locator('a[href="/account/v2/blog/create/"]')
        self.AUTHOR = page.get_by_label('Автор')
        self.title_input = page.get_by_placeholder("Например: Инновации встречаются с возможностями")
        self.CATEGORY = page.locator('select.text-select').nth(1)
        self.cover_upload_tab = page.get_by_text("Загрузить")
        self.cover_unsplash_tab = page.get_by_text("Unsplash")
        self.cover_youtube_tab = page.locator('span.community-tab', has_text="Youtube")
        self.YOUTUBE_T = page.get_by_placeholder("Вставьте ссылку на YouTube-видео")
        self.TEXT = page.locator('#editorRU .codex-editor__redactor')
        self.publish_btn = page.get_by_role("button", name="Опубликовать")
        self.confirm_btn = page.locator('button.btn--primary.rounded-md', has_text="Подтвердить")

    # ↓ все методы внутри класса — 4 пробела отступа!
    def go_to_community(self):
        self.page.goto("https://dev.astanahub.com/ru/community/")

    def go_to_create_post(self):
        self.CREATE_POST.click()

    def select_author(self, author: str):
        self.AUTHOR.select_option(label=author)

    def title(self, title: str):
        self.title_input.fill(title)

    def select_category(self, category: str):
        self.CATEGORY.select_option(value="9")  # 9 = GameDev

    def fill_youtube_link(self, url: str):
        self.cover_youtube_tab.click()
        self.page.wait_for_timeout(1000)
        self.YOUTUBE_T.fill(url, force=True)

    def fill_text(self, text: str):
        self.TEXT.click()
        self.TEXT.type(text)

    def publish(self):
        self.publish_btn.click()
        self.page.wait_for_timeout(1000)
        self.confirm_btn.click()
        expect(self.page).to_have_url(re.compile("/success/"))