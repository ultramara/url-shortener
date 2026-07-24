import httpx


class HttpClientContainer:
    client: httpx.AsyncClient = None


http_container = HttpClientContainer()
