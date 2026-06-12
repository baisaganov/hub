from playwright.sync_api import Page, expect
from pages.base import BasePage
import re

class NotificationPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.NOTIFICATION_BTN = page.locator('[href="/account/v2/user/profile/notifications/"]')

    def notification_click(self):
        self.NOTIFICATION_BTN.click(force=True)
