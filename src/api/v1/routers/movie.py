from typing import Any

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependencies import db_session, get_user
from src.api.v1.schemas import Movie, MovieCreate
from src.controllers import MovieController
from src.core.database import AsyncSession
from src.models import User

router = APIRouter()


@router.get("", response_model=Page[Movie])
async def get_movies(
    user: User = Depends(get_user), session: AsyncSession = Depends(db_session)
) -> Any:
    return await paginate(session, user.get_movies())


@router.post("", response_model=Movie, status_code=201)
async def create_movie(
    movie_data: MovieCreate,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(db_session),
) -> Any:
    return await MovieController.create(
        movie_data=movie_data, owner_id=user.id, session=session
    )
