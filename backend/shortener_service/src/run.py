import os
import uvicorn
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
SRC_DIR = CURRENT_DIR / "src"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8002))

    uvicorn.run(
        "main:app",
        app_dir=str(SRC_DIR),
        host="0.0.0.0",
        port=port,
        log_level="info",
    )

