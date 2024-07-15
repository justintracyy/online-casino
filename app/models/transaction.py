from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    game = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())