from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    user_id: int
    game_id: int
    amount: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True