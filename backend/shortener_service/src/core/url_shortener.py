import datetime
from typing import Callable, Awaitable
from fastapi import Depends, HTTPException, status
import httpx
import grpc

from src.schemas.urls import URLShortenRequest, URLShortenResponse
from src.algorithms.shortener import UrlShortener
from src.repositories.url import UrlRepository
from src.api.deps import get_shortener, get_url_repository


async def create_short_url_core(
    snowflake_id: int,
    long_url: str,
    shortener: UrlShortener,
    url_repository: UrlRepository 
) -> URLShortenResponse:
    try:
        short_code = shortener.create_short_code(snowflake_id)

        await url_repository.create(
            url_id=snowflake_id,
            long_url=long_url,
            short_code=short_code
        )

        short_url = shortener.create_short_url(short_code)

        return URLShortenResponse(
            short_url=short_url,
            created_at=datetime.datetime.now(datetime.timezone.utc)
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Ошибка генератора снежинок (REST): {exc.response.status_code}"
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Сервис снежинок (REST) недоступен"
        )
    except grpc.RpcError as exc:
        if exc.code() == grpc.StatusCode.UNAVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Сервис снежинок (gRPC) недоступен"
            )
        elif exc.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Сервис снежинок (gRPC) не отвечает"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Ошибка снежинки (gRPC): {exc.details()}"
            )