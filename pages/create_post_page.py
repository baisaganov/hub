from playwright.sync_api import Page, expect
from pages.base import BasePage
import re
import random



class CreatePostPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.FORM = self.page.locator('div[x-show="!loader"]')
        self.TITLE_POST = self.FORM.locator('input.text-input')
        self.CATEGORY_POST = self.FORM.locator('select[x-model="form.category"]')
        self.YOUTUBE_BTN = self.FORM.locator('div.community-tabs > span').nth(2)
        self.YOUTUBE_LINK = self.FORM.locator('input[type=url]')
        self.TEXT_POLE = self.FORM.locator('#editorRU div.ce-paragraph').first

        self.PUBLISH_BTN = self.page.locator("btn btn--primary btn-medium w-full")

        self.WINDOW = self.page.locator('div[x-show="showTranslationModal"]')
        self.MODALKA_TRANSLATE_BTN = self.WINDOW.locator("button.btn--primary")


    def title_text(self, text):
        self.TITLE_POST.fill(text)

    def category_post(self):
        self.CATEGORY_POST.scroll_into_view_if_needed()
        self.CATEGORY_POST.click()
        options = self.CATEGORY_POST.locator("option")
        count = options.count()
        random_index = random.randint(1, count - 1)
        random_value = options.nth(random_index).get_attribute("value")
        self.CATEGORY_POST.select_option(value=random_value)

    def youtube_btn(self):
        expect(self.YOUTUBE_BTN).to_be_visible()
        self.YOUTUBE_BTN.click()

    def youtube_link(self, link):
        self.YOUTUBE_LINK.click()
        self.YOUTUBE_LINK.fill(link)

    def fill_body(self, text):
        self.TEXT_POLE.click()
        self.TEXT_POLE.fill(text)

    def publish_btn(self):
        expect(self.PUBLISH_BTN).to_be_visible()
        self.PUBLISH_BTN.click()

    def translate_modalka(self):
        expect(self.WINDOW).to_be_visible()
        expect(self.MODALKA_TRANSLATE_BTN).to_be_visible()
        self.MODALKA_TRANSLATE_BTN.click()



