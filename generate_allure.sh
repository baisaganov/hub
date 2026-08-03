#!/bin/bash

rm -rf logs/allure-results logs/allure-report
mkdir -p logs/allure-results testdata/account_data

# API и UI гоняются отдельными процессами: sync-Playwright держит запущенный
# event loop в главном потоке, и asyncio-тесты в том же процессе после него падают.
# pytest --alluredir=logs/allure-results tests/api -v -n 2
# pytest --alluredir=logs/allure-results tests/ui -v -n 2




#rm -rf testdata/account_data

allure generate --config ./config/allurerc.json --output logs/allure-report logs/allure-results

allure open logs/allure-report




pytest tests/ui/test_event_create.py::TestEventsCreate::test_event_send
pytest tests/ui/test_vacancy_create_post.py::TestVacancy::test_vacancy_create_post_page