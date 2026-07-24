from generated import snowflake_pb2, snowflake_pb2_grpc
from src.algorithms.snowflake_generator import SnowflakeGenerator
from src.core.config import settings


class SnowflakeServiceImpl(snowflake_pb2_grpc.SnowflakeServicer):
    """Реализация gRPC-сервиса снежинки"""
    
    def __init__(self):
        self.generator = SnowflakeGenerator(
            datacenter_id=settings.DATACENTER_ID,
            worker_id=settings.WORKER_ID,
            epoch=settings.EPOCH
        )
    
    def GenerateId(self, request, context):
        """Метод GenerateId — основной RPC"""
        new_id = self.generator.next_id()
        return snowflake_pb2.GenerateIdResponse(snowflake_id=new_id)
