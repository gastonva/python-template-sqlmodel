from uuid import UUID

from sqlmodel import Field, ForeignKey

from src.core.database_sqlmodel import DatedTableMixinSQLModel, SQLBaseModel


class Movie(DatedTableMixinSQLModel, SQLBaseModel, table=True):
    title: str = Field(nullable=False)
    personal_rating: float = Field(ge=0, le=10)
    owner_id: UUID = Field(ForeignKey("user.id"))

    def __str__(self) -> str:
        return f"Movie {self.title} ({self.personal_rating})"
