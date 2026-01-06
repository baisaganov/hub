"""
Root conftest.py
Fixtures здесь доступны для ВСЕ тестов в проекте.
"""

import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path

from config import config
from utils.logger import Logger
import allure
import os

logger = Logger().get_logger(__name__)

TRACES_DIR = Path("traces")
SCREENSHOTS_DIR = Path("screenshots")
LOGS_DIR = Path("logs")

TRACES_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Аргументы браузера, берутся из конфига"""
    return {
        "headless": config.browser.headless,
        "slow_mo": config.browser.slow_mo,
    }


@pytest.fixture(scope="session")
def playwright():
    """Session-scoped"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright, browser_type_launch_args):
    """Если session один экземпляр браузера на все тесты, если function то каждый раз новый"""
    logger.info(f"Launching {config.browser.browser_type} browser")
    browser_type = getattr(playwright, config.browser.browser_type)
    browser = browser_type.launch(**browser_type_launch_args)

    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """Function-scoped - новый контекст на каждый тест"""
    FAKE_UA = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    context = browser.new_context(user_agent=FAKE_UA)
    context.set_default_timeout(config.browser.timeout)
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    """)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(request, context):
    print(f"Config loaded: {config.print_config()}")
    """Function-scoped - новый контекст на каждый тест"""
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")

    trace_path = TRACES_DIR / f"{test_name}_trace.zip"
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    yield page

    test_failed = (
        hasattr(request.node, 'rep_call') and
        request.node.rep_call.failed
    )

    context.tracing.stop(path=str(trace_path))

    if test_failed:
        logger.error(f"❌ TEST FAILED: {test_name}")

        # Скриншот
        screenshot_path = SCREENSHOTS_DIR / f"{test_name}_failure.png"
        screenshot_bytes = page.screenshot(path=str(screenshot_path))

        allure.attach(
            screenshot_bytes,
            name="Screenshot on failure",
            attachment_type=allure.attachment_type.PNG
        )
        logger.info(f"Screenshot saved: {screenshot_path}")

        if os.path.exists(trace_path):
            allure.attach.file(
                trace_path,
                name=f"Playwright Trace: {test_name}",
                attachment_type="application/zip"
            )
            logger.info(f"Trace saved: {trace_path}")

        else:
            logger.warning(f"Trace file not found: {trace_path}")
    else:
        logger.info(f"✅ TEST PASSED: {test_name}")

    context.close()
    # page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Общий hook для всех тестов"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def pytest_sessionstart(session):
    """Вызывается в начале сессии"""
    logger.info("PYTEST SESSION START")
    # config.print_config()


def pytest_sessionfinish(session, exitstatus):
    """Вызывается в конце сессии"""
    logger.info(f"PYTEST SESSION END - Exit status: {exitstatus}")
