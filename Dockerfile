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

CMD ["pytest", "-sv", "--alluredir=allure-results"]
