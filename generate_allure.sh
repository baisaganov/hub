#!/bin/bash

# Очищаем предыдущие результаты
rm -rf allure-results
mkdir -p allure-results

# Запуск нужных тестов
#pytest --alluredir=allure-results tests/ui/test_events.py::TestEvents::test_event_save_single_scope
#pytest --alluredir=allure-results tests/old_registration.py::TestRegistration::test_valid_reg_email
pytest --alluredir=allure-results --tracing=on

# Копируем историю отчета (если есть)
if [ -d "allure-report/history" ]; then
  mkdir -p allure-results/history
  cp -r allure-report/history allure-results/
fi

# Генерация нового отчета
allure generate allure-results --clean -o allure-report

# Открытие отчета
allure open allure-report
