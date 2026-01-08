#!/bin/bash

# Очищаем предыдущие результаты
rm -rf allure-results
mkdir -p allure-results

# Запуск нужных тестов
pytest --alluredir=allure-results tests/ui/test_hubid.py::TestHubID::test_phone_registration_from_auth
#pytest --alluredir=allure-results tests/old_registration.py::TestRegistration::test_valid_reg_email
#pytest --alluredir=allure-results --tracing=on

if [ -f "cookies.json" ]; then
  rm cookies.json
fi

# Копируем историю отчета (если есть)
if [ -d "allure-report/history" ]; then
  mkdir -p allure-results/history
  cp -r allure-report/history allure-results/
fi

# Генерация нового отчета
allure generate allure-results --clean -o allure-report

# Открытие отчета
allure open allure-report
