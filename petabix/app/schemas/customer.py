from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class CustomerCreate(BaseModel):
    username: constr(min_length=3, max_length=50)  # Username must be between 3 and 50 characters
    email: EmailStr  # Valid email format
    password: constr(min_length=6)  # Password must be at least 6 characters
    full_name: constr(min_length=1, max_length=100)  # Full name of the customer
    customer_phone: constr(min_length=10, max_length=15)  # Phone number
    customer_address: constr(min_length=5, max_length=255)  # Address

class CustomerUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)]  # Optional field
    email: Optional[EmailStr]  # Optional field
    password: Optional[constr(min_length=6)]  # Optional field
    full_name: Optional[constr(min_length=1, max_length=100)]  # Optional field
    customer_phone: Optional[constr(min_length=10, max_length=15)]  # Optional field
    customer_address: Optional[constr(min_length=5, max_length=255)]  # Optional field

class CustomerResponse(BaseModel):
    id: int  # Unique identifier for the customer
    username: str
    email: EmailStr
    full_name: str  # Full name of the customer
    customer_phone: str  # Phone number
    customer_address: str  # Address

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models