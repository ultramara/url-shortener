from fastapi import Request, Depends
from src.algorithms.snowflake_generator import SnowflakeGenerator


def get_snowflake_generator(request: Request) -> SnowflakeGenerator:
    return request.app.state.snowflake_generator
