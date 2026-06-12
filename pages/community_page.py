from playwright.sync_api import Page, expect
from pages.base import BasePage
import random


class CommunityPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.COMMUNITY_MENU = page.locator('#tour3')
        self.CREATE_POST = page.locator('a[href="/account/v2/blog/create/"]')
        self.TITLE = page.locator('input[x-model="form.title[lang]"]')
        self.CATEGORY = page.locator('select[x-model="form.category"]')
        self.YOUTUBE = page.locator('div.community-tabs span.community-tab', has_text = "Youtube")
        self.YOUTUBE_TEXT = page.locator('div[x-show="activeTab === \'youtube\'"] input[x-model="youtubeUrl"]')
        self.TEXT = self.page.locator('#editorRU .ce-paragraph[contenteditable="true"]')

        # опубликовать кнопка + форма
        self.PUBLISH = page.locator('span[x-show="!pendingPublish"]')
        self.PROCEED_TRANSLATION_BTN = page.locator('button.btn--primary.rounded-md') # для кнопки подтвердить

    def click_community(self):
        self.COMMUNITY_MENU.click()

    def click_create_post(self):
        self.CREATE_POST.click()
        self.page.wait_for_url("**/blog/create/**", wait_until='networkidle') # осыны понять

    def title_fill(self, title):
        self.TITLE.click()
        self.TITLE.fill(title)

    def select_random_category(self):
        # получаем все доступные options
        options = self.CATEGORY.locator('option').all()
        # убираем первый если это пустой placeholder ("Выберите категорию")
        options = [opt for opt in options if opt.get_attribute('value')]
        # выбираем рандомный
        random_option = random.choice(options)
        value = random_option.get_attribute('value')
        self.CATEGORY.select_option(value)

    def youtube_fill(self, youtube):
        self.YOUTUBE.click()
        self.YOUTUBE_TEXT.fill(youtube, force=True)

    def text_fill(self, text1):
        self.TEXT.click()
        self.TEXT.wait_for(state='visible')
        self.page.keyboard.type(text1)
        # ждём пока текст появится в редакторе
        self.page.wait_for_function(
            f"document.querySelector('#editorRU .ce-paragraph').innerText.length > 0"
        )

    # опубликовать
    def publish(self):
        self.PUBLISH.click()
        self.PROCEED_TRANSLATION_BTN.wait_for(state='visible')
        self.PROCEED_TRANSLATION_BTN.click()





