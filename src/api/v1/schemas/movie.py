from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MovieCreate(BaseModel):
    title: str
    personal_rating: float


class Movie(MovieCreate):
    owner_id: UUID
    model_config = ConfigDict(from_attributes=True)
