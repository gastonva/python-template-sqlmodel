from uuid import UUID

from src import models
from src.api.v1 import schemas
from src.core.database import AsyncSession


class MovieController:
    @staticmethod
    async def create(
        movie_data: schemas.MovieCreate, owner_id: UUID, session: AsyncSession
    ) -> models.Movie:
        movie_data = schemas.Movie(owner_id=owner_id, **movie_data.model_dump())
        movie = await models.Movie.objects(session).create(movie_data.model_dump())
        await session.refresh(movie)
        return movie
