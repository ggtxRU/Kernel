from typing import Optional

from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from vendors.config import DatabaseConfig


class Database:
    def __init__(self, engine: Optional[Engine] = None, async_engine: Optional[AsyncEngine] = None) -> None:
        self._engine = engine
        self._async_engine = async_engine

        if self._engine:
            self._session_factory = sessionmaker(bind=self._engine)
        else:
            self._session_factory = None

        if self._async_engine:
            self._async_session_factory = sessionmaker(self._async_engine, class_=AsyncSession, expire_on_commit=False)
        else:
            self._async_session_factory = None

    @property
    def async_engine(self) -> AsyncEngine:
        if not self._async_engine:
            raise ValueError
        return self._async_engine

    async def test_async_database(self) -> None:
        session = self.create_async_session()
        try:
            await session.execute('SELECT 2')
        except:
            await session.execute('CREATE DATABASE kernel_db')

    def create_async_session(self) -> AsyncSession:
        return self._async_session_factory()

    async def async_engine_close(self) -> None:
        await self.async_engine.dispose()


class DatabaseFactory:
    @staticmethod
    def get_dsn_by_config(config: DatabaseConfig) -> str:
        return f'{config.user}:{config.password}@{config.host}:{config.port}/{config.database}'

    @classmethod
    def get_async_from_config(cls, config: DatabaseConfig, pool_size: Optional[int] = None) -> Database:
        if not pool_size:
            pool_size = config.pool_size

        dsn = cls.get_dsn_by_config(config)
        engine = create_async_engine(f'postgresql+asyncpg://{dsn}', pool_pre_ping=True, pool_size=pool_size)
        return Database(async_engine=engine)