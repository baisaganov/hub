from commons.custom_response import CustomResponse
from pages import Enum, configparser, re, log, Page

from pages import SignXml, allure

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

    def error_response(self, error_text: str, service: Enum, status: int = None, exception: Exception | None = None):
        """
        Шаблон вывода ошибки в уровень теста
        :param status: Статус ответа, default=None
        :param service: в Каком сервисе возникла ошибка
        :param error_text: Текст ошибки для вывода
        :param exception: Какая ошибка
        :return: Возвращается словарь {"response"}
        """
        text = f"[{status}]{service.value}: {error_text} \n{exception}"
        self.logging.error(text)
        self.__take_screenshot(error_text)
        return CustomResponse(status_code=status, service=service, msg=error_text)

    def pass_response(self, service: Enum, message: str, status: int = None):
        """
        Ответ когда все ок
        :param service:
        :param message:
        :param status:
        :return:
        """
        text = f"[{status}]{service.value}: {message}"
        self.logging.debug(text)
        return CustomResponse(status_code=status, service=service, msg=text)

    def clear_service_id(self, service: Enum) -> CustomResponse:
        """
        Удаление ID заявки из конфига
        :param service:
        :param service_name:
        :return:
        """
        try:
            service_name = service.value + '_id'
            self.config.set('service_requests', service_name, '0')
            with open(config_path, 'w') as configfile:
                self.config.write(configfile)

            return self.pass_response(service=service, status=200, message='ID заявки удален')
        except Exception as e:
            return self.error_response(service=service,
                                       status=400,
                                       error_text='ID заявки не удалось удалить',
                                       exception=e)

    def get_request_id(self, service_name: Enum) -> str:
        return self.config['service_requests'][service_name.value + '_id']

    def save_service_id(self, service_name: Enum, service_id: str):
        """
        Сохранение ID заявки в конфиг
        :param service_name:
        :param service_id:
        :return:
        """
        try:
            self.config.set('service_requests', service_name.value + '_id', service_id)
            with open(config_path, 'w') as configfile:
                self.config.write(configfile)
            self.pass_response(status=200, service=service_name, message=f'ID заявки {service_id} сохранен')
        except Exception as e:
            return self.error_response(status=400,
                                       error_text=f'ID заявки {service_id} не удалось сохранить',
                                       exception=e,
                                       service=service_name)

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

            if resp.value.status not in [200, 201]:
                return self.error_response(error_text=f'Save error',
                                           status=resp.value.status,
                                           service=service_type)
            return self.pass_response(
                status=resp.value.status,
                service=service_type,
                message='{service_type.value}: Сохраненно')

        elif button_type.value == FormButton.ECP_SUBMIT.value:
            with self.page.expect_response(
                    f'https://dev.astanahub.com/account/api/service_request/{request_id}/sign/') as resp:
                self.logging.info(f"{service_type.value}: Submit btn click")
                self.ecp_submit_btn.click()
                self.logging.info(f"{service_type.value}: Sign started")
                SignXml().sign_xml()
                self.logging.info(f"{service_type.value}: Sign ended")

            if resp.value.status not in [200, 201]:
                return self.error_response(error_text=f'Sign error',
                                           status=resp.value.status,
                                           service=service_type)
            return self.pass_response(
                status=resp.value.status,
                service=service_type,
                message=f"{service_type.value}: Подписано")

        elif button_type.value == FormButton.NEXT.value:
            self.next_btn.click()
            return self.pass_response(
                status=200,
                service=service_type,
                message=f"{service_type.value}: Следующая страница кнопка нажата")

        elif button_type.value == FormButton.PREV.value:
            self.previous_btn.click()
            return self.pass_response(
                status=200,
                service=service_type,
                message=f"{service_type.value}: Предыдующая страница кнопка нажата")
