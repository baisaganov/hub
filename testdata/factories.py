"""
Фабрики тестовых данных на Faker.
Каждый вызов генерирует новые уникальные данные — тесты не конфликтуют
между собой при параллельном запуске.
"""
from faker import Faker

from models import UpdateContactRequest

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
