from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.games import blackjack

router = APIRouter(tags=["blackjack"])

@router.post("/blackjack")
def play_blackjack(user_id: int, bet_amount: float, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.balance < bet_amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    result, message = blackjack.play_blackjack(bet_amount)

    # Update user balance
    user.balance += result
    db.commit()

    # Record transaction
    transaction = models.Transaction(user_id=user_id, game="Blackjack", amount=result)
    db.add(transaction)
    db.commit()

    return {
        "message": message,
        "result": result,
        "new_balance": user.balance
    }