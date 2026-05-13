#!/bin/bash

rm -rf allure-results allure-report
mkdir -p allure-results testdata/account_data

pytest --alluredir=allure-results tests/ui/test_hubid.py::TestHubID::test_email_auth

rm -rf testdata/account_data

allure generate --config ./config/allurerc.json --output allure-report allure-results

allure open allure-report