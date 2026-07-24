import grpc
import sys
import signal
from typing import List
from concurrent import futures

from generated import snowflake_pb2_grpc
from .snowflake_service import SnowflakeServiceImpl


def create_grpc_server(
    max_workers: int = 10,
    interceptors: List[grpc.ServerInterceptor] = []
):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers),
        interceptors=interceptors
    )

    snowflake_pb2_grpc.add_SnowflakeServicer_to_server(
        SnowflakeServiceImpl(), 
        server
    )
    
    return server


def run_grpc_server(
    server: grpc.Server,
    port: int = 50051,
    shutdown_timeout: int = 5
):
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    def handle_shutdown(signum, frame):
        server.stop(shutdown_timeout).wait()
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    server.wait_for_termination()


class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        print(f"[gRPC] Вызов: {method}")
        return continuation(handler_call_details)
