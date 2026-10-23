from pydantic import BaseModel, Field


class GameCreate(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    genre: str = Field(min_length=3, max_length=40)
    platform: str = Field(min_length=2, max_length=30)

    # el stock debe estar entre 1 y 50: no se registra un juego con 0 unidades
    # (antes el límite inferior era ge=0 y por eso aceptaba stock = 0)
    stock: int = Field(ge=1, le=50)

    active: bool = True


class GameResponse(BaseModel):
    id: int
    title: str
    genre: str
    platform: str
    stock: int
    active: bool
