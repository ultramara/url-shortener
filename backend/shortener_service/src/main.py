import httpx
import grpc

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.config import settings
from src.core.http_client import http_container
from src.api.routers import url_shortener
from generated import snowflake_pb2_grpc

@asynccontextmanager
async def lifespan(app: FastAPI):
    http_container.client = httpx.AsyncClient(
        base_url="http://snowflake:8001",
        timeout=2.0
    )
    app.state.grpc_channel = grpc.insecure_channel('snowflake:50051')
    app.state.snowflake_stub  = snowflake_pb2_grpc.SnowflakeStub(app.state.grpc_channel)
    yield
    await http_container.client.aclose()
    app.state.grpc_channel.close()


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

