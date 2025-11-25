import re
from playwright.sync_api import Page, expect
import logging as log
import configparser
from enum import Enum
import allure
from commons.types import FormButton
from config.settings import config_path
from typing import Literal
from config import config


class BasePage:
    logging = log.getLogger(__name__)  # Подхватываем логгер
    config = configparser.ConfigParser()
    config.read(config_path)

    def __init__(self, page: Page):
        self.page = page
        self.save_btn = page.locator('#saveForm[type=submit]')
        self.ecp_submit_btn = page.locator('#sendEcp')
        self.next_btn = page.locator('#nextStep > div.btn')
        self.previous_btn = page.locator('#prevStep > div.btn')

    #  ============== Готовые функции ==============
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

        # self.page.pause()
        match button_id:
            case 'event-save':
                response_url = f'{config.app.app_url}/account/api/event/'
            case 'submit-create-event':
                response_url = re.compile(fr'{config.app.app_url}/account/api/event/.*')
        locator = self.page.locator(f"#{button_id}")
        expect(locator).to_be_visible()
        expect(locator).to_be_enabled()
        with self.page.expect_response(response_url) as response:
            locator.click()

        assert response.value.status == 200, f'BasePage: Ошибка запроса {response.value.status}, json {response.value.json()}'

    #  ============== Трбуется рефакторинг ==============
    def __take_screenshot(self, name="Скриншот"):
        """
        Создание скриншота
        :param name:
        :return:
        """
        allure.attach(
            self.page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    def error_info(self, msg: str, status: int = None, exception: Exception | str = ''):
        """
        Шаблон вывода ошибки в уровень теста
        :param status: Статус ответа, default=None
        :param msg: Текст ошибки для вывода
        :param exception: Какая ошибка
        :return: Возвращается словарь текст
        """
        text = f"[{status}] {msg} \n{exception}"
        self.logging.error(text)
        self.__take_screenshot(msg)
        return text

    def clear_service_id(self, service: Enum):
        """
        Удаление ID заявки из конфига
        :param service:
        :return:
        """
        try:
            service_name = service.value + '_id'
            self.config.set('service_requests', service_name, '0')
            with open(config_path, 'w') as configfile:
                self.config.write(configfile)

        except Exception as e:
            self.error_info(msg="ID заявки не удалось удалить", exception=e)

    def get_request_id(self, service_name: Enum) -> str:
        return self.config['service_requests'][service_name.value + '_id']

    def save_service_id(self, service_name: str, service_id: str):
        """
        Сохранение ID заявки в конфиг
        :param service_name:
        :param service_id:
        :return:
        """
        try:
            self.config.set('service_requests', service_name, service_id)
            with open(config_path, 'w') as configfile:
                self.config.write(configfile)
            self.error_info(status=200, msg=f'ID заявки {service_id} сохранен')
        except Exception as e:
            return self.error_info(status=400,
                                   msg=f'ID заявки {service_id} не удалось сохранить',
                                   exception=e)

