# Как написать API-тест

Пошаговый гайд по написанию API-теста в этом проекте: Pydantic-модели для контрактов,
Faker-фабрики для данных, клиенты для HTTP.

Главное правило: **на границе между тестом и HTTP данные всегда проходят через модель** —
и тело запроса, и тело ответа. Если в тесте появился `response.json()["..."]`
или в клиенте — словарь, собранный руками, значит какой-то шаг пропущен.

## Слои

```text
tests/api/          # сценарий и асерты — ЧТО проверяем
clients/            # HTTP-запросы, возвращают модели — КАК ходим в API
models/             # Pydantic-модели запросов/ответов — контракт API
testdata/factories.py  # Faker-фабрики тестовых данных
tests/api/conftest.py  # фикстуры клиентов (авторизованный / анонимный)
```

- В клиентах нет асертов и pytest — только HTTP и валидация моделей.
- В тестах нет разбора JSON руками — только вызовы клиента и асерты по полям модели.

## Шаг 1. Снять реальный ответ эндпоинта

Модель пишется по фактическому JSON, а не по памяти. Дёрните эндпоинт руками
и сохраните ответ — и успешный, и ошибочный:

```bash
uv run python - <<'EOF'
import asyncio, httpx, json
from clients.auth.auth_client import AuthClient
from config import config

async def main():
    async with httpx.AsyncClient(base_url=config.app.app_url, timeout=30000) as client:
        await AuthClient(client).login(config.app.test_user_email, config.app.test_user_password)
        r = await client.get("/api/my_endpoint/")          # ваш эндпоинт
        print(json.dumps(r.json(), ensure_ascii=False, indent=2))

asyncio.run(main())
EOF
```

## Шаг 2. Модель ответа в `models/`

Списываете структуру с реального JSON:

```python
# models/my_feature.py
from pydantic import BaseModel


class MyItem(BaseModel):
    id: int                  # обязательное поле
    title: str
    comment: str | None      # поле есть всегда, но может быть null
    is_active: bool


class MyListResponse(BaseModel):
    count: int
    results: list[MyItem]    # вложенные модели валидируются сами
```

Правила типов:

| В JSON | В модели |
|---|---|
| поле всегда есть | `title: str` |
| поле есть, но бывает `null` | `comment: str \| None` |
| поля может не быть | `comment: str = ""` (дефолт) |
| ISO-дата строкой | `created_at: datetime` — распарсится сама |
| словарь с переменными ключами | `RootModel[dict[str, ...]]` (см. `models/common.py`) |

Ответ DRF на 400 (`{"поле": ["сообщение"]}`) уже описан — `models/common.py::ValidationErrorResponse`,
переиспользуйте её для любого эндпоинта.

Новую модель добавьте в реэкспорт `models/__init__.py`.

## Шаг 3. Модель запроса + фабрика (если у запроса есть тело)

```python
# models/my_feature.py
class CreateItemRequest(BaseModel):
    title: str
    comment: str | None
```

```python
# testdata/factories.py
def fake_item_request() -> CreateItemRequest:
    return CreateItemRequest(
        title=f"Auto test {fake.uuid4()[:8]}",   # уникально при каждом вызове
        comment=fake.sentence(),
    )
```

Данные генерируются Faker'ом, а не хардкодятся: каждый вызов фабрики — уникальные
значения, поэтому тесты не конфликтуют при параллельном запуске (`-n N`)
и не зависят от состояния стенда.

## Шаг 4. Метод в клиенте

Один метод — один сценарий. У успеха и ошибки разные схемы ответа,
поэтому это разные методы с разными возвращаемыми типами:

