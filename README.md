# Обычный запуск
pytest tests/test_auth.py -v

# С Allure отчетом
pytest tests/ --alluredir=allure-results
allure serve allure-results

# Debug режим (видимый браузер)
HEADLESS=False pytest tests/test_auth.py -v -s

# Конкретный тест
pytest tests/test_auth.py::test_successful_login -v

# Параллельно (требует pytest-xdist)
pytest tests/ -n 4 --dist=loadscope

# Тестируем что fixtures загружаются правильно
pytest --fixtures

# Посмотреть где fixtures defined
pytest --fixtures | grep -A 5 "page"

# Запустить конкретный тест с verbose output
pytest tests/test_auth.py -v -s

# Посмотреть что используется
pytest tests/test_auth.py -v --setup-show


docker build -t playwright-tests .



project-root/
├── ✅config/
│   ├── __init__.py
│   ├── config.py                 # Конфиг окружения (base_url, timeouts и т.д.)
│   ├── browser_config.py         # Настройки браузеров (headless, resolution)
│   └── environment.py            # Загрузка переменных окружения
│
├── ✅pages/
│   ├── __init__.py
│   ├── base_page.py              # Базовый класс со всеми утилитами
│   ├── login_page.py             # Page Object для каждой страницы
│   ├── dashboard_page.py
│   └── ...
│
├── ✅api/
│   ├── __init__.py
│   ├── base_api.py               # Базовый класс для API запросов
│   ├── auth_api.py               # Отдельный класс для каждого API endpoint
│   ├── users_api.py
│   └── ...
│
│
├──✅ utils/
│   ├── __init__.py
│   ├── ✅ logger.py                 # Логирование

│
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Глобальный конфиг pytest
│   ├── ui/
│   │   ├── conftest.py           # UI-специфичные fixtures
│   │   ├── test_login.py
│   │   ├── test_dashboard.py
│   │   └── ...
│   └── api/
│       ├── conftest.py           # API-специфичные fixtures
│       ├── test_auth.py
│       ├── test_users.py
│       └── ...
│
├── ✅reports/                      # Auto-generated
├── ✅logs/                         # Auto-generated
├── ✅screenshots/                  # Auto-generated
│
├──✅ .env                          # Переменные окружения (не коммитить!)
├──✅ .env.example                  # Пример переменных
├── pytest.ini                    # Конфиг pytest
├── pyproject.toml                # Зависимости проекта
├── requirements.txt              # Python зависимости
└── README.md
└──✅ conftest.py

