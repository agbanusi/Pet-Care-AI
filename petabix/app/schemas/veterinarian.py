from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class VeterinarianCreate(BaseModel):
    username: constr(min_length=3, max_length=50)  # Username must be between 3 and 50 characters
    email: EmailStr  # Valid email format
    password: constr(min_length=6)  # Password must be at least 6 characters long
    full_name: constr(min_length=1, max_length=100)  # Full name of the veterinarian
    license_number: constr(min_length=1, max_length=50)  # License number of the veterinarian
    specialization: constr(min_length=1, max_length=100)  # Area of specialization

class VeterinarianUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)]  # Optional field
    email: Optional[EmailStr]  # Optional field
    password: Optional[constr(min_length=6)]  # Optional field
    full_name: Optional[constr(min_length=1, max_length=100)]  # Optional field
    license_number: Optional[constr(min_length=1, max_length=50)]  # Optional field
    specialization: Optional[constr(min_length=1, max_length=100)]  # Optional field

class VeterinarianResponse(BaseModel):
    id: int  # Unique identifier for the veterinarian
    username: str
    email: EmailStr
    full_name: str  # Full name of the veterinarian
    license_number: str  # License number of the veterinarian
    specialization: str  # Area of specialization

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models