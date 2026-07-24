from fastapi import APIRouter, Depends
from src.algorithms.snowflake_generator import SnowflakeGenerator
from src.api.deps import get_snowflake_generator

router = APIRouter()


@router.get("/generate-id")
def get_id(generator: SnowflakeGenerator = Depends(get_snowflake_generator)):
    new_id = generator.next_id()
    return {"id": new_id}
