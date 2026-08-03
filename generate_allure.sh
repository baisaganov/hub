#!/bin/bash

rm -rf logs/allure-results logs/allure-report
mkdir -p logs/allure-results testdata/account_data

# API и UI гоняются отдельными процессами: sync-Playwright держит запущенный
# event loop в главном потоке, и asyncio-тесты в том же процессе после него падают.
pytest --alluredir=logs/allure-results tests/api -v -s
pytest --alluredir=logs/allure-results tests/ui -v -s


#rm -rf testdata/account_data

allure generate --config ./config/allurerc.json --output logs/allure-report logs/allure-results

allure open logs/allure-report