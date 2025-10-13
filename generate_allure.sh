#!/bin/bash

# Очищаем предыдущие результаты
rm -rf allure-results
mkdir -p allure-results

# Запуск нужных тестов
#pytest --alluredir=allure-results tests/test_arm.py::TestArm::test_positive_accreditation
#pytest --alluredir=allure-results tests/test_registration.py::TestRegistration::test_valid_reg_email
pytest --alluredir=allure-results

# Копируем историю отчета (если есть)
if [ -d "allure-report/history" ]; then
  mkdir -p allure-results/history
  cp -r allure-report/history allure-results/
fi

# Генерация нового отчета
allure generate allure-results --clean -o allure-report

# Открытие отчета
allure open allure-report
