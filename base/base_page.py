from base import Enum, configparser, re, log, Page

from base import SignXml, allure

from commons.types import FormButton
from config.settings import config_path


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

    def clear_service_id(self, service: Enum) -> str:
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

            return self.error_info(status=200, msg='ID заявки удален')
        except Exception as e:
            return self.error_info(
                                       status=400,
                                       msg='ID заявки не удалось удалить',
                                       exception=e)

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

    def save_and_submit_form(self, service_type: Enum, button_type: FormButton):
        """
        Сохранение и Отправка заполненной формы
        :param button_type: Тип кнопки (Сохранить, Подписать, Отправить, След, Пред)
        :param service_type: AccreditationType Какой вид формы аккредитации
        :return:
        """
        request_id = re.findall("(\\d+)", self.page.url)[0]
        if button_type.value == FormButton.SAVE.value:
            with self.page.expect_response(
                    f'https://dev.astanahub.com/account/api/service_request/{request_id}/') as resp:
                self.save_btn.click()
                self.logging.debug(f"{service_type.value}: Save btn click")

            assert resp.value.status in [200, 201], self.error_info(
                msg=f'{service_type.value}: Save from error',
                status=resp.value.status)

        elif button_type.value == FormButton.ECP_SUBMIT.value:
            with self.page.expect_response(
                    f'https://dev.astanahub.com/account/api/service_request/{request_id}/sign/') as resp:
                self.logging.debug(f"{service_type.value}: Submit btn click")
                self.ecp_submit_btn.click()
                self.logging.debug(f"{service_type.value}: Sign started")
                SignXml().sign_xml()
                self.logging.debug(f"{service_type.value}: Sign ended")

            assert resp.value.status in [200, 201], self.error_info(
                msg=f'{service_type.value}: Sign error',
                status=resp.value.status)

        # Нужно придумать какие ассерты добавить (вариант со сменой сслыки? проверить в логах меняется ли)
        elif button_type.value == FormButton.NEXT.value:
            self.logging.info(self.page.url)
            self.next_btn.click()
            self.logging.info(self.page.url)

        elif button_type.value == FormButton.PREV.value:
            self.logging.info(self.page.url)
            self.previous_btn.click()
            self.logging.info(self.page.url)
        return request_id