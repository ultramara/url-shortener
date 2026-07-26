from functools import lru_cache
from time import time
import random

from redis.asyncio import Redis


class RateLimiter:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def is_limited(
        self, 
        ip_address: str,
        endpoint: str,
        max_requests: int,
        window_seconds: int
    ) -> bool:
        key = f"rate_limiter:{endpoint}:{ip_address}" 

        current_ms = time() * 1000
        windows_start_ms = current_ms - window_seconds * 1000

        current_request = f"{current_ms}-{random.randint(0, 100_000)}"

        async with self._redis.pipeline() as pipe:
            await pipe.zremrangebyscore(key, 0, windows_start_ms)

            await pipe.zcard(key)

            await pipe.zadd(key, {current_request: current_ms})

            await pipe.expire(key, window_seconds)

            result = await pipe.execute()

        _, current_count, _, _ = result
        return current_count >= max_requests
