import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://arm-dev.astanahub.com/v2/login")
    page.get_by_role("button", name="Войти через HubID").click()
    page.get_by_role("textbox", name="Введите ваш email").click()
    page.get_by_role("textbox", name="Введите ваш email").fill("monitoring_staff@hub.kz")
    page.get_by_role("button", name="Продолжить", exact=True).click()
    page.get_by_role("textbox", name="Введите ваш пароль").fill("Pass1234!")
    page.get_by_role("textbox", name="Введите ваш пароль").press("Enter")
    page.get_by_role("button", name="Продолжить").click()
    page.get_by_role("link", name="Заявки new").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("link", name="Детальный мониторинг 1 кв").click()
    page.get_by_role("link", name="Заявки", exact=True).click()
    page.get_by_role("link", name="Мониторинг тест").click()
    page.get_by_role("link", name="Заявки", exact=True).click()
    page.get_by_role("link", name="Мониторинг Финтех").click()
    page.get_by_role("button", name="Массовая рассылка уведомлений").click()
    page.get_by_role("textbox", name="Выбор компании").click()
    page.get_by_role("textbox", name="Выбор компании").fill("Ас")
    page.get_by_text("Компания с очень длинным названием и с местонахождением которая еще не является ").click()
    page.get_by_role("button", name="Проверить получателей").click()
    page.get_by_text("000840001222").dblclick()
    page.locator("body").press("ControlOrMeta+c")
    page.get_by_text("000840001222").dblclick()
    page.get_by_text("000840001222").click()
    page.get_by_text("000840001222").dblclick()
    page.get_by_role("button", name="Отправить уведомления").click()
    page.get_by_role("button", name="Готово").click()
    page.locator("body").press("ControlOrMeta+с")
    page.locator("body").press("ControlOrMeta+с")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
