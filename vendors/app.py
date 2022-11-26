from typing import Optional

import uvicorn
from fastapi import FastAPI, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from vendors.config import Config
from vendors.database import Database, DatabaseFactory


class Application:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._fast_api_server: Optional[FastAPI] = None
        self._db_primary: Optional[Database] = None

    def init_fast_api_server(self) -> None:
        self._fast_api_server = FastAPI(
            title=self._config.app.name,
            description=self._config.app.description,
            version=self._config.app.version,
            docs_url=self._config.server.docs_url,
            root_path=self._config.server.root_path
        )

    @property
    def config(self) -> Config:
        if not self._config:
            raise ValueError
        return self._config

    def init_primary_database_for_server(self) -> None:
        @self._fast_api_server.on_event('startup')
        async def init_primary_database_event() -> None:
            self._db_primary = DatabaseFactory.get_async_from_config(self._config.db_primary)
            await self._db_primary.test_async_database()

        @self._fast_api_server.on_event('shutdown')
        async def close_primary_database_event() -> None:
            await self._db_primary.async_engine_close()

    def add_routers(self, routers: list[APIRouter]) -> None:
        for router in routers:
            self._fast_api_server.include_router(router)

    def create_async_session(self) -> AsyncSession:
        return self._db_primary.create_async_session()

    def run_server(self) -> None:
        uvicorn.run(
            self._fast_api_server,  # type: ignore
            host=self._config.server.host,
            port=self._config.server.port,
            workers=self._config.server.workers
        )