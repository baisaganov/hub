# QA Automation Project

Проект для UI-автотестов на Python, Pytest и Playwright с поддержкой Allure Report. Playwright требует отдельной установки браузеров через `playwright install`, а Allure CLI обычно ставят отдельно от Python-зависимостей.

## Стек

- Python
- Pytest
- Playwright
- uv
- Allure Report
- Node.js

## Требования

Перед запуском должны быть установлены:

- Git
- Python 3.10+
- `pip`
- `uv`
- Node.js LTS: [nodejs.org](https://nodejs.org/en/download)
- Allure CLI

Playwright использует локально установленные браузеры, поэтому после установки зависимостей нужен отдельный шаг `playwright install`.[2]

## Quickstart

1. Клонировать репозиторий:

```bash
git clone <url>
cd <project_folder>
```

2. Получить или создать файл с секретами:

```bash
cp .env.example .env
```

Если шаблона `.env.example` нет, нужно запросить `.env` у команды или создать файл вручную с нужными переменными окружения.

3. Открыть проект в IDE.

4. Установить `uv`:

```bash
pip install uv
```

5. Установить Python-зависимости:

```bash
uv sync
```

Во многих Playwright-проектах `uv` используют для создания окружения и синхронизации зависимостей, а `uv sync --all-extras --dev` применяют, если проект разделяет dev/extras зависимости.[3][1]

6. Установить Node.js:

- Скачать: [nodejs.org](https://nodejs.org/en/download)

7. Установить Allure CLI:

```bash
npm install -g allure@3.3.1
```

8. Установить браузеры для Playwright:

```bash
playwright install
```

9. Запустить UI-тесты:

```bash
pytest tests/ui/ -v -s
```

## Запуск тестов

Базовый запуск:

```bash
pytest tests/ui/ -v -s
```

Примеры полезных вариантов:

```bash
pytest tests/ui/ -v -s -k login
pytest tests/ui/ -m smoke
pytest tests/ui/ --alluredir=logs/allure-results
```

Pytest можно запускать по маркерам, а результаты Allure обычно сохраняют в папку `allure-results` для последующего просмотра через `allure serve`.[1][4]

## Allure Report

Сформировать результаты:

```bash
pytest tests/ui/ --alluredir=logs/allure-results
```

Открыть отчет локально:

```bash
allure serve logs/allure-results
```

Во многих примерах с Pytest и Playwright локальный просмотр Allure запускают именно через `allure serve allure-results`.[1][4]

## Codegen

Для быстрой генерации сценария можно использовать Playwright Codegen:

```bash
playwright codegen https://dev.astanahub.com/v2/login --target=python -o test_case.py
```

Результат будет сохранен в файл `test_case.py` в корне проекта. После этого сгенерированные шаги можно адаптировать под Page Object, фикстуры и Allure-оформление теста.

## Переменные окружения

Рекомендуется хранить секреты только в `.env` и не коммитить этот файл в репозиторий.

Пример того, что часто указывают в `.env`:

```env
BASE_URL=https://dev.astanahub.com
LOGIN=<your_login>
PASSWORD=<your_password>
HEADLESS=false
ENV=dev
```

## Структура проекта

Ниже пример структуры, которую обычно используют в Playwright + Pytest проектах:

```text
.
├── tests/
│   ├── ui/
│   └── api/
├── pages/
├── utils/
├── conftest.py
├── pytest.ini
├── pyproject.toml
├── .env
├── .env.example
└── README.md
```

Для таких проектов обычно выносят тесты, page objects, утилиты и `conftest.py` отдельно, чтобы переиспользовать фикстуры и поддержку окружений.[5][6]

## Полезные команды Git

Начало работы с новой задачей:

```bash
git pull origin main
git checkout -b feature/new-tests
```

После изменений:

```bash
git add .
git commit -m "add: API tests for /auth endpoint"
git push origin feature/new-tests
```



Clients
Занимается только http
Условия:
- если действие нужно многим тестам — выноси в клиент,
- если это просто одна редкая проверка — можно оставить ближе к тесту,
- если метод в клиенте начинает содержать половину тестовой логики — ты перегрузил клиентgit restore -- .
git reset --hard
git clean -fd
git stash
git stash pop
git stash clear