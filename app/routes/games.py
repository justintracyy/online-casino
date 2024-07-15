from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.games import slot_machine, roulette, blackjack

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    db_game = models.Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get("/{game_id}", response_model=schemas.Game)
def read_game(game_id: int, db: Session = Depends(get_db)):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game

@router.post("/{game_id}/play")
def play_game(game_id: int, user_id: int, bet_amount: float, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    game = db.query(models.Game).filter(models.Game.id == game_id).first()

    if user is None or game is None:
        raise HTTPException(status_code=404, detail="User or Game not found")

    if user.balance < bet_amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    if bet_amount < game.min_bet or bet_amount > game.max_bet:
        raise HTTPException(status_code=400, detail="Bet amount out of range")

    # Play the game
    if game.name == "Slot Machine":
        result = slot_machine.play(bet_amount)
        message = "Slot machine result"
    elif game.name == "Roulette":
        result = roulette.play(bet_amount)
        message = "Roulette result"
    elif game.name == "Blackjack":
        result, message = blackjack.play(bet_amount)
    else:
        raise HTTPException(status_code=400, detail="Unknown game")

    # Update user balance
    user.balance += result

    # Record transaction
    transaction = models.Transaction(user_id=user_id, game_id=game_id, amount=result)
    db.add(transaction)

    db.commit()
    return {"result": result, "message": message, "new_balance": user.balance}