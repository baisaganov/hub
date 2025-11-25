FROM python:3.12-slim

WORKDIR /usr/workspace

# Установи зависимости для Allure (Java) и других инструментов
RUN apt-get update && \
    apt-get install -y default-jre allure && \
    rm -rf /var/lib/apt/lists/*

# Копируй requirements ДО других команд (для лучшего кэширования)
COPY requirements.txt .

# Установи Python зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Установи Playwright браузеры
RUN playwright install --with-deps chromium

# Копируй весь код
COPY . .

CMD ["pytest", "-sv", "--alluredir=allure-results"]






#WORKDIR /app
#
#COPY requirements.txt .
#
#RUN pip install --no-cache-dir -r requirements.txt
#
#FROM mcr.microsoft.com/playwright:v1.45.2-jammy
#
#WORKDIR /app
#
#COPY --from=builder /usr/local/lib/python3.12/site-packages \
#                    /usr/local/lib/python3.12/site-packages
#
#COPY . .
#
#RUN mkdir -p allure-results traces screenshots logs
#
#ENTRYPOINT ["pytest"]
#CMD ["tests/", "-v", "--alluredir=allure-results", "--clean-alluredir"]
