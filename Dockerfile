FROM python:3.12-slim

WORKDIR /usr/workspace

# Установи зависимости для Allure (Java)
RUN apt-get update && \
    apt-get install -y default-jre && \
    rm -rf /var/lib/apt/lists/*

# Установи allure через npm (нужен npm)
RUN apt-get update && \
    apt-get install -y npm && \
    npm install -g allure-commandline && \
    apt-get remove -y npm && \
    rm -rf /var/lib/apt/lists/*

# Копируй requirements
COPY requirements.txt .

# Установи Python зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Установи Playwright
RUN playwright install --with-deps chromium

# Копируй весь код
COPY . .

# Запусти тесты И генерацию отчета
# Даже если тесты упадут, отчет всё равно создастся
CMD ["/bin/sh", "-c", "pytest -sv --alluredir=allure-results || true; allure generate allure-results --clean -o allure-report"]
