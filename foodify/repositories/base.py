import uuid
from typing import Any, AsyncIterator, Type, Sequence
from contextlib import asynccontextmanager

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select

from foodify.db.base import Base


class BaseRepository:
    table: Type[Base] = Base
    model_cls: Type[BaseModel] = BaseModel

    def __init__(self, session_maker: async_sessionmaker):
        self.session_maker = session_maker

    @asynccontextmanager
    async def create_session(self) -> AsyncIterator[AsyncSession]:
        session = self.session_maker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def _get_all(self) -> Sequence:
        async with self.create_session() as session:
            result = await session.execute(select(self.table))

        rows = result.scalars().all()
        return rows

    async def get_all(self) -> list[BaseModel]:
        rows = await self._get_all()
        return [self.model_cls.from_orm(row) for row in rows]

    async def _get_by(self, field: str, value: Any) -> Base | None:
        async with self.create_session() as session:
            result = await session.execute(
                select(self.table).where(getattr(self.table, field) == value)
            )
        row = result.scalars().first()
        return row

    async def get_by(self, field: str, value: Any) -> BaseModel | None:
        row = await self._get_by(field, value)
        if not row:
            return None

        return self.model_cls.from_orm(row)

    async def _get_by_filter(self, field: str, value: Any) -> Sequence:
        async with self.create_session() as session:
            result = await session.execute(
                select(self.table).where(getattr(self.table, field) == value)
            )

        rows = result.scalars().all()
        return rows

    async def _get_by_filter_with_wildcard(
        self, wildcard_table: Type[Base], field: str, value: Any
    ) -> Sequence:
        async with self.create_session() as session:
            result = await session.execute(
                select(self.table)
                .join(wildcard_table)
                .where(getattr(wildcard_table, field) == value)
            )

        rows = result.scalars().all()
        return rows

    async def get_by_filter(self, field: str, value: Any) -> list[BaseModel]:
        rows = await self._get_by_filter(field, value)
        return [self.model_cls.from_orm(row) for row in rows]

    async def get_by_id(self, id: uuid.UUID) -> BaseModel | None:
        return await self.get_by("id", id)

    async def create(self, model: BaseModel) -> BaseModel:
        async with self.create_session() as session:
            row = self.table(**model.dict())
            session.add(row)
            await session.commit()
            await session.refresh(row)

        return self.model_cls.from_orm(row)
