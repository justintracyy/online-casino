from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.games import blackjack

router = APIRouter(tags=["blackjack"])

@router.post("/blackjack", response_model=schemas.BlackjackGameState)
def play_blackjack(game: schemas.BlackjackGame, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == game.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.balance < game.bet_amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    game_result = blackjack.simulate_blackjack(user.balance, game.bet_amount)

    # Update user balance in the database
    user.balance = game_result["playerBalance"]
    db.commit()

    # Create a transaction record
    transaction = models.Transaction(
        user_id=user.id,
        amount=game_result["payout"],  # Use the payout value
        game="Blackjack"
    )
    db.add(transaction)
    db.commit()

    return game_result