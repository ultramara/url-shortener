# High-Performance URL Shortener

A scalable microservice-based URL shortener built with Python and modern production practices. The project isolates ID generation using a distributed approach to ensure high availability and sub-millisecond lookups.

## 🛠️ Tech Stack & Architecture

- **FastAPI**: High-performance async web framework for the main application API.
- **gRPC**: Used for high-speed, binary-encoded inter-service communication.
- **Snowflake ID Generator**: A dedicated microservice for generating unique, time-ordered 64-bit IDs without DB bottlenecks.
- **PostgreSQL**: Reliable persistent storage for URL mappings with `asyncpg`.
- **Redis (Coming Soon)**: In-memory cache layer for lighting-fast redirection and DB load reduction.
- **Docker & Docker Compose**: Full containerization for reproducible local development and deployment.

## 📁 Repository Structure

- `proto/` — Protocol Buffers definitions (contracts).
- `backend/snowflake_service/` — gRPC ID generation microservice.
- `backend/shortener_service/` — Main URL shortener API.
