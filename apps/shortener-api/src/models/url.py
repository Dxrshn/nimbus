from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl


class ShortenRequest(BaseModel):
    url: HttpUrl


class UrlResponse(BaseModel):
    id: UUID
    short_code: str
    original_url: str
    short_url: str
    click_count: int
    created_at: datetime


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str