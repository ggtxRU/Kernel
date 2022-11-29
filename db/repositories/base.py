from typing import Any

from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from db.models.base import BaseModel


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def execute(self, query: Select) -> ChunkedIteratorResult:
        return await self._session.execute(query)

    async def one_or_none(self, query: Select) -> Any:
        result = await self.execute(query)
        return result.one_or_none()

    async def one_or_none_val(self, query: Select) -> Any:
        result = await self.one_or_none(query)
        if not result:
            return None
        return result[0]

    async def add_model(self, model: BaseModel) -> None:
        self._session.add(model)
        await self._session.flush([model])

    async def all_ones(self, query: Select) -> list[Any]:
        result = await self.execute(query)
        return [row[0] for row in result.all()]
