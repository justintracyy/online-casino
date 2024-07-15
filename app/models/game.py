from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    min_bet = Column(Float)
    max_bet = Column(Float)