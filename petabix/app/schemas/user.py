from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)  # Username must be between 3 and 50 characters
    email: EmailStr  # Valid email format
    password: constr(min_length=6)  # Password must be at least 6 characters

class UserUpdate(BaseModel):
    username: constr(min_length=3, max_length=50) = None  # Optional field
    email: EmailStr = None  # Optional field
    password: constr(min_length=6) = None  # Optional field

class UserResponse(BaseModel):
    id: int  # Assuming you have an ID field for the user
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models