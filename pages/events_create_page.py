import random
import re

from playwright.sync_api import Page, Locator
from datetime import datetime, timedelta, timezone

from pages.base import BasePage
from config import config
from typing import Literal

from lorem_text import lorem

# Соответствие значений формата кнопкам-табам на форме
FORMAT_LABELS = {
    "online": "Онлайн",
    "astanahub": "Офлайн",
    "hybrid": "Гибридный",
}


class EventCreatePage(BasePage):
    """
    Форма создания ивента (редизайн: Alpine.js).
    У полей нет стабильных id/name — локаторы строятся по атрибутам x-model.
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # Форма создания ивента
        self.COMPANY_SELECT = self.page.locator('select[x-model="form.company"]')
        # Поля тайтла ru/kk/en, в DOM все три — виден только текущий язык
        self.EVENT_TITLE = self.page.locator('input[x-model="form.title[lang]"]')
        self.EVENT_TITLE_VISIBLE = self.page.locator('input[x-model="form.title[lang]"]:visible')
        # Описание — EditorJS (contenteditable)
        self.EVENT_DESCRIPTION = self.page.locator("#editorRU .codex-editor__redactor")
        # Обложка: принимает только png/jpeg, после выбора открывается кроппер
        self.ATTACH_COVER = self.page.locator('input[type="file"][accept="image/png,image/jpeg"]').first
        self.CROPPER_SUBMIT = self.page.locator('button[\\@click="$store.avatarCropper.cropImage()"]')

        # Формат ивента — табы (Онлайн / Офлайн / Гибридный)
        self.EVENT_FORMAT_OPTIONS = self.page.locator('span[x-text="opt.label"]')

        # Датапикеры
        self.DATETIME_START = self.page.locator('div[x-model="form.datetime_start"]')
        self.DATETIME_END = self.page.locator('div[x-model="form.datetime_end"]')

        self.ONLINE_LINK = self.page.locator('input[x-model="form.online_link"]')

        # Мультиселект сфер
        self.SCOPE_FIELD = self.page.locator("div[x-data*=\"name: 'scope'\"]")
        self.SCOPE_TOGGLE = self.SCOPE_FIELD.get_by_role("button").first
        self.SCOPE_ITEMS = self.SCOPE_FIELD.locator("ul > li")
        # Пилюли выбранных сфер над дропдауном
        self.SCOPE_SELECTED_PILLS = self.SCOPE_FIELD.locator("div.rounded-full")

        self.EVENT_TYPE_SELECT = self.page.locator('select[x-model="form.event_type"]')
        self.EVENT_PHONE = self.page.locator('input[x-model="form.phone"]')
        self.EVENT_EMAIL = self.page.locator('input[x-model="form.email"]')

        self.POLICY_CHECKBOX = self.page.locator("#publication_policy_accepted")
        self.AGREEMENT_CHECKBOX = self.page.locator("#agreement")

        self.SAVE_DRAFT_BTN = self.page.get_by_role("button", name="Сохранить как черновик")
        self.PUBLISH_BTN = self.page.get_by_role("button", name="Опубликовать")
        # Модалка автоперевода (появляется, если контент заполнен не на всех языках)
        self.TRANSLATION_MODAL_SUBMIT = self.page.locator('button[\\@click="proceedWithTranslation()"]')

    # =============== Сингл таск функции ===============
    def navigate(self):
        """Переход на страницу мероприятий"""
        with self.page.expect_response(f"{config.app.app_url}/ru/event/") as resp:
            self.page.goto(f"{config.app.app_url}/ru/event/", wait_until="domcontentloaded")

        return resp.value

    def format_option(self, event_format: Literal["online", "astanahub", "hybrid"]) -> Locator:
        """Локатор таба формата ивента (для клика и проверок в тесте)"""
        return self.EVENT_FORMAT_OPTIONS.filter(has_text=FORMAT_LABELS[event_format])

    def select_format(self, event_format: Literal["online", "astanahub", "hybrid"]):
        """Клик по табу формата ивента"""
        self.format_option(event_format).click()

    def fill_description(self, words: int = 30):
        """Заполнение описания в EditorJS"""
        self.EVENT_DESCRIPTION.click()
        self.page.keyboard.type(lorem.words(words))

    def upload_cover(self, file_path: str = "testdata/files/profile_photo.png"):
        """
        Загрузка обложки: выбор файла и подтверждение в кроппере.
        Перед кликом ждём загрузку изображения в croppie — иначе cropImage() зависает.
        :return: ответ POST /account/api/media_file/
        """
        self.ATTACH_COVER.set_input_files(file_path)
        # croppie рисует canvas.cr-image асинхронно (~100мс после открытия модалки)
        self.page.wait_for_function(
            "() => { const c = document.querySelector('canvas.cr-image');"
            " return c && c.width > 0; }"
        )
        with self.page.expect_response(re.compile(r"/account/api/media_file/")) as resp:
            self.CROPPER_SUBMIT.click()
        self.CROPPER_SUBMIT.wait_for(state="hidden")
        return resp.value

    def _pick_date(self, picker: Locator, day: int):
        """
        Выбор дня в датапикере: открыть, перелистнуть на следующий месяц, кликнуть день.
        День ищется только в сетке календаря, чтобы не пересечься с колонками часов/минут.
        """
        picker.locator("input").click()
        picker.locator('button[\\@click="nextMonth()"]').click()
        picker.locator("div.grid.grid-cols-7").get_by_role("button", name=str(day), exact=True).first.click()
        self.page.keyboard.press("Escape")

    def set_dates(self, start_day: int = 15, end_day: int = 16):
        """Даты проведения: start и end в следующем месяце (всегда валидны для модерации)"""
        self._pick_date(self.DATETIME_START, start_day)
        self._pick_date(self.DATETIME_END, end_day)

    def select_scope(self, scope_count: int) -> list[str]:
        """
        Выбор рандомных сфер ивента в мультиселекте
        :param scope_count: сколько сфер нужно выбрать
        :return: названия выбранных сфер
        """
        self.SCOPE_TOGGLE.click()
        total = self.SCOPE_ITEMS.count()
        indexes = random.sample(range(total), scope_count)

        scopes_selected = []
        for i in indexes:
            item = self.SCOPE_ITEMS.nth(i)
            scopes_selected.append(item.inner_text().strip())
            item.click()

        self.page.keyboard.press("Escape")
        return scopes_selected

    # =============== Мульти таск функции ===============
    def fill_form(self,
                  phone_number: str = "+77777777777",
                  link: str = "https://test.kz",
                  email: str | None = None,
                  event_type: Literal["open_event", "closed_event"] = "open_event",
                  event_format: Literal["online", "astanahub", "hybrid"] = "online",
                  scope_count: int = 1,
                  ) -> list[str]:
        """
        Заполнение формы создания мероприятия (без проверок — ассерты в тесте)
        :param phone_number: Номер телефона для связи
        :param link: Ссылка на конференцию (для online/hybrid)
        :param email: Почта для связи (по умолчанию — почта тестового юзера)
        :param event_type: Тип ивента (открытый или закрытый)
        :param event_format: Формат проведения (online / astanahub / hybrid)
        :param scope_count: Сколько сфер выберет автотест
        :return: названия выбранных сфер
        """
        tz = timezone(timedelta(hours=5))

        self.COMPANY_SELECT.select_option(index=1)
        self.EVENT_TITLE_VISIBLE.fill(f"Auto test {datetime.now(tz)}")
        self.fill_description()
        self.upload_cover()

        self.select_format(event_format)
        self.set_dates()

        if event_format in ("online", "hybrid"):
            self.ONLINE_LINK.fill(link)

        scopes = self.select_scope(scope_count)

        self.EVENT_TYPE_SELECT.select_option(value=event_type)
        self.EVENT_PHONE.fill(phone_number)
        self.EVENT_EMAIL.fill(email or config.app.test_user_email)

        self.POLICY_CHECKBOX.check(force=True)
        self.AGREEMENT_CHECKBOX.check(force=True)

        return scopes

    def submit_for_moderation(self):
        """
        Клик "Опубликовать": создаёт ивент (POST /account/api/event/)
        и отправляет на модерацию (GET /account/api/event/{id}/send/).
        :return: (ответ создания, ответ отправки на модерацию) — статусы проверяются в тесте
        """
        self.PUBLISH_BTN.click()
        # Форма заполняется только на русском, поэтому появляется модалка автоперевода
        self.TRANSLATION_MODAL_SUBMIT.wait_for(state="visible")

        # Перевод занимает время, поэтому таймаут на ответы увеличен
        with self.page.expect_response(re.compile(r"/account/api/event/\d+/send/"), timeout=90000) as send_resp:
            with self.page.expect_response(re.compile(r"/account/api/event/$"), timeout=90000) as create_resp:
                self.TRANSLATION_MODAL_SUBMIT.click()

        return create_resp.value, send_resp.value

    def save_draft(self):
        """Клик "Сохранить как черновик". :return: ответ POST /account/api/event/"""
        with self.page.expect_response(re.compile(r"/account/api/event/")) as resp:
            self.SAVE_DRAFT_BTN.click()

        return resp.value
