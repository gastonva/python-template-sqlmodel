import uuid
from datetime import datetime
from typing import Any, Dict, Generic, Sequence, Type, TypeVar

from fastapi import HTTPException
from sqlalchemy import Column, DateTime, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Field, SQLModel


class SQLBaseModel(SQLModel):
    __abstract__ = True

    @classmethod
    def objects(
        cls: Type["_ModelSQLModel"], session: AsyncSession
    ) -> "ObjectsSQLModel[_ModelSQLModel]":
        return ObjectsSQLModel(cls, session)


_ModelSQLModel = TypeVar("_ModelSQLModel", bound=SQLBaseModel)


class TableIdMixinSQLModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class DatedTableMixinSQLModel(TableIdMixinSQLModel):
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), server_default=func.now(), nullable=True
        )
    )
    updated_at: datetime = Field(sa_column=Column(DateTime(), onupdate=func.now()))


# Gestor de consultas asíncronas
class ObjectsSQLModel(Generic[_ModelSQLModel]):
    cls: Type[_ModelSQLModel]
    session: AsyncSession
    base_statement: Any
    queryset_filters: Any = None

    def __init__(
        self,
        cls: Type[_ModelSQLModel],
        session: AsyncSession,
        *queryset_filters: Any,
    ) -> None:
        self.cls = cls
        self.session = session
        base_statement = select(cls)
        if queryset_filters:
            self.queryset_filters = queryset_filters
            base_statement = base_statement.where(*queryset_filters)
        self.base_statement = base_statement

    async def all(self) -> Sequence[_ModelSQLModel]:
        result = await self.session.execute(self.base_statement)
        return result.scalars().unique().all()

    async def get(self, *where_clause: Any) -> _ModelSQLModel | None:
        statement = self.base_statement.where(*where_clause)
        result = await self.session.execute(statement)
        return result.unique().scalar_one_or_none()

    async def get_or_404(self, *where_clause: Any) -> _ModelSQLModel:
        obj = await self.get(*where_clause)
        if obj is None:
            raise HTTPException(
                status_code=404, detail=f"{self.cls.__name__} not found"
            )
        return obj

    async def get_all(self, *where_clause: Any) -> Sequence[_ModelSQLModel]:
        statement = self.base_statement.where(*where_clause)
        result = await self.session.execute(statement)
        return result.scalars().unique().all()

    async def count(self, *where_clause: Any) -> int:
        statement = select(func.count()).select_from(self.cls)
        if self.queryset_filters:
            statement = statement.where(*self.queryset_filters)
        if where_clause:
            statement = statement.where(*where_clause)

        result = await self.session.execute(statement)
        return result.scalar_one()

    async def create(self, data: Dict[str, Any]) -> _ModelSQLModel:
        obj = self.cls(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def bulk_create(
        self, data: Sequence[Dict[str, Any]]
    ) -> Sequence[_ModelSQLModel]:
        objs = [self.cls(**item) for item in data]
        self.session.add_all(objs)
        await self.session.commit()
        return objs
