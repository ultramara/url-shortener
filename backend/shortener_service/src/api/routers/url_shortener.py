import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from src.algorithms.shortener import UrlShortener
from src.schemas.urls import URLShortenRequest, URLShortenResponse
from src.repositories.url import UrlRepository
from src.repositories.url_cache_repository import UrlCacheRepository
from src.api.deps import (
    get_shortener, 
    get_url_repository, 
    get_cache_repository,
    rate_limiter_rest_shorten, 
    rate_limiter_grpc_shorten, 
    rate_limiter_redirect
)
from src.providers import get_id_from_rest, get_id_from_grpc
from src.core.url_shortener import create_short_url_core, get_long_url_core
from generated import snowflake_pb2, snowflake_pb2_grpc

router = APIRouter()

def create_shorten_endpoint(id_dependency):
    async def endpoint(
        long_url: URLShortenRequest,
        snowflake_id: int = Depends(id_dependency),
        shortener: UrlShortener = Depends(get_shortener),
        url_repository: UrlRepository = Depends(get_url_repository),
    ):
        return await create_short_url_core(
            snowflake_id=snowflake_id,
            long_url=str(long_url.long_url),
            shortener=shortener,
            url_repository=url_repository,
        )

    return endpoint


router.post(
    "/rest-shorten", 
    response_model=URLShortenResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limiter_rest_shorten)]
)(create_shorten_endpoint(get_id_from_rest))


router.post(
    "/grpc-shorten", 
    response_model=URLShortenResponse, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limiter_grpc_shorten)]
)(create_shorten_endpoint(get_id_from_grpc))


@router.get(
    "/{short_code}",
    dependencies=[Depends(rate_limiter_redirect)]
)
async def redirect_long_url(
    short_code: str, 
    cache_repository: UrlCacheRepository = Depends(get_cache_repository),
    url_repository: UrlRepository = Depends(get_url_repository),
):
    long_url = await get_long_url_core(short_code, cache_repository, url_repository)

    if not long_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Ссылка не найдена"
        )

    return RedirectResponse(url=long_url)
