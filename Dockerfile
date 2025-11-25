FROM python:3.12-slim

WORKDIR /usr/workspace

# Установи allure через apt
RUN apt-get update && \
    apt-get install -y default-jre allure && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN playwright install --with-deps chromium

COPY . .

# Запусти тесты, потом ВСЕГДА создай отчет, но сохрани exit code тестов
CMD ["/bin/sh", "-c", "pytest -sv --alluredir=allure-results || true; allure generate allure-results --clean -o allure-report"]
