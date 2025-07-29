import pytest
from playwright.sync_api import sync_playwright
import logging

from pages.auth_page import AuthPage


# import yaml


@pytest.fixture(scope="function")
def page():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Очистим старые хендлеры, чтобы не было дублирования
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler("logs_hub.log", mode='a')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Можно добавить вывод в консоль
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=0, args=['--window-size=1920,1080'])
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture
def auth_page(page):
    return AuthPage(page)


#
# def pytest_collection_modifyitems(items):
#     with open("./tests/order.yaml") as f:
#         order_map = yaml.safe_load(f)["order"]
#
#     file_order = {name: i for i, name in enumerate(order_map)}
#
#     items.sort(key=lambda item: (
#         file_order.get(os.path.basename(item.location[0]), 999),
#         item.name
#     ))
