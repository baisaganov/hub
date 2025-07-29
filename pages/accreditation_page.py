from playwright.sync_api import Page

from commons.types import AccreditationType
from base.base_page import BasePage
from config.links import Links
from config.settings import upload_document

class AccreditationPage(BasePage):
    """
    Услуга: Аккредитация (Аккредитация, переоформление, дубликат)
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        self.cert_number_input = page.locator('input[name=cert_number]')
        self.iin_input = page.locator('input[name=iin_number]')
        self.bin_input = page.locator('input[name=company_bin]')
        self.fio_input = page.locator('input[name=surname_field]')
        self.phone_number_input = page.locator('input[name=mobile_phone_number]')
        self.email_input = page.locator('input[name=email_field]')
        self.cert_give_date = page.locator('input[name=accreditation_given_date]')
        self.cert_end_date = page.locator('input[name=data_cved]')
        self.given_org = page.locator('input[name=vydano_svid]')
        self.company_name_input = page.locator('div.fblockcompany_name  > input[name=company_name]')
        self.dublicate_reason_input = page.locator('input[name=reason_why]')

        self.check_cert_btn = page.locator('div.check-wrapper > div.btn')

        self.fio_doc = page.locator(
            'div.fblockchange_accept_copy > div.file-block > div.label-file-upload > label > input[type=file]')
        self.old_cert_doc = page.locator(
            'div.fblockcert_copy > div.file-block > div.label-file-upload > label > input[type=file]')

        # Старая аккредитация ФЛ
        self.surname_input = page.locator('input[name=surname]')
        self.name_input = page.locator('input[name=name]')
        self.patronymic_input = page.locator('input[name=patronymic]')
        self.iin_field = page.locator('input[name=iin]')
        self.mobile_number_input = page.locator('input[name=mobile_number]')
        self.email_field = page.locator('input[name=email]')

    @staticmethod
    def __get_service_link(service_type: AccreditationType):
        match service_type:
            case service_type.RENEWAL_FL:
                return Links.ACCREDITATION_RENEWAL_FL
            case service_type.RENEWAL_UL:
                return Links.ACCREDITATION_RENEWAL_UL
            case service_type.DUBLICATE_FL:
                return Links.ACCREDITATION_DUBLICATE_FL
            case service_type.DUBLICATE_UL:
                return Links.ACCREDITATION_DUBLICATE_UL
            case _:
                return None

    def nav_service_(self, service_type: AccreditationType):
        """
        Переход к форме заполнения заявки
        :param service_type: AccreditationType К какому виду формы аккредитации переходить
        :return:
        """
        url = self.__get_service_link(service_type)
        with self.page.expect_response(url) as resp:
            self.page.goto(url)
            self.logging.info(f'{service_type.value}: Navigate to {url}')

        assert resp.value.status in [200, 302], self.error_info(status=resp.value.status,
                                                                msg=f'{service_type.value}: Page not reacheable '
                                                                    f'[{service_type.value}]')

        assert self.page.locator('#page404').count() == 0, self.error_info(status=404,
                                                                           msg=f'{service_type.value}: '
                                                                               f'Прием заявок не открыт '
                                                                               f'[{service_type.value}]')

    def fill_service_renewal_fl(self, cert_number: str):
        """
        Заполнение формы переоформления аккредитации ФЛ
        :param cert_number: Номер сертификата для проверки в базе
        :return:
        """

        self.cert_number_input.click()
        self.cert_number_input.fill(cert_number)  # Ввод номера сертификата

        with self.page.expect_response(f'https://dev.astanahub.com/service/api/fl-accreditation-requests/'
                                       f'{cert_number}/') as resp:
            self.check_cert_btn.click()
            self.logging.info(f"Accreditation Renewal FL: Check btn clicked")

        assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                         msg=f'Accreditation Renewal FL: Check btn clicked error '
                                                             f'{resp.value.json()}')

        self.phone_number_input.fill('1234567890')

        with self.page.expect_response('https://dev.astanahub.com/account/api/protected_media_file/') as resp:
            self.fio_doc.set_input_files(upload_document)
            self.logging.info(f"Accreditation Renewal FL: FIO file upload")

        assert resp.value.status in [200, 201], self.error_info(f'Accreditation Renewal FL: FIO doc not uploaded '
                                                                f'{resp.value.json()}')

        with self.page.expect_response('https://dev.astanahub.com/account/api/protected_media_file/') as resp:
            self.old_cert_doc.set_input_files(upload_document)
            self.logging.info(f"Accreditation Renewal FL: Old cert doc file upload")

        assert resp.value.status in [200, 201], self.error_info(status=resp.value.status,
                                                                msg=f'Accreditation Renewal FL: '
                                                                    f'Old cert file not uploaded {resp.value.json()}')

    def fill_service_renewal_ul(self, cert_number: str):
        """
        Заполнение формы переоформления аккредитации ЮЛ

        :param cert_number: Номер сертификата для проверки в базе
        :return:
        """
        self.cert_number_input.click()
        self.cert_number_input.fill(cert_number)
        self.logging.info(f"Accreditation Renewal UL: Номер свидетельства введен")

        with self.page.expect_response(f'https://dev.astanahub.com/service/api/company-accreditation-requests/'
                                       f'{cert_number}/') as resp:
            self.check_cert_btn.click()
            self.logging.info(f"Accreditation Renewal UL: Check btn clicked")

        assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                         msg=f'Accreditation Renewal FL: Check btn clicked error '
                                                             f'{resp.value.json()}')

        assert (self.cert_give_date.input_value() != '' or
                self.company_name_input.input_value() != '' or
                self.email_input.input_value() != ''), self.error_info(
            msg=f'Accreditation Renewal UL: Автозаполнение не работает '
                f'Cert give date = {self.cert_give_date.input_value()}'
                f'BIN = {self.bin_input.input_value()}'
                f'Company name = {self.company_name_input.input_value()}'
                f'Email = {self.email_input.input_value()}')

        try:
            self.cert_give_date.click()
            self.page.get_by_text('10', exact=True).click()
            self.logging.info(f"Accreditation Renewal UL: Дата выдачи сертификата заполнена")
        except Exception as e:
            assert 1 == 0, self.error_info(msg=f"Акред Переоформление ЮЛ: Ошибка при заполнении даты",
                                           exception=e)

        # if self.cert_give_date.input_value() == '':
        #     logging.info('ERRRRRRR')
        # else:
        #     logging.info(self.cert_give_date.input_value())

        try:
            self.bin_input.fill('123456789112')
            self.logging.info(f"Accreditation Renewal UL: Бин заполнен")
        except Exception as e:
            return self.error_info(msg=f"Акред Переоформление ЮЛ: Ошибка при заполнении БИН",
                                   exception=e)

        self.company_name_input.fill('Test Company Name')
        self.phone_number_input.fill('1234567890')

        with self.page.expect_response('https://dev.astanahub.com/account/api/protected_media_file/') as resp:
            self.fio_doc.set_input_files(upload_document)
            self.logging.info(f"Accreditation Renewal UL: Rename file upload")

        assert resp.value.status in [200, 201], self.error_info(status=resp.value.status,
                                                                msg=f'Accreditation Renewal UL: Rename doc not uploaded'
                                                                    f' {resp.value.json()}')

        with self.page.expect_response('https://dev.astanahub.com/account/api/protected_media_file/') as resp:
            self.old_cert_doc.set_input_files(upload_document)
            self.logging.info(f"Accreditation Renewal UL: Old cert doc file upload")

        assert resp.value.status in [200, 201], self.error_info(status=resp.value.status,
                                                                msg=f'Accreditation Renewal UL: Old cert file not '
                                                                    f'uploaded {resp.value.json()}')

    def fill_service_dublicate_fl(self, cert_number, iin):
        """
        Заполнение формы дубликата аккредитации ФЛ

        :param cert_number: Номер сертификата для проверки в базе
        :param iin:
        :return:
        """
        self.cert_number_input.click()
        self.cert_number_input.fill(cert_number)
        self.logging.info('Accreditation Dubplicate FL: Номер свидетельства введен')

        with self.page.expect_response('') as resp:
            self.check_cert_btn.click()
            self.logging.info('Accreditation Dubplicate FL: Кнопка проверки нажата')

        assert resp.value.status == 200, self.error_info(status=resp.value.status,
                                                         msg="Accreditation Dubplicate FL: Ошибка при проверке свид-ва")

        assert (self.cert_give_date.input_value() != '' or
                self.cert_end_date.input_value() != '' or
                self.iin_input.input_value() != '' or
                self.company_name_input.input_value() != ''
                ), self.error_info(msg="Accreditation Dubplicate FL: Автозаполнение не работает")

        try:
            self.cert_give_date.click()
            self.page.get_by_text('10', exact=True).click()
            self.logging.info(f"Accreditation Dubplicate FL: Дата выдачи сертификата заполнена")
        except Exception as e:
            assert 1 == 0, self.error_info(msg="Accreditation Dubplicate FL: Ошибка при заполнении даты выдачи",
                                           exception=e)

        try:
            self.cert_end_date.click()
            self.page.get_by_text('20', exact=True).click()
            self.logging.info(f"Accreditation Dubplicate FL: Дата завершнения сертификата заполнена")
        except Exception as e:
            assert 1 == 0, self.error_info(msg="Accreditation Dubplicate FL: Ошибка при заполнении завершнения даты",
                                           exception=e)

        self.given_org.fill('TOO Astana')

        try:
            self.iin_input.fill(iin)
            self.logging.info('Accreditation Dubplicate FL: ИИН заполнен')
        except Exception as e:
            assert 1 == 0, self.error_info("Accreditation Dubplicate FL: Ошибка при заполнении ИИН", exception=e)

        self.company_name_input.fill("Auto Test")
        self.phone_number_input.fill('1234567890')
        self.dublicate_reason_input.fill('Test')

        with self.page.expect_response('https://dev.astanahub.com/account/api/protected_media_file/') as resp:
            self.old_cert_doc.set_input_files(upload_document)
            self.logging.info('Accreditation Dubplicate FL: Загржуен старый сертификат')

        assert resp.value.status in [200, 201], self.error_info(status=resp.value.status,
                                                                msg=f'AAccreditation Dubplicate FL: Old cert file not '
                                                                    f'uploaded {resp.value.json()}')

