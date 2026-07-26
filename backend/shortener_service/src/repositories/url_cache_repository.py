from redis.asyncio import Redis


class UrlCacheRepository:
    def __init__(self, redis: Redis) -> None:
        self._redis: Redis = redis

    async def set_long_url(
        self, 
        short_code: str,
        long_url: str,
        ttl_seconds: int = 600  # 10 минут
    ):
        key = f"url_cache:{short_code}"

        await self._redis.set(
            name=key, 
            value=long_url, 
            ex=ttl_seconds
        )

    async def get_long_url(self, short_code: str) -> str | None:
        key = f"url_cache:{short_code}"
        long_url = await self._redis.get(name=key)
        return long_url
