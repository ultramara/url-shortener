from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.core.config import settings
from src.algorithms.snowflake_generator import SnowflakeGenerator
from src.api.routers import snowflake

@asynccontextmanager
async def lifespan(app: FastAPI):
    generator = SnowflakeGenerator(
        datacenter_id=settings.DATACENTER_ID,
        worker_id=settings.WORKER_ID,
        epoch=settings.EPOCH
    )
    app.state.snowflake_generator = generator
    yield
    del app.state.snowflake_generator


app = FastAPI(
    title="Snowflake Generator",
    description="Twitter Snowflake ID generator service",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(snowflake.router, tags=["Snowflake"])
