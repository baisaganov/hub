import random

from playwright.sync_api import Page
from datetime import datetime, timedelta, timezone, date

from pages.base import BasePage
from config import config
from typing import Literal

from lorem_text import lorem


class EventPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page

        # BTNS List
        self.EVENT_LIST_BTNS = self.page.locator("div.events-list-buttons > a")
        self.CREATE_EVENT = self.EVENT_LIST_BTNS.first
        self.MY_EVENTS = self.EVENT_LIST_BTNS.last

        # Блок табов (Все, Избранные)
        self.TABS_BLOCK = self.page.locator("div.tabs-block")
        self.ALL = self.TABS_BLOCK.first
        self.FAVORITE = self.TABS_BLOCK.last

        # Форма создания ивента
        self.COMPANY_SELECT = self.page.locator("#event-company")
        self.EVENT_TITLE = self.page.locator("fieldset[data-type=title] [required]")
        self.EVENT_DESCRIPTION = self.page.locator("#editorRU_ifr")
        self.ATTACH_COVER = self.page.locator("#inputImage")
        self.EVENT_FORMAT = self.page.locator(".event-format-list")
        self.DATETIME_START = self.page.locator("input[data-alt-field='#datetime_start']")
        self.DATETIME_END = self.page.locator("input[data-alt-field='#datetime_end']")
        self.ONLINE_LINK = self.page.locator("input[name=online_link]")
        self.EVENT_SCOPE = self.page.locator("div.event-form-field span[role=combobox]")
        self.EVENT_SCOPE_LIST = self.page.locator("ul[role=listbox] > li")
        self.EVENT_TYPE_SELECT = self.page.locator("select[name=event_type]")
        self.OWN_LINK_SLIDER = self.page.locator("#use_own_link")
        self.EVENT_PHONE = self.page.locator("div.event-form-field > input[name=phone]")
        self.EVENT_EMAIL = self.page.locator("div.event-form-field > input[name=email]")
        self.AGREEMENT = self.page.locator("div.event-form-section > div.label-checkbox input[type=checkbox]")

    # =============== Сингл таск функции ===============
    def navigate(self):
        """
        Переход на страницу мероприятий
        :return:
        """
        with self.page.expect_response(f'{config.app.app_url}/ru/event/') as resp:
            self.page.goto(f'{config.app.app_url}/ru/event/')

        assert resp.value.status == 200, "EventPage: Страница не доступна"

    def select_scope(self, scope_count: int) -> list[int]:
        """
        Выбор рандомных сфер ивента
        :param scope_count: Int сколько сфер нужно выбрать
        :return: Список из int которые были выбраны
        """
        scopes_selected = []
        for i in range(0, scope_count):
            self.EVENT_SCOPE.click()
            scope_count = self.EVENT_SCOPE_LIST.count()
            scope_to_select = random.randint(1, scope_count)
            step = True
            while step:
                if scope_to_select in scopes_selected:
                    scope_to_select = random.randint(1, 7)
                    continue

                step = False
            self.EVENT_SCOPE_LIST.nth(scope_to_select).click()
            scopes_selected.append(scope_to_select)

        return scopes_selected

    def open_create_form(self):
        """
        Клик по кнопке "Создать мероприятие"
        :return:
        """
        with self.page.expect_response(f'{config.app.app_url}/account/event/create/') as resp:
            self.CREATE_EVENT.click()

        assert resp.value.status == 200, 'EventPage: Страница не доступна'

    # =============== Мульти таск функции ===============
    #     TODO: Добавить в функцию гибридный и оффлайн форматы
    #     TODO: Добавить в функцию выбор своей ссылки
    def fill_form(self,
                  company_id,
                  phone_number="+77777777777",
                  link="https://test.kz",
                  event_type: Literal["open_event", "closed_event"] = "open_event",
                  event_format: Literal["online", "astanahub", "hybrid"] = "online",
                  scope_count: int = 1
                  ):
        """

        Заполнение формы создания мероприятий
        :param company_id: ID компании в которой юзер Владелец или Советник
        :param phone_number: Номер телефона для связи  ( дефолтный +77777777777)
        :param link: Ссылка на конференцию
        :param event_type: Тип ивента (Открытый или Закрытый)
        :param event_format: Формат провередения ивента ( Онлайн, Офлайн, Гибрид )
        :param scope_count: Какой количество сфер выбререт автотест
        :return:
        """
        today = date.today()
        data_day = (date(today.year, today.month+1, 1) - timedelta(days=1)).day
        data_month = today.month
        data_year = today.year
        tz = timezone(timedelta(hours=5))
        self.COMPANY_SELECT.select_option(value=str(company_id))
        self.EVENT_TITLE.fill(f'Auto test {datetime.now(tz)}')
        self.EVENT_DESCRIPTION.click()
        self.page.keyboard.type(lorem.words(30))
        self.ATTACH_COVER.set_input_files('testdata/files/test_pdf.pdf')

        assert (self.EVENT_FORMAT.locator('li.current')
                .get_attribute('data-value') == event_format), 'EventPage: Формат ивента != Онлайн'

        self.DATETIME_START.click()

        self.page.locator(f'div[data-date=\"{data_day-1}\"][data-month=\"{data_month-1}\"][data-year=\"{data_year}\"]').first.click()

        self.DATETIME_END.click()
        self.page.locator(f'div[data-date="{data_day}"][data-month="{data_month-1}"][data-year="{data_year}"]').last.click()

        self.ONLINE_LINK.fill(link)

        self.select_scope(scope_count)

        self.EVENT_TYPE_SELECT.select_option(value=event_type)

        self.EVENT_PHONE.fill(phone_number)

        assert self.EVENT_EMAIL.get_attribute('value') not in [None, ''], 'EventPage: Почта не подтянулась'

        for checkbox in self.AGREEMENT.all():
            checkbox.check()





# <div class="datepicker--cell datepicker--cell-day -weekend-" data-date="8" data-month="10" data-year="2025">8</div>