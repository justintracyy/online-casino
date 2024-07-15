from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    balance: float
    is_active: bool  # Make sure this line is here if you need it, or remove it if you don't

    class Config:
        orm_mode = True