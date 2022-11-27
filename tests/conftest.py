import os
from typing import Generator

import pytest
from alembic import command
from sqlalchemy.engine import URL
from starlette.testclient import TestClient
from alembic.config import Config as AlembicConfig

from server.routers import routers
from vendors.app import Application
from vendors.config import Config
from vendors.database import DatabaseFactory, Database
from vendors.router import CustomRoute


@pytest.fixture(scope='session')
def config() -> Config:
    config_path = os.environ.get('CONFIG', 'configs/test.yaml')
    return Config(file=config_path)


@pytest.fixture(scope='session')
def database(config) -> Database:
    os.environ['CONFIG'] = 'configs/test.yaml'
    database = DatabaseFactory.get_from_config(config.db_primary)
    database.engine.execute("""
        DROP SCHEMA public CASCADE;
        CREATE SCHEMA public;
        GRANT ALL ON SCHEMA public TO postgres;
        GRANT ALL ON SCHEMA public TO public;
    """)
    db_config = config.db_primary
    dsn = str(URL(
        drivername='postgresql',
        host=db_config.host,
        port=db_config.port,
        username=db_config.user,
        password=db_config.password,
        database=db_config.database
    ))
    config = AlembicConfig('./alembic.ini')
    config.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(config, 'head')

    return database


@pytest.fixture(scope='session')
def app(config, database) -> Application:
    app = Application(config)

    app.init_fast_api_server()

    app.init_primary_database_for_server()

    CustomRoute.set_app(app)

    app.add_routers(routers)

    return app


@pytest.fixture(scope='session')
def client(app) -> Generator:
    with TestClient(app.fast_api_server) as client:
        yield client
