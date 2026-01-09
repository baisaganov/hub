# ===== STAGE 1: Builder =====
FROM ubuntu:24.04 AS builder

WORKDIR /build

# ⭐ Установим python3-venv для поддержки виртуальных окружений
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    default-jre \
    npm \
    fonts-unifont \
    build-essential \
    curl \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ⭐ Создаем виртуальное окружение (главный ключ!)
RUN python3.12 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Установка Allure
RUN npm install -g allure-commandline && \
    npm cache clean --force

# Копируем requirements
COPY requirements.txt .

# Теперь pip установится в виртуальное окружение, а не в систему
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Установка Playwright
RUN playwright install --with-deps chromium


# ===== STAGE 2: Runtime =====
FROM ubuntu:24.04

WORKDIR /usr/workspace

# Минимальные runtime зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-minimal \
    default-jre-headless \
    fonts-unifont \
    curl \
    libgbm1 \
    libnss3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ⭐ Копируем ВЕСЬ виртуальный окружение из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем Allure из builder
COPY --from=builder /usr/local/lib/node_modules/allure-commandline /opt/allure
RUN ln -s /opt/allure/bin/allure /usr/local/bin/allure

# Копируем Playwright browsers из builder
COPY --from=builder /root/.cache/ms-playwright /root/.cache/ms-playwright

# Копируем исходный код
COPY . .

ENV PYTHONUNBUFFERED=1

# Запуск тестов
CMD ["/bin/sh", "-c", "pytest -sv --alluredir=allure-results || true; allure generate allure-results --clean -o allure-report"]