```python
# clients/my_feature_client.py
from clients.base.base_client import BaseClient
from models import MyListResponse, CreateItemRequest, ValidationErrorResponse

ITEMS_URL = "/api/my_endpoint/"


class MyFeatureClient(BaseClient):
    async def get_items(self) -> MyListResponse:
        response = await self.get(ITEMS_URL, expected_status=200)
        return MyListResponse.model_validate(response.json())

    async def create_item(self, item: CreateItemRequest) -> MyItemResponse:
        response = await self.post(
            ITEMS_URL,
            json_body=item.model_dump(),      # модель -> dict для httpx
            expected_status=201,
        )
        return MyItemResponse.model_validate(response.json())

    async def create_item_expect_error(
        self, item: CreateItemRequest, expected_status: int = 400
    ) -> ValidationErrorResponse:
        response = await self.post(
            ITEMS_URL, json_body=item.model_dump(), expected_status=expected_status
        )
        return ValidationErrorResponse.model_validate(response.json())
```

Ключевые моменты:

- `expected_status` обязателен — `BaseClient` сам кинет `ApiError` с телом ответа,
  если статус не совпал. Тесту не нужно ассертить статус.
- `model_validate(response.json())` — валидация всего контракта одной строкой.
  Если бэкенд переименует/уберёт поле или сменит тип — тест упадёт
  с понятной `ValidationError`, а не со случайным `KeyError`.
- Если успешный ответ приходит с пустым телом — верните `httpx.Response` без модели
  (пример: `UserClient.save_contact`).

## Шаг 5. Фикстура клиента в `tests/api/conftest.py`

```python
@pytest.fixture
async def my_feature_client(authorized_http_client):
    yield MyFeatureClient(authorized_http_client)
```

- `authorized_http_client` — httpx-клиент с куками залогиненного юзера
  (логин один раз, куки берутся из cookie jar httpx).
- `anonymous_http_client` — без авторизации, для публичных эндпоинтов
  и проверок «без логина нельзя».

## Шаг 6. Тест

```python
# tests/api/test_my_feature.py
import allure
import pytest

from testdata.factories import fake_item_request

pytestmark = [pytest.mark.api]


@allure.suite("MyFeature")
@allure.label("owner", "aliwka")
class TestMyFeature:

    @allure.title("Создание айтема с валидными данными")
    @pytest.mark.asyncio
    async def test_create_item_valid(self, my_feature_client):
        item = fake_item_request()

        with allure.step("Создание айтема"):
            created = await my_feature_client.create_item(item)

        with allure.step("Проверка ответа"):
            assert created.title == item.title
            assert created.is_active is True

    @allure.title("Создание айтема без title возвращает 400")
    @pytest.mark.asyncio
    async def test_create_item_empty_title(self, my_feature_client):
        item = fake_item_request()
        item.title = ""

        with allure.step("Попытка создания"):
            errors = await my_feature_client.create_item_expect_error(item)

        with allure.step("Проверка ошибки валидации"):
            assert "title" in errors
            assert errors["title"], "Список ошибок по title пуст"
```

Требования к тесту:

- `@allure.suite`, `@allure.title` и `@allure.label("owner", ...)` обязательны
  (suite и owner можно вешать один раз на класс).
- `@pytest.mark.asyncio` на каждом async-тесте.
- Все асерты — в тесте, не в клиенте. Шаги — через `with allure.step(...)`.
- Если предусловие не выполнено (нет данных на стенде) — `pytest.skip("причина")`
  в тесте, не в клиенте.

## Шаг 7. Запуск

```bash
uv run pytest tests/api -v                # все API-тесты
uv run pytest tests/api -v -k my_feature  # только ваши
uv run pytest tests/api -n 2              # параллельно
```

## Чек-лист перед PR

- [ ] Модель ответа написана по реальному JSON со стенда
- [ ] Клиент возвращает модель, а не `dict` / сырой `Response` (кроме пустых ответов)
- [ ] Негативный сценарий — отдельный метод `*_expect_error`
- [ ] Тестовые данные — из фабрики (Faker), без хардкодов
- [ ] Асерты и `pytest.skip` только в тесте, в клиенте — только HTTP
- [ ] Allure-метаданные: suite, title, owner
