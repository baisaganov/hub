from datetime import datetime

from pydantic import BaseModel


class LocalizedText(BaseModel):
    en: str
    kk: str
    ru: str


class EventAuthor(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    avatar_letters: str


class Event(BaseModel):
    id: int
    author: EventAuthor
    title: LocalizedText
    slug: str
    content: LocalizedText
    datetime_start: datetime
    datetime_end: datetime
    event_format: str
    event_type: str
    absolute_url: str
    created_at: datetime
    status: str
    is_favorite: bool
    is_participated_by_me: bool
    available: bool
    company_id: int | None
    registration_fields: list[str]
    image_url: str | None


class EventsListResponse(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: list[Event]
