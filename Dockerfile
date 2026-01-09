# ===== STAGE 1: Builder =====
FROM ubuntu:24.04 AS builder

WORKDIR /build

# Обновляем репозитории (Ubuntu имеет больше пакетов)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.12 \
    python3-pip \
    python3.12-venv \
    default-jre \
    npm \
    fonts-unifont \
    build-essential \
    curl \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка Allure
RUN npm install -g allure-commandline && \
    npm cache clean --force

# Копируем requirements и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Обновляем PATH для playwright
ENV PATH=/root/.local/bin:$PATH

# Установка Playwright (fonts-unifont уже установлен!)
RUN playwright install --with-deps chromium


# ===== STAGE 2: Runtime =====
FROM ubuntu:24.04

WORKDIR /usr/workspace

# Runtime зависимости (минимальные)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.12 \
    default-jre-headless \
    fonts-unifont \
    curl \
    libgbm1 \
    libnss3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем Allure из builder
COPY --from=builder /usr/local/lib/node_modules/allure-commandline /opt/allure
RUN ln -s /opt/allure/bin/allure /usr/local/bin/allure

# Копируем Python packages из builder
COPY --from=builder /root/.local /root/.local

# Копируем Playwright browsers из builder
COPY --from=builder /root/.cache/ms-playwright /root/.cache/ms-playwright

# Обновляем PATH
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1

# Копируем исходный код
COPY . .

# Запуск тестов
CMD ["/bin/sh", "-c", "python3 -m pytest -sv --alluredir=allure-results || true; allure generate allure-results --clean -o allure-report"]
