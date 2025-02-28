 # schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class CarbonEntryCreate(BaseModel):
    category: str
    value: float

class CarbonEntryResponse(BaseModel):
    id: int
    user_id: int
    category: str
    value: float
    co2_emission: float

    class Config:
        from_attributes = True