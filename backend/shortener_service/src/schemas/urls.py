from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class URLShortenRequest(BaseModel):
    """Схема для входящего запроса"""
    long_url: HttpUrl = Field(..., description="Оригинальная длинная ссылка")

class URLShortenResponse(BaseModel):
    """Схема для ответа клиенту"""
    short_url: str
    created_at: datetime
