FROM python:3.12-slim

WORKDIR /usr/workspace

# Обновляем sources.list с полным списком репозиториев (security, updates)
RUN echo "deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware" > /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre \
    npm \
    fonts-unifont && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Установка Allure через npm
RUN npm install -g allure-commandline && \
    apt-get remove -y npm && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps chromium

# Копируем весь код
COPY . .

# Запуск тестов и генерация отчета
CMD ["/bin/sh", "-c", "pytest -sv --alluredir=allure-results || true; allure generate allure-results --clean -o allure-report"]
