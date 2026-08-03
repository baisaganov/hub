import re
import json
from pathlib import Path

from playwright.sync_api import Page

from config import config
from utils.logger import Logger


class BasePage:
    logger = Logger().get_logger(__name__)

    def __init__(self, page: Page):
        self.page: Page = page

    #  ============== Готовые функции ==============
    def get_context_path(self, env=''):
        return {
            'COOKIES_PATH': Path(f'testdata/account_data/cookies_{env}.json'),
            'LOCALSTORAGE_PATH': Path(f'testdata/account_data/localstorage_{env}.json'),
            'SESSIONSTORAGE_PATH': Path(f'testdata/account_data/sessionstorage_{env}.json')
        }

    def get_current_lang(self, url) -> str | None:
        """Язык из URL текущего окружения (dev/qa/prod берётся из конфига)"""
        domain = re.escape(
            config.app.app_url.removeprefix("https://").removeprefix("http://")
        )
        match = re.search(rf'https?://{domain}/(en|kk|ru)(?=/|$)', url)
        if match:
            return match.group(1)

        return None

    def save_context(self, env=''):
        paths = self.get_context_path(env)

        cookies = self.page.context.cookies()
        paths['COOKIES_PATH'].write_text(json.dumps(cookies))

        local_data = self.page.evaluate("() => Object.fromEntries(Object.entries(localStorage))")
        paths['LOCALSTORAGE_PATH'].write_text(json.dumps(local_data))

        session_data = self.page.evaluate("() => Object.fromEntries(Object.entries(sessionStorage))")
        paths['SESSIONSTORAGE_PATH'].write_text(json.dumps(session_data))

    def get_input_value(self, selector: str) -> str:
        """:return: значение инпута — сверяется в тесте"""
        return self.page.locator(selector).input_value()
