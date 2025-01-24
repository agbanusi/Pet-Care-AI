from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class VendorCreate(BaseModel):
    username: constr(min_length=3, max_length=50)  # Username must be between 3 and 50 characters
    email: EmailStr  # Valid email format
    password: constr(min_length=6)  # Password must be at least 6 characters long
    business_name: constr(min_length=1, max_length=100)  # Name of the vendor's business
    business_address: constr(min_length=5, max_length=255)  # Address of the business
    business_phone: constr(min_length=10, max_length=15)  # Phone number of the business

class VendorUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)]  # Optional field
    email: Optional[EmailStr]  # Optional field
    password: Optional[constr(min_length=6)]  # Optional field
    business_name: Optional[constr(min_length=1, max_length=100)]  # Optional field
    business_address: Optional[constr(min_length=5, max_length=255)]  # Optional field
    business_phone: Optional[constr(min_length=10, max_length=15)]  # Optional field

class VendorResponse(BaseModel):
    id: int  # Unique identifier for the vendor
    username: str
    email: EmailStr
    business_name: str  # Name of the vendor's business
    business_address: str  # Address of the business
    business_phone: str  # Phone number of the business

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models