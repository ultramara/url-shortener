from fastapi import Depends
from src.core.http_client import http_container
from src.api.deps import get_snowflake_stub
from generated import snowflake_pb2, snowflake_pb2_grpc

async def get_id_from_rest() -> int:
    """Получает ID через REST-запрос к снежинке"""
    response = await http_container.client.get("/generate-id")
    response.raise_for_status()
    data = response.json()
    return data["id"]


async def get_id_from_grpc(
    stub: snowflake_pb2_grpc.SnowflakeStub = Depends(get_snowflake_stub)
) -> int:
    """Получает ID через gRPC-запрос к снежинке"""
    request = snowflake_pb2.EmptyRequest()
    response = stub.GenerateId(request, timeout=1.0)
    return response.snowflake_id
