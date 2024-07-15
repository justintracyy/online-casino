from pydantic import BaseModel

class GameBase(BaseModel):
    name: str
    min_bet: float
    max_bet: float

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int

    class Config:
        orm_mode = True