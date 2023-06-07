import datetime
import re
import uuid

import asyncpg.pgproto.pgproto as pg_proto
import pydantic.json
import sqlalchemy
from sqlalchemy import MetaData, orm
from sqlalchemy.dialects.postgresql import UUID, asyncpg
from sqlalchemy.dialects.postgresql import base as pg_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import as_declarative, declared_attr

from foodify.config import config

metadata = MetaData()


async_engine = create_async_engine(
    config.database_url,
    future=True,
    echo=True,
)
session_async = orm.sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


def camel_to_snake(name: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def get_table_name_from_class(cls: "Base") -> str:
    """
    Generate a table name for the model class
    """
    return camel_to_snake(cls.__name__) + "s"


@as_declarative(metadata=metadata)
class Base:
    """
    Base model class for ORM
    """

    id = sqlalchemy.Column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        nullable=False,
        index=True,
        default=uuid.uuid4,
    )
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        default=datetime.datetime.utcnow,
    )
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        nullable=True,
    )

    @declared_attr
    def __tablename__(cls):
        return get_table_name_from_class(cls)

    def __repr__(self):
        return "<" + self.__class__.__name__ + ": " + self.__str__() + ">"

    def __str__(self):
        return str(self.id)


# Patch sqlalchemy
class AsyncpgUUID(asyncpg.AsyncpgUUID):
    def bind_processor(self, dialect):
        if not self.as_uuid and dialect.use_native_uuid:

            def process(value):
                if value is not None:
                    if not isinstance(value, uuid.UUID):
                        return asyncpg._python_UUID(value)
                return value

            return process


# To make pydantic know about postgres uuid type
pydantic.json.ENCODERS_BY_TYPE[pg_proto.UUID] = str

# Patch asyncpg
asyncpg.PGDialect_asyncpg.colspecs[UUID] = AsyncpgUUID


# Patch sqlalchemy/databases
pg_base._python_UUID = lambda v: str(v) if isinstance(v, UUID) else v
