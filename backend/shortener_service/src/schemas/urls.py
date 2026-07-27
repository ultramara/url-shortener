from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class URLShortenRequest(BaseModel):
    """Схема для входящего запроса"""
    long_url: HttpUrl = Field(..., description="Оригинальная длинная ссылка")
    custom_code: str | None = Field(..., description="Пользовательский короткий код")

class URLShortenResponse(BaseModel):
    """Схема для ответа клиенту"""
    short_url: str
    created_at: datetime
