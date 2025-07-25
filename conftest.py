import pytest
from playwright.async_api import async_playwright
import logging
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

    with async_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=0, )  # slow_mo помогает увидеть действия
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

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
