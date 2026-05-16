import re
from playwright.sync_api import Page, expect, Locator
import logging as log
import configparser
from enum import Enum
import allure
from config.settings import config_path
from typing import Literal
from config import config
import json
from pathlib import Path


class BasePage:
    logging = log.getLogger(__name__)  # Подхватываем логгер

    def __init__(self, page: Page):
        self._page = page
        self.SAVE_BTN = page.locator('#saveForm[type=submit]')
        self.SUBMIT_ECP_BTN = page.locator('#sendEcp')
        self.NEXT_BTN = page.locator('#nextStep > div.btn')

    #  ============== Готовые функции ==============
    def get_context_path(self, env=''):
        return {
            'COOKIES_PATH': Path(f'testdata/account_data/cookies_{env}.json'),
            'LOCALSTORAGE_PATH': Path(f'testdata/account_data/localstorage_{env}.json'),
            'SESSIONSTORAGE_PATH': Path(f'testdata/account_data/sessionstorage_{env}.json')
        }

    def save_context(self, env=''):
        paths = self.get_context_path(env)
        COOKIES_PATH = paths.get('COOKIES_PATH')
        LOCALSTORAGE_PATH = paths.get('LOCALSTORAGE_PATH')
        SESSIONSTORAGE_PATH = paths.get('SESSIONSTORAGE_PATH')

        cookies = self._page.context.cookies()
        COOKIES_PATH.write_text(json.dumps(cookies))

        local_data = self._page.evaluate("() => Object.fromEntries(Object.entries(localStorage))")
        LOCALSTORAGE_PATH.write_text(json.dumps(local_data))

        session_data = self._page.evaluate("() => Object.fromEntries(Object.entries(sessionStorage))")
        SESSIONSTORAGE_PATH.write_text(json.dumps(session_data))

    def load_context(self, env=''):
        paths = self.get_context_path(env)
        COOKIES_PATH = paths.get('COOKIES_PATH')
        LOCALSTORAGE_PATH = paths.get('LOCALSTORAGE_PATH')
        SESSIONSTORAGE_PATH = paths.get('SESSIONSTORAGE_PATH')

        if COOKIES_PATH.exists():
            with open(COOKIES_PATH) as f:
                cookies = json.load(f)
            self._page.context.add_cookies(cookies)

        if LOCALSTORAGE_PATH.exists():
            data = json.load(open(LOCALSTORAGE_PATH))
            for key, value in data.items():
                self._page.add_init_script(f"""
                        localStorage.setItem('{key}', '{value}');
                    """)

        if SESSIONSTORAGE_PATH.exists():
            data = json.load(open(SESSIONSTORAGE_PATH))
            self._page.evaluate(f"""
                const data = {json.dumps(data)};
                Object.entries(data).forEach(([k, v]) => sessionStorage.setItem(k, v));
            """)

        self._page.reload()

    def is_context_exists(self, env):
        paths = self.get_context_path(env)
        COOKIES_PATH = paths.get('COOKIES_PATH')
        LOCALSTORAGE_PATH = paths.get('LOCALSTORAGE_PATH')
        SESSIONSTORAGE_PATH = paths.get('SESSIONSTORAGE_PATH')

        return True if COOKIES_PATH.exists() and LOCALSTORAGE_PATH.exists() and SESSIONSTORAGE_PATH.exists() else False

    def check_input_text_correct(self, locator: str, text: str) -> str:
        result = self._page.evaluate(f'document.querySelector("{locator}").value')
        return result

    def action_buttons(self, button_id: Literal[
        'event-save',
        'submit-create-event'
    ]):
        """
        Сохранение и Отправка заполненной формы
        :param button_id: ID кнопки для клика
            - 'event-save': Сохранить черновик Event
            - 'submit-create-event': Отправить Event на модерацию
        :return:
        """
        response_url = ''

        match button_id:
            case 'event-save':
                response_url = f'{config.app.app_url}/account/api/event/'
            case 'submit-create-event':
                response_url = re.compile(fr'{config.app.app_url}/account/api/event/.*')
        locator = self._page.locator(f"#{button_id}")
        expect(locator).to_be_visible()
        expect(locator).to_be_enabled()
        with self._page.expect_response(response_url) as response:
            locator.click()

        assert response.value.status == 200, f'BasePage: Ошибка запроса {response.value.status}, json {response.value.json()}'

