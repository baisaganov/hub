FROM mcr.microsoft.com/playwright/python:v1.54.0-jammy

WORKDIR /usr/workspace

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre-headless \
    npm && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка Allure CLI
RUN npm install -g allure-commandline && \
    npm cache clean --force

# Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["/bin/sh", "-c", "pytest -sv --alluredir=allure-results || true; allure generate allure-results --clean -o allure-report"]
