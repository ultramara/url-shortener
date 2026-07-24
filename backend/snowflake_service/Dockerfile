FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /backend/snowflake_service/src/ ./src/

COPY proto/ ./proto/ 

RUN mkdir -p ./generated

RUN python -m grpc_tools.protoc \
    --proto_path=./proto \
    --python_out=./generated \
    --grpc_python_out=./generated \
    ./proto/*.proto

RUN touch ./generated/__init__.py

CMD [ "python", "-m", "src.run" ]
