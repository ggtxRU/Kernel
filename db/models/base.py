import datetime
from typing import Optional

from sqlalchemy import Column, text, MetaData
from sqlalchemy.orm import declarative_base

import sqlalchemy.types as types


meta = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}, schema=None)

Base = declarative_base(metadata=meta)   # type: ignore


class BaseModel(Base):
    __abstract__ = True

    id = Column(types.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(
        types.TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP')
    )
    updated_at = Column(
        types.TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP')
    )

    __mapper_args__ = {"eager_defaults": True}
