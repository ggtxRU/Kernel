from typing import Any

from sqlalchemy import select, exists
from sqlalchemy.cimmutabledict import immutabledict
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, Delete

from db.models.base import BaseModel


class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def execute(self, query: Select) -> ChunkedIteratorResult:
        return await self._session.execute(query)

    async def execute_fetch(self, query: Delete) -> None:
        return await self._session.execute(query, execution_options=immutabledict({"synchronize_session": 'fetch'}))

    async def one(self, query: Select) -> Any:
        result = await self.execute(query)
        return result.one()

    async def one_or_none(self, query: Select) -> Any:
        result = await self.execute(query)
        return result.one_or_none()

    async def one_val(self, query: Select) -> Any:
        result = await self.one(query)
        return result[0]

    async def one_or_none_val(self, query: Select) -> Any:
        result = await self.one_or_none(query)
        if not result:
            return None
        return result[0]

    async def add_model(self, model: BaseModel) -> None:
        self._session.add(model)
        await self._session.flush([model])

    async def add_model_ignore_exceptions(self, model: BaseModel) -> None:
        try:
            async with self._session.begin_nested():
                await self.add_model(model)
        except IntegrityError:
            pass

    async def add_models(self, models: list[BaseModel]) -> None:
        for model in models:
            await self.add_model(model)

    async def delete(self, model: BaseModel) -> None:
        await self._session.delete(model)

    async def delete_many(self, models: list[BaseModel]) -> None:
        for model in models:
            await self.delete(model)

    async def all(self, query: Select) -> list[Any]:
        result = await self.execute(query)
        return result.all()

    async def all_ones(self, query: Select) -> list[Any]:
        result = await self.execute(query)
        return [row[0] for row in result.all()]

    async def exists(self, query: Select) -> bool:
        query = select(exists(query))
        return await self.one_val(query)
