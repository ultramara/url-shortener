from fastapi import Request, Depends
from algorithms.shortener import UrlShortener
from algorithms.feistel import FeistelCipher
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
from src.repositories.url import UrlRepository
from generated import snowflake_pb2_grpc

def get_shortener() -> UrlShortener:
    feistel = FeistelCipher(secret_key=settings.FEISTEL_SECRET_KEY)
    return UrlShortener(base_url=settings.BASE_URL, feistel=feistel)


def get_url_repository(db: AsyncSession = Depends(get_db)) -> UrlRepository:
    """Фабрика для создания репозитория с текущей сессией БД"""
    return UrlRepository(db)

def get_snowflake_stub(request: Request) -> snowflake_pb2_grpc.SnowflakeStub:
    return request.app.state.snowflake_stub
