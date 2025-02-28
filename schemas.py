 # schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True  # Converts SQLAlchemy models to Pydantic
