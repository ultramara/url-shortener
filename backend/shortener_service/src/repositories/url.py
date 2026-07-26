from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.urls import Urls

class UrlRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, url_id: int, long_url: str, short_code: str) -> Urls:
        new_url = Urls(
            url_id=url_id,
            long_url=long_url,
            short_code=short_code
        )

        self.db.add(new_url)
        await self.db.commit()

        return new_url

    async def get_long_url(self, short_code) -> str:
        query = select(Urls.long_url).where(Urls.short_code == short_code)
        result = await self.db.execute(query)
        return result.scalars().first()
