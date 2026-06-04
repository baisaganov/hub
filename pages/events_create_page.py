import random

from playwright.sync_api import Page, expect

from pages.base import BasePage
from config import config
from pathlib import Path


# Авторизация и Регистрация на портале Astanahub
class EventsCreatePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.CREATE_EVENT_BUTTON = page.locator("button:has-text('Создать мероприятие')")
        self.COMPANY_SELECT = page.locator("select[name='company']")
    def create_event(self, event_name: str, event_description: str, company_name: str):
        self.CREATE_EVENT_BUTTON.click()
        self.COMPANY_SELECT.select_option(label=company_name)
        assert self.COMPANY_SELECT.input_value() != "", "Компания не выбрана"
        # Здесь можно добавить дополнительные шаги для заполнения информации о мероприятии и его создания
    from pathlib import Path
 
from playwright.sync_api import Page, expect
 
from pages.base import BasePage
from config import config
 
 
class EventCreatePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
 
        # ============================ Компания (1) ============================
        self.COMPANY_DROPDOWN = page.locator("")  # TODO: add locator
 
        # ============================ Название мероприятия (2) ============================
        self.EVENT_TITLE_INPUT = page.locator("")  # TODO: add locator
 
        # ============================ Описание мероприятия (3) ============================
        self.EVENT_DESCRIPTION_INPUT = page.locator("")  # TODO: add locator
 
        # ============================ Обложка (4) ============================
        self.COVER_UPLOAD_INPUT = page.locator("")  # TODO: add locator
        self.COVER_FILE = Path('testdata/files/event_cover.png')
 
        # ============================ Формат (5) ============================
        self.FORMAT_ONLINE_BTN = page.locator("")   # TODO: add locator
        self.FORMAT_OFFLINE_BTN = page.locator("")  # TODO: add locator
        self.FORMAT_HYBRID_BTN = page.locator("")   # TODO: add locator
 
        # ============================ Дата и время начала (6) ============================
        self.START_DATE_INPUT = page.locator("")  # TODO: add locator
 
        # ============================ Дата и время окончания (7) ============================
        self.END_DATE_INPUT = page.locator("")  # TODO: add locator
 
        # ============================ Ссылка на онлайн-мероприятие (8) ============================
        self.ONLINE_LINK_INPUT = page.locator("")  # TODO: add locator
 
        # ============================ Сфера (9) ============================
        self.SPHERE_DROPDOWN = page.locator("")  # TODO: add locator
 
        # ============================ Приём заявок (10) ============================
        self.OWN_LINK_TOGGLE = page.locator("")  # TODO: add locator - "Использовать собственную ссылку для приёма заявок"
        self.IIN_TOGGLE = page.locator("")       # TODO: add locator - "Запрашивать ИИН для пропуска на мероприятие"
 
        # ============================ Тип мероприятия (11) ============================
        self.EVENT_TYPE_DROPDOWN = page.locator("")  # TODO: add locator
 
        # ============================ Телефон (12) ============================
        self.PHONE_INPUT = page.locator("")  # TODO: add locator
 
        # ============================ Электронная почта (13) ============================
        self.EMAIL_INPUT = page.locator("")  # TODO: add locator
 
        # ============================ Боковая панель — статус и кнопки ============================
        self.STATUS_LABEL = page.locator("")        # TODO: add.  locator - "Черновик"
        self.STATE_LABEL = page.locator("")         # TODO: add locator - "Не сохранено"
        self.SAVE_DRAFT_BTN = page.locator("")      # TODO: add locator - "Сохранить как черновик"
        self.PUBLISH_BTN = page.locator("")         # TODO: add locator - green "Опубликовать"
 
        # ============================ Чекбоксы публикации ============================
        self.PUBLISH_RULES_CHECKBOX = page.locator("")   # TODO: add locator - "Я ознакомлен(а) с «Правилами публикации»"
        self.PUBLISH_PERMIT_CHECKBOX = page.locator("")  # TODO: add locator - "Я даю разрешение на публикацию указанных данных..."
 
    # ============================ Навигация ============================
 
    def navigate(self):
        with self.page.expect_response('**/events/create/') as resp:
            self.page.goto(f'{config.app.app_url}/ru/events/create/')
 
        assert resp.value.status == 200, f'EventCreatePage: Страница не доступна [{resp.value.status}]'
 
    # ============================ Одиночные действия ============================
 
    def select_company(self, company_name: str):
        """
        Выбор компании из дропдауна (поле 1)
        :param company_name: Название компании
        """
        self.COMPANY_DROPDOWN.click()
        self.page.get_by_text(company_name).click()
 
    def fill_event_title(self, title: str):
        """
        Ввод названия мероприятия (поле 2)
        :param title: Название мероприятия (макс. 200 символов)
        """
        self.EVENT_TITLE_INPUT.fill(title)
 
    def fill_event_description(self, description: str):
        """
        Ввод описания мероприятия (поле 3)
        :param description: Описание мероприятия (макс. 1000 символов)
        """
        self.EVENT_DESCRIPTION_INPUT.fill(description)
 
    def upload_cover(self, file_path: Path = None):
        """
        Загрузка обложки мероприятия (поле 4)
        :param file_path: Путь к файлу обложки (по умолчанию testdata/files/event_cover.png)
        """
        target_file = file_path or self.COVER_FILE
        self.COVER_UPLOAD_INPUT.set_input_files(target_file)
 
    def select_format(self, format_type: str = 'online'):
        """
        Выбор формата мероприятия (поле 5): online | offline | hybrid
        :param format_type: Тип формата
        """
        formats = {
            'online': self.FORMAT_ONLINE_BTN,
            'offline': self.FORMAT_OFFLINE_BTN,
            'hybrid': self.FORMAT_HYBRID_BTN,
        }
        btn = formats.get(format_type.lower())
        assert btn is not None, f'EventCreatePage: Неизвестный формат "{format_type}". Допустимые: online, offline, hybrid'
        btn.click()
 
    def fill_start_date(self, date_value: str):
        """
        Ввод даты и времени начала мероприятия (поле 6)
        :param date_value: Дата и время начала
        """
        self.START_DATE_INPUT.fill(date_value)
 
    def fill_end_date(self, date_value: str):
        """
        Ввод даты и времени окончания мероприятия (поле 7)
        :param date_value: Дата и время окончания
        """
        self.END_DATE_INPUT.fill(date_value)
 
    def fill_online_link(self, url: str):
        """
        Ввод ссылки на онлайн-мероприятие (поле 8)
        :param url: Ссылка https://...
        """
        self.ONLINE_LINK_INPUT.fill(url)
 
    def select_sphere(self, sphere_name: str):
        """
        Выбор сферы мероприятия из дропдауна (поле 9)
        :param sphere_name: Название сферы
        """
        self.SPHERE_DROPDOWN.click()
        self.page.get_by_text(sphere_name).click()
 
    def toggle_own_link(self, enable: bool = True):
        """
        Переключение тоггла "Использовать собственную ссылку для приёма заявок" (поле 10)
        :param enable: True — включить, False — выключить
        """
        is_checked = self.OWN_LINK_TOGGLE.is_checked()
        if enable and not is_checked:
            self.OWN_LINK_TOGGLE.click()
        elif not enable and is_checked:
            self.OWN_LINK_TOGGLE.click()
 
    def toggle_iin(self, enable: bool = True):
        """
        Переключение тоггла "Запрашивать ИИН для пропуска на мероприятие" (поле 10)
        :param enable: True — включить, False — выключить
        """
        is_checked = self.IIN_TOGGLE.is_checked()
        if enable and not is_checked:
            self.IIN_TOGGLE.click()
        elif not enable and is_checked:
            self.IIN_TOGGLE.click()
 
    def select_event_type(self, event_type: str):
        """
        Выбор типа мероприятия из дропдауна (поле 11)
        :param event_type: Тип мероприятия
        """
        self.EVENT_TYPE_DROPDOWN.click()
        self.page.get_by_text(event_type).click()
 
    def fill_phone(self, phone: str):
        """
        Ввод номера телефона (поле 12)
        :param phone: Номер телефона
        """
        self.PHONE_INPUT.fill(phone)
 
    def fill_email(self, email: str):
        """
        Ввод электронной почты (поле 13)
        :param email: Email
        """
        self.EMAIL_INPUT.fill(email)
 
    def accept_publish_checkboxes(self):
        """
        Отмечает оба чекбокса публикации:
        - "Я ознакомлен(а) с «Правилами публикации»"
        - "Я даю разрешение на публикацию указанных данных..."
        """
        if not self.PUBLISH_RULES_CHECKBOX.is_checked():
            self.PUBLISH_RULES_CHECKBOX.check()
 
        if not self.PUBLISH_PERMIT_CHECKBOX.is_checked():
            self.PUBLISH_PERMIT_CHECKBOX.check()
 
        assert self.PUBLISH_RULES_CHECKBOX.is_checked(), \
            'EventCreatePage: Чекбокс "Правила публикации" не отмечен'
        assert self.PUBLISH_PERMIT_CHECKBOX.is_checked(), \
            'EventCreatePage: Чекбокс "Разрешение на публикацию" не отмечен'
 
    def click_save_draft(self):
        """
        Клик по кнопке "Сохранить как черновик"
        """
        with self.page.expect_response('**/events/api/**/draft/') as resp:
            self.SAVE_DRAFT_BTN.click()
 
        assert resp.value.status in [200, 201], \
            f'EventCreatePage: Ошибка сохранения черновика [{resp.value.status}]'
 
    def click_publish(self):
        """
        Клик по зелёной кнопке "Опубликовать"
        """
        with self.page.expect_response('**/events/api/**/publish/') as resp:
            self.PUBLISH_BTN.click()
 
        assert resp.value.status in [200, 201], \
            f'EventCreatePage: Ошибка публикации мероприятия [{resp.value.status}]'
 
    # ============================ Обобщённые функции ============================
 
    def fill_required_fields(
        self,
        title: str,
        description: str,
        start_date: str,
        end_date: str,
        sphere: str,
        event_type: str,
        phone: str,
        email: str,
        format_type: str = 'online',
        online_link: str = None,
        company_name: str = None,
    ):
        """
        Заполняет все обязательные поля формы создания мероприятия
        """
        if company_name:
            self.select_company(company_name)
 
        self.fill_event_title(title)
        self.fill_event_description(description)
        self.upload_cover()
        self.select_format(format_type)
        self.fill_start_date(start_date)
        self.fill_end_date(end_date)
 
        if online_link and format_type in ('online', 'hybrid'):
            self.fill_online_link(online_link)
 
        self.select_sphere(sphere)
        self.select_event_type(event_type)
        self.fill_phone(phone)
        self.fill_email(email)
 
    def create_and_publish_event(
        self,
        title: str,
        description: str,
        start_date: str,
        end_date: str,
        sphere: str,
        event_type: str,
        phone: str,
        email: str,
        format_type: str = 'online',
        online_link: str = None,
        company_name: str = None,
    ):
        """
        Полный флоу создания и публикации мероприятия:
        навигация → заполнение полей → чекбоксы → публикация
        """
        self.navigate()
        self.fill_required_fields(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            sphere=sphere,
            event_type=event_type,
            phone=phone,
            email=email,
            format_type=format_type,
            online_link=online_link,
            company_name=company_name,
        )
        self.accept_publish_checkboxes()
        self.click_publish()