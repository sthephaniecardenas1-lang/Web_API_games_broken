from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_session
from schemas.game import GameCreate, GameResponse
from services.game_service import (
    create_game,
    list_games,
    get_game,
    delete_game,
)

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)


@router.post(
    "",
    response_model=GameResponse,
    status_code=201
)
def create_game_endpoint(
    game: GameCreate,
    session: Session = Depends(get_session)
):
    return create_game(game, session)


@router.get(
    "",
    # devuelve varios registros, por eso el modelo de respuesta es una lista
    response_model=list[GameResponse]
)
def list_games_endpoint(
    session: Session = Depends(get_session)
):
    return list_games(session)


@router.get(
    "/{game_id}",
    response_model=GameResponse
)
def get_game_endpoint(
    game_id: int,
    session: Session = Depends(get_session)
):
    return get_game(game_id, session)


@router.delete("/{game_id}")
def delete_game_endpoint(
    game_id: int,
    session: Session = Depends(get_session)
):
    return delete_game(game_id, session)
