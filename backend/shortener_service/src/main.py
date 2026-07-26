import logging
import httpx
import grpc

from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.exceptions import ConnectionError, TimeoutError, RedisError
from src.core.config import settings
from src.core.http_client import http_container
from src.api.routers import url_shortener
from src.infrastructure.redis.client import init_redis
from generated import snowflake_pb2_grpc

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    http_container.client = httpx.AsyncClient(
        base_url="http://snowflake:8001",
        timeout=2.0
    )
    app.state.grpc_channel = grpc.insecure_channel('snowflake:50051')
    app.state.snowflake_stub  = snowflake_pb2_grpc.SnowflakeStub(app.state.grpc_channel)
    
    try:
        app.state.redis = await init_redis()
    except (ConnectionError, TimeoutError) as e:
        logger.critical(f"Redis недоступен при старте приложения: {e}")
        raise e
    
    yield

    try:
        await http_container.client.aclose()
    except Exception as e:
        logger.error(f"Ошибка при закрытии HTTP клиента: {e}")

    try:
        app.state.grpc_channel.close()
    except Exception as e:
        logger.error(f"Ошибка при закрытии gRPC канала: {e}")

    if hasattr(app.state, "redis") and app.state.redis:
        try:
            await app.state.redis.aclose()
        except RedisError as e:
            logger.error(f"Ошибка при закрытии пула Redis: {e}")


app = FastAPI(
    title="URL Shortener",
    description="URL Shortener service",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(url_shortener.router, tags=["URL Shortener"])

