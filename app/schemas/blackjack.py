from pydantic import BaseModel
from typing import List, Optional

class Card(BaseModel):
    suit: str
    value: str

class BlackjackGame(BaseModel):
    user_id: int
    bet_amount: float

class BlackjackGameState(BaseModel):
    gameId: str
    status: str
    playerHand: List[Card]
    playerHandValue: int
    dealerHand: List[Card]
    dealerHandValue: int
    currentBet: float
    playerBalance: float
    availableActions: List[str]
    lastAction: str
    outcome: Optional[str] = None
    payout: float  # Add this line