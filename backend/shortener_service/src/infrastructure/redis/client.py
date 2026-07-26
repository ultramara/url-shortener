import os

from functools import lru_cache
from redis.asyncio import Redis, ConnectionPool
from fastapi import Request


async def init_redis() -> Redis:
    redis_url = os.getenv("REDIS_URL", "redis://url-shortener-redis:6379/0")

    pool = ConnectionPool.from_url(
        redis_url,
        decode_responses=True,
        encoding="utf-8",
        socket_timeout=2.0,
        socket_connect_timeout=2.0,
        max_connections=50,
        health_check_interval=30
    )

    client = Redis(connection_pool=pool)

    await client.ping()

    return client


def get_redis(request: Request) -> Redis:
    return request.app.state.redis
