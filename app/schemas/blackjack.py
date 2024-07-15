from pydantic import BaseModel

class BlackjackGame(BaseModel):
    user_id: int
    bet_amount: float

class BlackjackResult(BaseModel):
    message: str
    result: float
    new_balance: float