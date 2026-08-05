"""
Фабрики тестовых данных на Faker.
Каждый вызов генерирует новые уникальные данные — тесты не конфликтуют
между собой при параллельном запуске.
"""
from faker import Faker

from models import UpdateContactRequest, UpdateNamesRequest

fake = Faker("ru_RU")


def fake_contact_request() -> UpdateContactRequest:
    """Валидные контакты профиля"""
    url = fake.url(schemes=["https"])
    return UpdateContactRequest(
        contact_phone=f"+7777{fake.numerify('#######')}",
        contact_email=fake.email(),
        website=url,
        linkedin_url=url,
        facebook_url=url,
        portfolio_url=url,
    )


def empty_contact_request() -> UpdateContactRequest:
    """Контакты с пустыми полями — для негативных проверок"""
    return UpdateContactRequest(
        contact_phone=None,
        contact_email=None,
        website=None,
        linkedin_url=None,
        facebook_url=None,
        portfolio_url=None,
    )


def fake_invalid_email() -> str:
    """Синтаксически невалидный email"""
    return fake.email() + "@"


def fake_password(length: int = 12) -> str:
    return fake.password(length=length)


def fake_unregistered_email() -> str:
    """Валидный email, которого гарантированно нет в базе"""
    return f"autotest_{fake.uuid4()[:10]}@hub.kz"


def fake_phone() -> str:
    """Телефон тестового диапазона +7777XXXXXXX"""
    return f"+7777{fake.numerify('#######')}"


def fake_invalid_phone() -> str:
    """Синтаксически невалидный телефон"""
    return fake.lexify("????????")


def fake_names() -> UpdateNamesRequest:
    """Имя и фамилия для set_names / update_profile"""
    return UpdateNamesRequest(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
    )
