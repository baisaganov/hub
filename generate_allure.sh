#!/bin/bash

rm -rf logs/allure-results logs/allure-report
mkdir -p logs/allure-results testdata/account_data

# Линт: базовые правила + запрет asserts/pytest в pages/
ruff check . || exit 1

# Проверка Allure-метаданных (@allure.suite / @allure.title / owner) — валит запуск на коллекции
pytest tests --collect-only -q > /dev/null || exit 1

# API и UI гоняются отдельными процессами: sync-Playwright держит запущенный
# event loop в главном потоке, и asyncio-тесты в том же процессе после него падают.
pytest --alluredir=logs/allure-results tests/api -v -n 2
pytest --alluredir=logs/allure-results tests/ui -v -n 2


#rm -rf testdata/account_data

allure generate --config ./config/allurerc.json --output logs/allure-report logs/allure-results

allure open logs/allure-report




