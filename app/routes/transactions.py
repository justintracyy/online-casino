from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.get("/{user_id}", response_model=list[schemas.Transaction])
def read_user_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    return transactions