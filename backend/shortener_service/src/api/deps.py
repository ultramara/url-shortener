from typing import Annotated

from fastapi import HTTPException, Request, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from core.config import settings
from algorithms.shortener import UrlShortener
from algorithms.feistel import FeistelCipher
from src.infrastructure.redis.limiter import RateLimiter
from src.db.database import get_db
from src.infrastructure.redis.client import get_redis
from src.repositories.url import UrlRepository
from src.repositories.url_cache_repository import UrlCacheRepository
from generated import snowflake_pb2_grpc

def get_shortener() -> UrlShortener:
    feistel = FeistelCipher(secret_key=settings.FEISTEL_SECRET_KEY)
    return UrlShortener(base_url=settings.BASE_URL, feistel=feistel)


def get_url_repository(db: AsyncSession = Depends(get_db)) -> UrlRepository:
    """Фабрика для создания репозитория с текущей сессией БД"""
    return UrlRepository(db)

def get_cache_repository(redis: Redis = Depends(get_redis)) -> UrlCacheRepository:
    return UrlCacheRepository(redis)


def get_snowflake_stub(request: Request) -> snowflake_pb2_grpc.SnowflakeStub:
    return request.app.state.snowflake_stub


async def get_rate_limiter(redis: Annotated[Redis, Depends(get_redis)]) -> RateLimiter:
    return RateLimiter(redis)


def rate_limiter_factory(
    endpoint: str,
    max_requests: int,
    window_seconds: int    
):
    async def dependency(
        request: Request,
        rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
    ):
        ip_address = request.client.host

        limited = await rate_limiter.is_limited(
            ip_address,
            endpoint,
            max_requests,
            window_seconds,
        )

        if limited:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Превышено количество запросов. Повторите позже"
            )

    return dependency


rate_limiter_rest_shorten = rate_limiter_factory("rest-shorten", 5, 60)
rate_limiter_grpc_shorten = rate_limiter_factory("grpc-shorten", 5, 60)
rate_limiter_redirect = rate_limiter_factory("redirect", 60, 60)
