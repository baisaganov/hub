# ===== STAGE 1: Builder (для установки всех зависимостей) =====
FROM python:3.12-slim as builder

WORKDIR /build

# Установка инструментов сборки
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre \
    npm \
    fonts-unifont \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка Allure (нужен npm и Java)
RUN npm install -g allure-commandline && \
    npm cache clean --force

# Копируем requirements и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Установка Playwright
RUN playwright install --with-deps chromium


# ===== STAGE 2: Runtime (финальный образ) =====
FROM python:3.12-slim

WORKDIR /usr/workspace

# Устанавливаем только runtime зависимости (без build-tools)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre-headless \
    fonts-unifont \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем Allure из builder
COPY --from=builder /usr/local/lib/node_modules/allure-commandline /opt/allure
RUN ln -s /opt/allure/bin/allure /usr/local/bin/allure

# Копируем Python packages из builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Копируем Playwright browsers из builder
COPY --from=builder /root/.cache/ms-playwright /root/.cache/ms-playwright

# Копируем исходный код
COPY . .

# Запуск тестов и генерация отчета
CMD ["/bin/sh", "-c", "pytest -sv --alluredir=allure-results || true; allure generate allure-results --clean -o allure-report"]
