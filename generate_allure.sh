#!/bin/bash

rm -rf logs/allure-results logs/allure-report
mkdir -p logs/allure-results testdata/account_data

pytest --alluredir=logs/allure-results tests/ui/ -v
pytest --alluredir=logs/allure-results tests/ -v -n 4


#rm -rf testdata/account_data

allure generate --config ./config/allurerc.json --output logs/allure-report logs/allure-results

allure open logs/allure-report