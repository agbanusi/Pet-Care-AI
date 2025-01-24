from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class RiderCreate(BaseModel):
    username: constr(min_length=3, max_length=50)  # Username must be between 3 and 50 characters
    email: EmailStr  # Valid email format
    password: constr(min_length=6)  # Password must be at least 6 characters long
    full_name: constr(min_length=1, max_length=100)  # Full name of the rider
    vehicle_type: constr(min_length=1, max_length=50)  # Type of vehicle (e.g., bike, car)
    vehicle_number: constr(min_length=1, max_length=20)  # Vehicle registration number

class RiderUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)]  # Optional field
    email: Optional[EmailStr]  # Optional field
    password: Optional[constr(min_length=6)]  # Optional field
    full_name: Optional[constr(min_length=1, max_length=100)]  # Optional field
    vehicle_type: Optional[constr(min_length=1, max_length=50)]  # Optional field
    vehicle_number: Optional[constr(min_length=1, max_length=20)]  # Optional field

class RiderResponse(BaseModel):
    id: int  # Unique identifier for the rider
    username: str
    email: EmailStr
    full_name: str  # Full name of the rider
    vehicle_type: str  # Type of vehicle
    vehicle_number: str  # Vehicle registration number

    class Config:
        orm_mode = True  # This allows Pydantic to work with ORM models