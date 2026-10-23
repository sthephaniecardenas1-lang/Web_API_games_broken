from fastapi import HTTPException
from sqlmodel import Session, select

from models.game import Game
from schemas.game import GameCreate


def create_game(game_data: GameCreate, session: Session):
    game = Game(
        title=game_data.title,
        genre=game_data.genre,
        platform=game_data.platform,
        stock=game_data.stock,
        active=game_data.active
    )

    session.add(game)

    # orden correcto: add -> commit -> refresh
    # sin commit el insert nunca se confirma en arcade.db y refresh() falla,
    # porque el objeto todavía no existe en la base de datos
    session.commit()
    # recarga el juego ya guardado para obtener el id que generó SQLite
    session.refresh(game)

    return game


def list_games(session: Session):
    statement = select(Game)
    return session.exec(statement).all()


def get_game(game_id: int, session: Session):
    # session.get devuelve None si el id no existe
    game = session.get(Game, game_id)

    # si no existe se responde 404 con el mensaje pedido, en vez de devolver None
    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    return game


def delete_game(game_id: int, session: Session):
    game = session.get(Game, game_id)

    if not game:
        raise HTTPException(
            status_code=404,
            detail="Game not found"
        )

    session.delete(game)

    # delete() solo marca el registro para borrarlo dentro de la sesión;
    # el commit es lo que confirma el borrado en arcade.db
    session.commit()

    return {"message": "Game deleted"}
