import os
import uvicorn
import threading
from pathlib import Path

from src.snowflake_grpc.server import create_grpc_server, run_grpc_server, LoggingInterceptor

CURRENT_DIR = Path(__file__).resolve().parent
SRC_DIR = CURRENT_DIR / "src"

def run_rest():
    port = int(os.environ.get("PORT", 8001))

    uvicorn.run(
        "main:app",
        app_dir=str(SRC_DIR),
        host="0.0.0.0",
        port=port,
        log_level="info",
    )


def run_grpc():
    server = create_grpc_server(interceptors=[LoggingInterceptor()])
    run_grpc_server(server)


if __name__ == "__main__":
    threading.Thread(target=run_rest, daemon=True).start()
    run_grpc()

